"""
Analysis calculations and aggregations for procurement data
"""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
import sys

# Add parent to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    MIN_SUPPLIERS_FOR_CONSOLIDATION,
    MIN_SPEND_FOR_CONSOLIDATION,
    TOP_N_SUPPLIERS,
    AMOUNT_COLUMN,
    SUPPLIER_COLUMN,
    STATE_COLUMN,
    DATE_COLUMN,
    CATEGORY_COLUMN
)


@st.cache_data(ttl=3600)
def calculate_spend_by_period(df, period='M'):
    """
    Calculate spend over time aggregated by period

    Args:
        df: DataFrame with procurement data
        period: Period for aggregation ('D'=daily, 'W'=weekly, 'M'=monthly, 'Q'=quarterly, 'Y'=yearly)

    Returns:
        pd.Series: Spend by period
    """
    if df.empty or DATE_COLUMN not in df.columns:
        return pd.Series()

    return df.groupby(df[DATE_COLUMN].dt.to_period(period))[AMOUNT_COLUMN].sum().sort_index()


@st.cache_data(ttl=3600)
def calculate_top_suppliers(df, n=TOP_N_SUPPLIERS):
    """
    Get top N suppliers by total spend

    Args:
        df: DataFrame with procurement data
        n: Number of top suppliers to return

    Returns:
        pd.Series: Top N suppliers with spend amounts
    """
    if df.empty or SUPPLIER_COLUMN not in df.columns:
        return pd.Series()

    return df.groupby(SUPPLIER_COLUMN)[AMOUNT_COLUMN].sum().nlargest(n)


@st.cache_data(ttl=3600)
def calculate_spend_by_category(df):
    """
    Calculate total spend by category

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.Series: Spend by category
    """
    if df.empty or 'Category' not in df.columns:
        return pd.Series()

    return df.groupby('Category')[AMOUNT_COLUMN].sum().sort_values(ascending=False)


@st.cache_data(ttl=3600)
def calculate_spend_by_subcategory(df):
    """
    Calculate total spend by subcategory

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.Series: Spend by subcategory
    """
    if df.empty or 'SubCategory' not in df.columns:
        return pd.Series()

    return df.groupby('SubCategory')[AMOUNT_COLUMN].sum().sort_values(ascending=False)


@st.cache_data(ttl=3600)
def calculate_spend_by_state(df):
    """
    Calculate total spend by state

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.Series: Spend by state
    """
    if df.empty or STATE_COLUMN not in df.columns:
        return pd.Series()

    return df.groupby(STATE_COLUMN)[AMOUNT_COLUMN].sum().sort_values(ascending=False)


@st.cache_data(ttl=3600)
def calculate_supplier_count_by_state(df):
    """
    Calculate number of unique suppliers by state

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.Series: Supplier count by state
    """
    if df.empty or STATE_COLUMN not in df.columns or SUPPLIER_COLUMN not in df.columns:
        return pd.Series()

    return df.groupby(STATE_COLUMN)[SUPPLIER_COLUMN].nunique().sort_values(ascending=False)


@st.cache_data(ttl=3600)
def calculate_consolidation_opportunities(df, min_suppliers=MIN_SUPPLIERS_FOR_CONSOLIDATION,
                                         min_spend=MIN_SPEND_FOR_CONSOLIDATION):
    """
    Identify consolidation opportunities (subcategories with multiple suppliers)

    Args:
        df: DataFrame with procurement data
        min_suppliers: Minimum number of suppliers to flag as opportunity
        min_spend: Minimum total spend to flag as opportunity

    Returns:
        pd.DataFrame: Consolidation opportunities with metrics
    """
    if df.empty or 'SubCategory' not in df.columns:
        return pd.DataFrame()

    opportunities = []

    for subcategory in df['SubCategory'].dropna().unique():
        subcat_df = df[df['SubCategory'] == subcategory]
        num_suppliers = subcat_df[SUPPLIER_COLUMN].nunique()
        total_spend = subcat_df[AMOUNT_COLUMN].sum()

        if num_suppliers >= min_suppliers and total_spend >= min_spend:
            state_breakdown = subcat_df.groupby(STATE_COLUMN)[SUPPLIER_COLUMN].nunique()

            opportunities.append({
                'SubCategory': subcategory,
                'Suppliers': num_suppliers,
                'Total Spend': total_spend,
                'States': len(state_breakdown),
                'Avg per Supplier': total_spend / num_suppliers,
                'Potential Savings (10%)': total_spend * 0.10,
                'Potential Savings (15%)': total_spend * 0.15
            })

    if not opportunities:
        return pd.DataFrame()

    return pd.DataFrame(opportunities).sort_values('Total Spend', ascending=False)


