"""
Supplier Explorer Page
Interactive search and detailed supplier profiles
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data, filter_data, search_suppliers, format_currency, format_number
from utils.calculations import calculate_supplier_metrics, calculate_spend_by_period
from utils.visualizations import create_spend_trend_chart, create_category_pie_chart
from config import SUPPLIER_COLUMN, AMOUNT_COLUMN, DATE_COLUMN, CATEGORY_COLUMN

# Page config
st.set_page_config(page_title="Supplier Explorer", page_icon="🔍", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .supplier-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/vtx_logo2.png", width=150)
with col2:
    st.markdown('<h1 class="main-header">🔍 Supplier Explorer</h1>', unsafe_allow_html=True)
    st.markdown("**Search, analyze, and compare supplier performance**")

# Load data
df = load_data()

# Early data validation
if df.empty:
    st.error("❌ No data available. Please check if the data file is loaded correctly.")
    st.stop()

# Sidebar - Search and Filters
st.sidebar.header("🔍 Search & Filters")

# Search suppliers
search_term = st.sidebar.text_input("Search Suppliers", placeholder="Enter supplier name...")
if search_term:
    matching_suppliers = search_suppliers(df, search_term)
    st.sidebar.info(f"Found {len(matching_suppliers)} matching suppliers")
else:
    matching_suppliers = df[SUPPLIER_COLUMN].dropna().unique()

# Filter by categories
all_categories = sorted(df[CATEGORY_COLUMN].dropna().unique())
selected_categories = st.sidebar.multiselect("Filter by Category", options=all_categories)

# Subcategory filter (dependent on category selection)
if selected_categories:
    # Filter subcategories based on selected categories
    available_subcategories = sorted(
        df[df[CATEGORY_COLUMN].isin(selected_categories)]['SubCategory'].dropna().unique()
    ) if 'SubCategory' in df.columns else []
else:
    # Show all subcategories if no category is selected
    available_subcategories = sorted(df['SubCategory'].dropna().unique()) if 'SubCategory' in df.columns else []

selected_subcategories = st.sidebar.multiselect(
    "Filter by Subcategory",
    options=available_subcategories,
    help="Select subcategories to filter"
)

# Filter by states
all_states = sorted(df['SupplierState'].dropna().unique())
selected_states = st.sidebar.multiselect("Filter by State", options=all_states)

# City filter (dependent on state selection)
if selected_states:
    available_cities = sorted(
        df[df['SupplierState'].isin(selected_states)]['SupplierCity'].dropna().unique()
    ) if 'SupplierCity' in df.columns else []
else:
    available_cities = sorted(df['SupplierCity'].dropna().unique()) if 'SupplierCity' in df.columns else []

selected_cities = st.sidebar.multiselect("Filter by City", options=available_cities)

# Date range filter
min_date = df[DATE_COLUMN].min().date()
max_date = df[DATE_COLUMN].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters to get supplier list
filtered_df = filter_data(
    df,
    date_range=date_range,
    categories=selected_categories if selected_categories else None,
    subcategories=selected_subcategories if selected_subcategories else None,
    states=selected_states if selected_states else None,
    cities=selected_cities if selected_cities else None
)

# Filter suppliers based on search
if search_term:
    filtered_df = filtered_df[filtered_df[SUPPLIER_COLUMN].isin(matching_suppliers)]

# Get supplier metrics
supplier_metrics = calculate_supplier_metrics(filtered_df)

# Sort options
sort_by = st.sidebar.selectbox(
    "Sort By",
    options=['Total Spend', 'Number of POs', 'Avg PO Value', 'Categories Served'],
    index=0
)

sort_mapping = {
    'Total Spend': 'total_spend',
    'Number of POs': 'po_count',
    'Avg PO Value': 'avg_po_value',
    'Categories Served': 'category_count'
}

supplier_metrics = supplier_metrics.sort_values(sort_mapping[sort_by], ascending=False)

# Main content
st.markdown("---")

# Summary stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Suppliers Found", format_number(len(supplier_metrics)))
with col2:
    st.metric("💰 Total Spend", format_currency(supplier_metrics['total_spend'].sum()))
with col3:
    st.metric("📝 Total POs", format_number(supplier_metrics['po_count'].sum()))
with col4:
    avg_spend = supplier_metrics['total_spend'].mean()
    st.metric("📈 Avg Spend/Supplier", format_currency(avg_spend))

st.markdown("---")

# Two-column layout
col_list, col_detail = st.columns([1, 2])

with col_list:
    st.subheader("📋 Supplier List")

    # Display supplier list with selection
    if len(supplier_metrics) > 0:
        # Create clickable supplier list
        supplier_names = supplier_metrics.index.tolist()

        # Pagination
        items_per_page = 20
        total_pages = (len(supplier_names) + items_per_page - 1) // items_per_page
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(supplier_names))

        st.caption(f"Showing {start_idx + 1}-{end_idx} of {len(supplier_names)} suppliers")

        # Display suppliers as radio buttons for selection
        selected_supplier = st.radio(
            "Select a supplier to view details:",
            options=supplier_names[start_idx:end_idx],
            label_visibility="collapsed"
        )
    else:
        st.warning("No suppliers found matching your criteria.")
        selected_supplier = None

with col_detail:
    st.subheader("📊 Supplier Details")

    if selected_supplier:
        # Get supplier data
        supplier_data = filtered_df[filtered_df[SUPPLIER_COLUMN] == selected_supplier]
        metrics = supplier_metrics.loc[selected_supplier]

        # Supplier card header
        st.markdown(f"""
        <div class="supplier-card">
            <h2>{selected_supplier}</h2>
            <p><strong>Primary State:</strong> {supplier_data['SupplierState'].mode()[0] if len(supplier_data['SupplierState'].mode()) > 0 else 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Spend", format_currency(metrics['total_spend']))
        with col2:
            st.metric("📝 Purchase Orders", format_number(metrics['po_count']))
        with col3:
            st.metric("📊 Avg PO Value", format_currency(metrics['avg_po_value']))
        with col4:
            st.metric("🏷️ Categories", format_number(metrics['category_count']))

        # Tabs for detailed analysis
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Spend Trend", "🏷️ Categories", "📍 Locations", "📋 Recent Orders"])

        with tab1:
            st.markdown("#### Spending Over Time")
            spend_by_month = calculate_spend_by_period(supplier_data, period='M')
            if len(spend_by_month) > 0:
                fig = create_spend_trend_chart(
                    spend_by_month,
                    title=f"Monthly Spend - {selected_supplier}"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Trend insights
                total_months = len(spend_by_month)
                avg_monthly = spend_by_month.mean()
                max_month = spend_by_month.idxmax()
                max_amount = spend_by_month.max()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📅 Active Months", format_number(total_months))
                with col2:
                    st.metric("📊 Avg Monthly Spend", format_currency(avg_monthly))
                with col3:
                    st.metric("📈 Peak Month", f"{max_month.strftime('%b %Y')}")
            else:
                st.info("No spend data available for trend analysis.")

        with tab2:
            st.markdown("#### Category Breakdown")
            category_spend = supplier_data.groupby(CATEGORY_COLUMN)[AMOUNT_COLUMN].sum().sort_values(ascending=False)

            if len(category_spend) > 0:
                fig = create_category_pie_chart(category_spend, title=f"Categories - {selected_supplier}")
                st.plotly_chart(fig, use_container_width=True)

                # Category table
                category_df = pd.DataFrame({
                    'Category': category_spend.index,
                    'Spend': category_spend.values,
                    '% of Total': (category_spend.values / category_spend.sum() * 100).round(1)
                })
                category_df['Spend'] = category_df['Spend'].apply(format_currency)
                category_df['% of Total'] = category_df['% of Total'].astype(str) + '%'
                st.dataframe(category_df, use_container_width=True, hide_index=True)
            else:
                st.info("No category data available.")

        with tab3:
            st.markdown("#### Geographic Distribution")
            state_spend = supplier_data.groupby('SupplierState')[AMOUNT_COLUMN].sum().sort_values(ascending=False)

            if len(state_spend) > 0:
                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=state_spend.values,
                        y=state_spend.index,
                        orientation='h',
                        marker_color='#1f77b4'
                    )
                ])
                fig.update_layout(
                    title=f"Spend by State - {selected_supplier}",
                    xaxis_title="Total Spend ($)",
                    yaxis_title="State",
                    height=max(300, len(state_spend) * 30)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No location data available.")

        with tab4:
            st.markdown("#### Recent Purchase Orders")

            # Show recent orders
            recent_orders = supplier_data.nlargest(20, DATE_COLUMN)[[
                DATE_COLUMN, 'VSTX PO #', CATEGORY_COLUMN, 'SubCategory', AMOUNT_COLUMN
            ]].copy()

            if len(recent_orders) > 0:
                recent_orders[DATE_COLUMN] = recent_orders[DATE_COLUMN].dt.strftime('%Y-%m-%d')
                recent_orders[AMOUNT_COLUMN] = recent_orders[AMOUNT_COLUMN].apply(format_currency)
                recent_orders.columns = ['Date', 'PO Number', 'Category', 'Subcategory', 'Amount']

                st.dataframe(recent_orders, use_container_width=True, hide_index=True)
            else:
                st.info("No order data available.")
    else:
        st.info("👈 Select a supplier from the list to view detailed information.")

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Use the search and filters in the sidebar to narrow down suppliers. Click on any supplier to see detailed analytics.")
