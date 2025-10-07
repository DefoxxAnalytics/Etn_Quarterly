"""
Category Deep Dive Page
Detailed analysis of spending categories and subcategories
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data, filter_data, format_currency, format_number, format_percentage
from utils.calculations import (
    calculate_spend_by_category,
    calculate_spend_by_subcategory,
    calculate_category_metrics,
    calculate_spend_by_period
)
from utils.visualizations import create_category_pie_chart, create_spend_trend_chart
from config import SUPPLIER_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN, DATE_COLUMN

# Page config
st.set_page_config(page_title="Category Deep Dive", page_icon="🏷️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .category-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .subcategory-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17becf;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/vtx_logo2.png", width=150)
with col2:
    st.markdown('<h1 class="main-header">🏷️ Category Deep Dive</h1>', unsafe_allow_html=True)
    st.markdown("**Explore spending patterns across categories and subcategories**")

# Load data
df = load_data()

# Early data validation
if df.empty:
    st.error("❌ No data available. Please check if the data file is loaded correctly.")
    st.stop()

if DATE_COLUMN not in df.columns or 'Supplier State' not in df.columns:
    st.error("❌ Required columns missing from dataset.")
    st.stop()

# Sidebar - Filters
st.sidebar.header("🔍 Filters")

# Date filter
min_date = df[DATE_COLUMN].min().date()
max_date = df[DATE_COLUMN].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# State filter
all_states = sorted(df['Supplier State'].dropna().unique())
selected_states = st.sidebar.multiselect("Filter by State", options=all_states)

# Apply filters
filtered_df = filter_data(
    df,
    date_range=date_range,
    states=selected_states if selected_states else None
)

# Calculate category metrics
category_spend = calculate_spend_by_category(filtered_df)
category_metrics = calculate_category_metrics(filtered_df)

# Main content
st.markdown("---")

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏷️ Total Categories", format_number(len(category_spend)))
with col2:
    st.metric("💰 Total Spend", format_currency(category_spend.sum()))
with col3:
    top_category = category_spend.idxmax() if len(category_spend) > 0 else "N/A"
    st.metric("🏆 Top Category", top_category)
with col4:
    avg_spend = category_spend.mean() if len(category_spend) > 0 else 0
    st.metric("📊 Avg Spend/Category", format_currency(avg_spend))

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Category Explorer", "📈 Trend Analysis", "🎯 Supplier Capability Matrix"])

with tab1:
    st.subheader("Category Spending Overview")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Pie chart
        fig_pie = create_category_pie_chart(category_spend, title="Spend by Category")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Category table
        st.markdown("#### Category Breakdown")
        category_df = pd.DataFrame({
            'Category': category_spend.index,
            'Spend': category_spend.values,
            '% of Total': (category_spend.values / category_spend.sum() * 100)
        })
        category_df['Spend'] = category_df['Spend'].apply(format_currency)
        category_df['% of Total'] = category_df['% of Total'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(category_df, use_container_width=True, hide_index=True)

    # Category metrics comparison
    st.markdown("---")
    st.markdown("#### Category Metrics Comparison")

    if len(category_metrics) > 0:
        # Format for display
        display_metrics = category_metrics.copy()
        display_metrics['total_spend'] = display_metrics['total_spend'].apply(format_currency)
        display_metrics['avg_po_value'] = display_metrics['avg_po_value'].apply(format_currency)

        display_metrics.columns = ['Total Spend', 'PO Count', 'Avg PO Value', 'Suppliers', 'Subcategories']

        st.dataframe(display_metrics, use_container_width=True)

        # Visualization - Suppliers vs Spend
        st.markdown("#### Supplier Concentration by Category")

        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=category_metrics['supplier_count'],
            y=category_metrics['total_spend'],
            mode='markers+text',
            marker=dict(
                size=category_metrics['po_count'] / 10,
                color=category_metrics['total_spend'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Spend ($)")
            ),
            text=category_metrics.index,
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                          'Suppliers: %{x}<br>' +
                          'Spend: $%{y:,.0f}<br>' +
                          '<extra></extra>'
        ))

        fig_scatter.update_layout(
            title="Supplier Count vs Total Spend by Category",
            xaxis_title="Number of Suppliers",
            yaxis_title="Total Spend ($)",
            height=500
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("🔍 Category Explorer")

    # Select category
    selected_category = st.selectbox(
        "Select a category to explore",
        options=category_spend.index.tolist()
    )

    if selected_category:
        # Filter data for selected category
        category_data = filtered_df[filtered_df[CATEGORY_COLUMN] == selected_category]

        # Get metrics
        cat_metrics = category_metrics.loc[selected_category]

        # Category header card
        st.markdown(f"""
        <div class="category-card">
            <h2>{selected_category}</h2>
            <p><strong>Total Spend:</strong> {format_currency(cat_metrics['total_spend'])}</p>
            <p><strong>Suppliers:</strong> {format_number(cat_metrics['supplier_count'])} |
               <strong>POs:</strong> {format_number(cat_metrics['po_count'])} |
               <strong>Subcategories:</strong> {format_number(cat_metrics['subcategory_count'])}</p>
        </div>
        """, unsafe_allow_html=True)

        # Subcategory analysis
        st.markdown("#### Subcategory Breakdown")

        subcategory_spend = category_data.groupby('SubCategory')[AMOUNT_COLUMN].sum().sort_values(ascending=False)

        if len(subcategory_spend) > 0:
            col1, col2 = st.columns([2, 1])

            with col1:
                # Treemap of subcategories
                subcat_df = pd.DataFrame({
                    'SubCategory': subcategory_spend.index,
                    'Spend': subcategory_spend.values
                })

                fig_treemap = px.treemap(
                    subcat_df,
                    path=['SubCategory'],
                    values='Spend',
                    title=f'Subcategories in {selected_category}',
                    height=500
                )
                st.plotly_chart(fig_treemap, use_container_width=True)

            with col2:
                # Subcategory table
                subcat_display = pd.DataFrame({
                    'Subcategory': subcategory_spend.index,
                    'Spend': subcategory_spend.values,
                    '% of Category': (subcategory_spend.values / subcategory_spend.sum() * 100)
                })
                subcat_display['Spend'] = subcat_display['Spend'].apply(format_currency)
                subcat_display['% of Category'] = subcat_display['% of Category'].apply(lambda x: f"{x:.1f}%")

                st.dataframe(subcat_display, use_container_width=True, hide_index=True)

        # Top suppliers in category
        st.markdown("---")
        st.markdown("#### Top Suppliers in this Category")

        supplier_spend = category_data.groupby(SUPPLIER_COLUMN)[AMOUNT_COLUMN].agg([
            ('Total Spend', 'sum'),
            ('PO Count', 'count'),
            ('Avg PO', 'mean')
        ]).sort_values('Total Spend', ascending=False).head(15)

        if len(supplier_spend) > 0:
            col1, col2 = st.columns([2, 1])

            with col1:
                fig_suppliers = go.Figure(data=[
                    go.Bar(
                        x=supplier_spend['Total Spend'],
                        y=supplier_spend.index,
                        orientation='h',
                        marker_color='#2ca02c',
                        text=supplier_spend['Total Spend'].apply(format_currency),
                        textposition='auto'
                    )
                ])
                fig_suppliers.update_layout(
                    title=f"Top 15 Suppliers - {selected_category}",
                    xaxis_title="Total Spend ($)",
                    yaxis_title="Supplier",
                    height=500
                )
                st.plotly_chart(fig_suppliers, use_container_width=True)

            with col2:
                supplier_display = supplier_spend.copy()
                supplier_display['Total Spend'] = supplier_display['Total Spend'].apply(format_currency)
                supplier_display['Avg PO'] = supplier_display['Avg PO'].apply(format_currency)

                st.dataframe(supplier_display, use_container_width=True)

        # Geographic distribution
        st.markdown("---")
        st.markdown("#### Geographic Distribution")

        state_spend = category_data.groupby('Supplier State')[AMOUNT_COLUMN].sum().sort_values(ascending=False).head(10)

        if len(state_spend) > 0:
            fig_states = go.Figure(data=[
                go.Bar(
                    x=state_spend.index,
                    y=state_spend.values,
                    marker_color='#ff7f0e',
                    text=[format_currency(v) for v in state_spend.values],
                    textposition='auto'
                )
            ])
            fig_states.update_layout(
                title=f"Top 10 States - {selected_category}",
                xaxis_title="State",
                yaxis_title="Total Spend ($)",
                height=400
            )
            st.plotly_chart(fig_states, use_container_width=True)

with tab3:
    st.subheader("📈 Category Trend Analysis")

    # Select categories to compare
    categories_to_compare = st.multiselect(
        "Select categories to compare (1-5 recommended)",
        options=category_spend.index.tolist(),
        default=category_spend.nlargest(3).index.tolist() if len(category_spend) >= 3 else category_spend.index.tolist()[:1]
    )

    if len(categories_to_compare) > 0:
        # Time period selector
        period_option = st.radio(
            "Aggregation Period",
            options=['Monthly', 'Quarterly', 'Yearly'],
            horizontal=True
        )

        period_map = {'Monthly': 'M', 'Quarterly': 'Q', 'Yearly': 'Y'}
        period = period_map[period_option]

        # Create multi-line chart
        fig_trends = go.Figure()

        for category in categories_to_compare:
            cat_data = filtered_df[filtered_df[CATEGORY_COLUMN] == category]
            spend_by_period = calculate_spend_by_period(cat_data, period=period)

            if len(spend_by_period) > 0:
                dates = [pd.Period(p, freq=period).to_timestamp() for p in spend_by_period.index]

                fig_trends.add_trace(go.Scatter(
                    x=dates,
                    y=spend_by_period.values,
                    mode='lines+markers',
                    name=category,
                    line=dict(width=2)
                ))

        fig_trends.update_layout(
            title=f"{period_option} Spend Trends by Category",
            xaxis_title="Date",
            yaxis_title="Spend ($)",
            height=500,
            hovermode='x unified'
        )

        st.plotly_chart(fig_trends, use_container_width=True)

        # Growth analysis
        st.markdown("#### Growth Analysis")

        growth_data = []
        for category in categories_to_compare:
            cat_data = filtered_df[filtered_df[CATEGORY_COLUMN] == category]
            spend_by_period = calculate_spend_by_period(cat_data, period=period)

            if len(spend_by_period) >= 2:
                first_period = spend_by_period.iloc[0]
                last_period = spend_by_period.iloc[-1]
                growth = ((last_period - first_period) / first_period * 100) if first_period > 0 else 0

                growth_data.append({
                    'Category': category,
                    'First Period': first_period,
                    'Last Period': last_period,
                    'Growth %': growth
                })

        if growth_data:
            growth_df = pd.DataFrame(growth_data)
            growth_df['First Period'] = growth_df['First Period'].apply(format_currency)
            growth_df['Last Period'] = growth_df['Last Period'].apply(format_currency)
            growth_df['Growth %'] = growth_df['Growth %'].apply(lambda x: f"{x:+.1f}%")

            st.dataframe(growth_df, use_container_width=True, hide_index=True)

    else:
        st.info("👆 Select at least one category to view trend analysis.")

with tab4:
    st.subheader("🎯 Supplier Capability Matrix")

    st.markdown("""
    This matrix shows which suppliers can provide services across multiple categories,
    helping identify opportunities for consolidation and preferred supplier relationships.
    """)

    # Build capability matrix
    supplier_categories = filtered_df.groupby(SUPPLIER_COLUMN)[CATEGORY_COLUMN].apply(
        lambda x: list(x.unique())
    ).reset_index()
    supplier_categories['Category Count'] = supplier_categories[CATEGORY_COLUMN].apply(len)

    # Filter to suppliers serving multiple categories
    multi_category_suppliers = supplier_categories[supplier_categories['Category Count'] > 1].copy()

    # Add spend
    supplier_spend = filtered_df.groupby(SUPPLIER_COLUMN)[AMOUNT_COLUMN].sum()
    multi_category_suppliers = multi_category_suppliers.merge(
        supplier_spend.rename('Total Spend'),
        left_on=SUPPLIER_COLUMN,
        right_index=True
    )

    multi_category_suppliers = multi_category_suppliers.sort_values('Total Spend', ascending=False)

    if len(multi_category_suppliers) > 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏢 Multi-Category Suppliers", format_number(len(multi_category_suppliers)))
        with col2:
            st.metric("💰 Total Spend", format_currency(multi_category_suppliers['Total Spend'].sum()))
        with col3:
            avg_categories = multi_category_suppliers['Category Count'].mean()
            st.metric("📊 Avg Categories/Supplier", f"{avg_categories:.1f}")

        # Top multi-category suppliers
        st.markdown("#### Top Multi-Category Suppliers")

        top_multi = multi_category_suppliers.head(20)

        # Create heatmap data
        heatmap_data = []
        suppliers_list = top_multi[SUPPLIER_COLUMN].tolist()
        all_categories = sorted(filtered_df[CATEGORY_COLUMN].unique())

        for supplier in suppliers_list:
            supplier_row = []
            supplier_data = filtered_df[filtered_df[SUPPLIER_COLUMN] == supplier]

            for category in all_categories:
                spend = supplier_data[supplier_data[CATEGORY_COLUMN] == category][AMOUNT_COLUMN].sum()
                supplier_row.append(spend)

            heatmap_data.append(supplier_row)

        # Create heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=all_categories,
            y=suppliers_list,
            colorscale='Blues',
            text=[[format_currency(val) if val > 0 else '' for val in row] for row in heatmap_data],
            texttemplate='%{text}',
            textfont={"size": 8},
            hovertemplate='Supplier: %{y}<br>Category: %{x}<br>Spend: $%{z:,.0f}<extra></extra>'
        ))

        fig_heatmap.update_layout(
            title="Supplier Capability Heatmap (Top 20 Suppliers)",
            xaxis_title="Category",
            yaxis_title="Supplier",
            height=max(600, len(suppliers_list) * 30)
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Detailed table
        st.markdown("#### Multi-Category Supplier Details")

        multi_category_suppliers['Categories'] = multi_category_suppliers[CATEGORY_COLUMN].apply(
            lambda x: ', '.join(sorted(x))
        )

        display_multi = multi_category_suppliers[[SUPPLIER_COLUMN, 'Category Count', 'Categories', 'Total Spend']].copy()
        display_multi['Total Spend'] = display_multi['Total Spend'].apply(format_currency)

        st.dataframe(display_multi, use_container_width=True, hide_index=True)

        # Download
        csv = multi_category_suppliers.to_csv(index=False)
        st.download_button(
            label="📥 Download Capability Matrix (CSV)",
            data=csv,
            file_name="supplier_capability_matrix.csv",
            mime="text/csv"
        )

    else:
        st.info("No suppliers found serving multiple categories.")

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Use the Category Explorer to dive deep into specific categories. Check the Capability Matrix to find suppliers serving multiple categories.")