@st.cache_data(ttl=3600)
def calculate_po_metrics(df):
    """
    Calculate purchase order metrics

    Args:
        df: DataFrame with procurement data

    Returns:
        dict: PO metrics
    """
    if df.empty:
        return {}

    metrics = {
        'total_pos': df['VSTX PO #'].nunique() if 'VSTX PO #' in df.columns else 0,
        'avg_po_value': df[AMOUNT_COLUMN].mean(),
        'median_po_value': df[AMOUNT_COLUMN].median(),
        'max_po_value': df[AMOUNT_COLUMN].max(),
        'min_po_value': df[AMOUNT_COLUMN].min()
    }

    # PO status breakdown if available
    if 'PO Status' in df.columns:
        status_counts = df['PO Status'].value_counts()
        metrics['po_status'] = status_counts.to_dict()
        if 'Closed' in status_counts.index:
            total_pos = status_counts.sum()
            metrics['closure_rate'] = (status_counts['Closed'] / total_pos) * 100 if total_pos > 0 else 0

    return metrics


@st.cache_data(ttl=3600)
def calculate_supplier_metrics(df):
    """
    Calculate supplier-level metrics

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.DataFrame: Supplier metrics
    """
    if df.empty or SUPPLIER_COLUMN not in df.columns:
        return pd.DataFrame()

    supplier_metrics = df.groupby(SUPPLIER_COLUMN).agg({
        AMOUNT_COLUMN: ['sum', 'mean', 'count'],
        CATEGORY_COLUMN: 'nunique' if CATEGORY_COLUMN in df.columns else lambda x: 0
    }).round(2)

    # Flatten column names (lowercase with underscores for consistency)
    supplier_metrics.columns = ['total_spend', 'avg_po_value', 'po_count', 'category_count']

    return supplier_metrics.sort_values('total_spend', ascending=False)


@st.cache_data(ttl=3600)
def calculate_category_metrics(df):
    """
    Calculate category-level metrics

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.DataFrame: Category metrics
    """
    if df.empty or 'Category' not in df.columns:
        return pd.DataFrame()

    category_metrics = df.groupby('Category').agg({
        AMOUNT_COLUMN: ['sum', 'mean', 'count'],
        SUPPLIER_COLUMN: 'nunique',
        'SubCategory': 'nunique' if 'SubCategory' in df.columns else lambda x: 0
    }).round(2)

    # Flatten column names (lowercase with underscores for consistency)
    category_metrics.columns = ['total_spend', 'avg_po_value', 'po_count', 'supplier_count', 'subcategory_count']

    return category_metrics.sort_values('total_spend', ascending=False)


@st.cache_data(ttl=3600)
def calculate_top_concentration(df, n=20):
    """
    Calculate concentration of top N suppliers

    Args:
        df: DataFrame with procurement data
        n: Number of top suppliers

    Returns:
        dict: Concentration metrics
    """
    if df.empty or SUPPLIER_COLUMN not in df.columns:
        return {}

    total_spend = df[AMOUNT_COLUMN].sum()
    top_n_spend = calculate_top_suppliers(df, n).sum()

    return {
        'top_n': n,
        'top_n_spend': top_n_spend,
        'total_spend': total_spend,
        'concentration_pct': (top_n_spend / total_spend * 100) if total_spend > 0 else 0,
        'remaining_spend': total_spend - top_n_spend,
        'remaining_pct': ((total_spend - top_n_spend) / total_spend * 100) if total_spend > 0 else 0
    }


@st.cache_data(ttl=3600)
def calculate_geographic_metrics(df):
    """
    Calculate geographic distribution metrics

    Args:
        df: DataFrame with procurement data

    Returns:
        pd.DataFrame: Geographic metrics by state
    """
    if df.empty or STATE_COLUMN not in df.columns:
        return pd.DataFrame()

    geo_metrics = df.groupby(STATE_COLUMN).agg({
        AMOUNT_COLUMN: 'sum',
        SUPPLIER_COLUMN: 'nunique',
        'VSTX PO #': 'nunique' if 'VSTX PO #' in df.columns else 'count'
    }).round(2)

    geo_metrics.columns = ['Total Spend', 'Unique Suppliers', 'PO Count']

    # Add percentage of total spend
    total_spend = df[AMOUNT_COLUMN].sum()
    geo_metrics['% of Total Spend'] = (geo_metrics['Total Spend'] / total_spend * 100).round(2)

    return geo_metrics.sort_values('Total Spend', ascending=False)


def calculate_spend_trend_stats(spend_series):
    """
    Calculate trend statistics for spend over time

    Args:
        spend_series: Series with spend by period

    Returns:
        dict: Trend statistics
    """
    if spend_series.empty or len(spend_series) < 2:
        return {}

    # Convert period index to timestamp for calculations
    spend_values = spend_series.values

    return {
        'average': np.mean(spend_values),
        'median': np.median(spend_values),
        'std_dev': np.std(spend_values),
        'min': np.min(spend_values),
        'max': np.max(spend_values),
        'trend': 'increasing' if spend_values[-1] > spend_values[0] else 'decreasing',
        'change_pct': ((spend_values[-1] - spend_values[0]) / spend_values[0] * 100) if spend_values[0] != 0 else 0
    }
