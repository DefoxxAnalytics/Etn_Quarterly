"""
Executive Dashboard - High-level KPIs and visualizations
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data, filter_data, get_data_summary, format_currency, format_number, format_percentage
from utils.calculations import (
    calculate_spend_by_period,
    calculate_top_suppliers,
    calculate_spend_by_category,
    calculate_spend_by_state,
    calculate_top_concentration,
    calculate_spend_trend_stats
)
from utils.visualizations import (
    create_spend_trend_chart,
    create_category_pie_chart,
    create_supplier_bar_chart,
    create_state_choropleth,
    create_state_bar_chart,
    create_concentration_chart
)

# Page configuration
st.set_page_config(page_title="Executive Dashboard", page_icon="📊", layout="wide")

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/vtx_logo2.png", width=150)
with col2:
    st.title("📊 Executive Dashboard")
    st.markdown("**High-level insights and key performance indicators**")

st.markdown("---")

# Load data
df = load_data()

if df.empty:
    st.error("❌ No data available. Please check the data source.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
min_date = df['PO Order Date'].min().date()
max_date = df['PO Order Date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter data by purchase order date range"
)

# Category filter
if 'Category' in df.columns:
    all_categories = sorted(df['Category'].dropna().unique())
    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=all_categories,
        default=all_categories,
        help="Select categories to include in analysis"
    )
else:
    selected_categories = []

# Subcategory filter (dependent on category selection)
if 'SubCategory' in df.columns:
    if selected_categories:
        # Filter subcategories based on selected categories
        available_subcategories = sorted(
            df[df['Category'].isin(selected_categories)]['SubCategory'].dropna().unique()
        )
    else:
        # Show all subcategories if no category is selected
        available_subcategories = sorted(df['SubCategory'].dropna().unique())

    selected_subcategories = st.sidebar.multiselect(
        "Subcategories",
        options=available_subcategories,
        default=available_subcategories,
        help="Select subcategories to include in analysis"
    )
else:
    selected_subcategories = []

# State filter
if 'SupplierState' in df.columns:
    all_states = sorted(df['SupplierState'].dropna().unique())
    selected_states = st.sidebar.multiselect(
        "States",
        options=all_states,
        default=all_states,
        help="Select states to include in analysis"
    )
else:
    selected_states = []

# PO Status filter
if 'PO Status' in df.columns:
    all_statuses = sorted(df['PO Status'].dropna().unique())
    selected_statuses = st.sidebar.multiselect(
        "PO Status",
        options=all_statuses,
        default=all_statuses,
        help="Select PO statuses to include"
    )
else:
    selected_statuses = []

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use filters to analyze specific time periods, categories, or regions.")

# Apply filters
filtered_df = filter_data(
    df,
    date_range=date_range,
    categories=selected_categories if selected_categories else None,
    subcategories=selected_subcategories if selected_subcategories else None,
    states=selected_states if selected_states else None,
    po_status=selected_statuses if selected_statuses else None
)

# Check if filtered data is empty
if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
    st.stop()

# Get summary for filtered data
summary = get_data_summary(filtered_df)

# KPI Cards
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Spend",
        value=format_currency(summary['total_spend']),
        help="Total procurement spending for selected period and filters"
    )

with col2:
    st.metric(
        label="🏢 Unique Suppliers",
        value=format_number(summary['unique_suppliers']),
        help="Number of unique suppliers"
    )

with col3:
    st.metric(
        label="🗺️ States Covered",
        value=summary['unique_states'],
        help="Number of states with suppliers"
    )

with col4:
    st.metric(
        label="📋 Purchase Orders",
        value=format_number(summary['unique_pos']),
        help="Total number of purchase orders"
    )

st.markdown("---")

# Row 1: Spend Trend and Category Breakdown
st.subheader("📊 Spend Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Spend Trend Over Time")

    # Period selector
    period_options = {
        'Monthly': 'M',
        'Quarterly': 'Q',
        'Yearly': 'Y'
    }
    selected_period = st.selectbox(
        "Aggregation Period",
        options=list(period_options.keys()),
        index=0,
        key='period_selector'
    )

    # Calculate spend by period
    spend_by_period = calculate_spend_by_period(filtered_df, period=period_options[selected_period])

    if not spend_by_period.empty:
        # Create trend chart
        fig_trend = create_spend_trend_chart(
            spend_by_period,
            title=f"Spend Trend ({selected_period})"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Show trend statistics
        trend_stats = calculate_spend_trend_stats(spend_by_period)
        if trend_stats:
            with st.expander("📈 Trend Statistics"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Average", format_currency(trend_stats['average']))
                    st.metric("Median", format_currency(trend_stats['median']))
                with col_b:
                    st.metric("Min", format_currency(trend_stats['min']))
                    st.metric("Max", format_currency(trend_stats['max']))
                with col_c:
                    st.metric("Trend", trend_stats['trend'].title())
                    st.metric("Change", f"{trend_stats['change_pct']:.1f}%")
    else:
        st.info("No spend data available for the selected period.")

with col2:
    st.markdown("#### Spend by Category")

    # Calculate spend by category
    category_spend = calculate_spend_by_category(filtered_df)

    if not category_spend.empty:
        # Create pie chart
        fig_pie = create_category_pie_chart(category_spend)
        st.plotly_chart(fig_pie, use_container_width=True)

        # Show category table
        with st.expander("📋 Category Details"):
            category_df = pd.DataFrame({
                'Category': category_spend.index,
                'Spend': category_spend.values,
                '% of Total': (category_spend.values / category_spend.sum() * 100)
            })
            category_df['Spend'] = category_df['Spend'].apply(format_currency)
            category_df['% of Total'] = category_df['% of Total'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(category_df, hide_index=True, use_container_width=True)
    else:
        st.info("No category data available.")

st.markdown("---")

# Row 2: Top Suppliers
st.subheader("🏆 Top Suppliers")

# Calculate top suppliers
top_n_input = st.slider("Number of top suppliers to display", min_value=5, max_value=50, value=20, step=5)
top_suppliers = calculate_top_suppliers(filtered_df, n=top_n_input)

if not top_suppliers.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create bar chart
        fig_suppliers = create_supplier_bar_chart(
            top_suppliers,
            title=f"Top {top_n_input} Suppliers by Spend",
            n=top_n_input
        )
        st.plotly_chart(fig_suppliers, use_container_width=True)

    with col2:
        # Calculate concentration
        concentration = calculate_top_concentration(filtered_df, n=top_n_input)

        if concentration:
            st.metric(
                label=f"Top {top_n_input} Concentration",
                value=format_percentage(concentration['concentration_pct']),
                help=f"Percentage of total spend with top {top_n_input} suppliers"
            )

            # Concentration pie chart
            fig_concentration = create_concentration_chart(
                concentration['top_n_spend'],
                concentration['remaining_spend'],
                n=top_n_input
            )
            st.plotly_chart(fig_concentration, use_container_width=True)

        # Top suppliers table
        with st.expander(f"📋 Top {top_n_input} Suppliers List"):
            top_suppliers_df = pd.DataFrame({
                'Rank': range(1, len(top_suppliers) + 1),
                'Supplier': top_suppliers.index,
                'Spend': top_suppliers.values
            })
            top_suppliers_df['Spend'] = top_suppliers_df['Spend'].apply(format_currency)
            st.dataframe(top_suppliers_df, hide_index=True, use_container_width=True)
else:
    st.info("No supplier data available.")

st.markdown("---")

# Row 3: Geographic Distribution
st.subheader("🌎 Geographic Distribution")

# Calculate state spend
state_spend = calculate_spend_by_state(filtered_df)

if not state_spend.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create choropleth map
        fig_map = create_state_choropleth(state_spend)
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        # Top states bar chart
        st.markdown("#### Top 10 States")
        fig_states = create_state_bar_chart(state_spend, n=10)
        st.plotly_chart(fig_states, use_container_width=True)

        # Top states table
        with st.expander("📋 Top 10 States Details"):
            top_states = state_spend.head(10)
            states_df = pd.DataFrame({
                'Rank': range(1, len(top_states) + 1),
                'State': top_states.index,
                'Spend': top_states.values,
                '% of Total': (top_states.values / state_spend.sum() * 100)
            })
            states_df['Spend'] = states_df['Spend'].apply(format_currency)
            states_df['% of Total'] = states_df['% of Total'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(states_df, hide_index=True, use_container_width=True)
else:
    st.info("No geographic data available.")

# Footer
st.markdown("---")
st.caption(f"""
**Executive Dashboard** | Filtered Data: {format_number(summary['total_records'])} records |
Date Range: {summary['date_min'].strftime('%b %d, %Y')} to {summary['date_max'].strftime('%b %d, %Y')}
""")
