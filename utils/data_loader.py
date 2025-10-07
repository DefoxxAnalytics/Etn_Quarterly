"""
Data loading and filtering utilities with Streamlit caching
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Add parent to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    CSV_PATH, CSV_ENCODING, DATE_COLUMN,
    AMOUNT_COLUMN, SUPPLIER_COLUMN, STATE_COLUMN,
    CACHE_TTL
)

@st.cache_data(ttl=CACHE_TTL, show_spinner="Loading data...")
def load_data(file_path=None):
    """
    Load and cache CSV data with data cleaning

    Args:
        file_path: Path to CSV file (default: from config)

    Returns:
        pd.DataFrame: Cleaned dataframe with additional computed columns
    """
    if file_path is None:
        file_path = CSV_PATH

    try:
        # Load CSV
        df = pd.read_csv(file_path, encoding=CSV_ENCODING)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Data type conversions
        df[AMOUNT_COLUMN] = pd.to_numeric(df[AMOUNT_COLUMN], errors='coerce')
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')

        # Handle supplier location columns
        # New format: SupplierCity and SupplierState are separate columns
        # Legacy format: Extract from 'Supplier City/State' if new columns don't exist
        if 'SupplierState' not in df.columns and 'Supplier City/State' in df.columns:
            # Legacy support: Extract from combined column
            df['SupplierState'] = df['Supplier City/State'].str.split(',').str[-1].str.strip()
            df['SupplierCity'] = df['Supplier City/State'].str.split(',').str[0].str.strip()

        # Clean and standardize state codes
        if 'SupplierState' in df.columns:
            df['SupplierState'] = df['SupplierState'].str.strip().str.upper()

        # Clean city names
        if 'SupplierCity' in df.columns:
            df['SupplierCity'] = df['SupplierCity'].str.strip()

        # Ensure columns exist even if data is missing
        if 'SupplierState' not in df.columns:
            df['SupplierState'] = None
        if 'SupplierCity' not in df.columns:
            df['SupplierCity'] = None

        # Add date components for easier filtering/grouping
        df['Year'] = df[DATE_COLUMN].dt.year
        df['Month'] = df[DATE_COLUMN].dt.month
        df['Quarter'] = df[DATE_COLUMN].dt.quarter
        df['Month_Name'] = df[DATE_COLUMN].dt.strftime('%B %Y')
        df['Year_Month'] = df[DATE_COLUMN].dt.to_period('M')
        df['Year_Quarter'] = df[DATE_COLUMN].dt.to_period('Q')

        # Add fiscal year (assuming Jan-Dec)
        df['Fiscal_Year'] = df['Year']

        # Remove rows with null amounts (can't analyze spending without amount)
        df = df.dropna(subset=[AMOUNT_COLUMN])

        # Remove rows with null dates
        df = df.dropna(subset=[DATE_COLUMN])

        return df

    except FileNotFoundError:
        st.error(f"❌ Data file not found: {file_path}")
        st.info("Please ensure PO_Data.csv is in the correct location or upload a file.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL)
def get_data_summary(df):
    """
    Calculate high-level data summary statistics

    Args:
        df: DataFrame to summarize

    Returns:
        dict: Summary statistics
    """
    if df.empty:
        return {
            'total_spend': 0,
            'total_records': 0,
            'unique_pos': 0,
            'unique_suppliers': 0,
            'unique_states': 0,
            'unique_cities': 0,
            'date_min': None,
            'date_max': None,
            'categories': 0,
            'subcategories': 0
        }

    return {
        'total_spend': df[AMOUNT_COLUMN].sum(),
        'total_records': len(df),
        'unique_pos': df['VSTX PO #'].nunique() if 'VSTX PO #' in df.columns else 0,
        'unique_suppliers': df[SUPPLIER_COLUMN].nunique(),
        'unique_states': df[STATE_COLUMN].nunique() if STATE_COLUMN in df.columns else 0,
        'unique_cities': df['SupplierCity'].nunique() if 'SupplierCity' in df.columns else 0,
        'date_min': df[DATE_COLUMN].min(),
        'date_max': df[DATE_COLUMN].max(),
        'categories': df['Category'].nunique() if 'Category' in df.columns else 0,
        'subcategories': df['SubCategory'].nunique() if 'SubCategory' in df.columns else 0
    }


def filter_data(df, date_range=None, categories=None, states=None, suppliers=None,
                subcategories=None, po_status=None, cities=None):
    """
    Apply filters to dataframe

    Args:
        df: DataFrame to filter
        date_range: Tuple of (start_date, end_date)
        categories: List of categories to include
        states: List of states to include
        suppliers: List of suppliers to include
        subcategories: List of subcategories to include
        po_status: List of PO statuses to include
        cities: List of supplier cities to include

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()

    # Date range filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df[DATE_COLUMN] >= pd.Timestamp(start_date)) &
            (filtered_df[DATE_COLUMN] <= pd.Timestamp(end_date))
        ]

    # Category filter
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]

    # Subcategory filter
    if subcategories and len(subcategories) > 0:
        filtered_df = filtered_df[filtered_df['SubCategory'].isin(subcategories)]

    # State filter
    if states and len(states) > 0:
        filtered_df = filtered_df[filtered_df[STATE_COLUMN].isin(states)]

    # City filter
    if cities and len(cities) > 0:
        filtered_df = filtered_df[filtered_df['SupplierCity'].isin(cities)]

    # Supplier filter
    if suppliers and len(suppliers) > 0:
        filtered_df = filtered_df[filtered_df[SUPPLIER_COLUMN].isin(suppliers)]

    # PO Status filter
    if po_status and len(po_status) > 0 and 'PO Status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['PO Status'].isin(po_status)]

    return filtered_df


@st.cache_data
def search_suppliers(df, query):
    """
    Search for suppliers matching query

    Args:
        df: DataFrame to search
        query: Search string

    Returns:
        list: Matching supplier names
    """
    if not query:
        return []

    query_lower = query.lower()
    suppliers = df[SUPPLIER_COLUMN].dropna().unique()
    matches = [s for s in suppliers if query_lower in s.lower()]
    return sorted(matches)


def format_currency(value):
    """Format value as currency"""
    return f"${value:,.0f}"


def format_number(value):
    """Format value as number with commas"""
    return f"{value:,}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.1f}%"
