"""
Geographic Analysis Page
State-by-state supplier and spend analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data, filter_data, format_currency, format_number, format_percentage
from utils.calculations import calculate_spend_by_state, calculate_geographic_metrics
from utils.visualizations import create_state_choropleth, create_state_bar_chart
from config import SUPPLIER_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN

# Page config
st.set_page_config(page_title="Geographic Analysis", page_icon="🗺️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .state-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .insight-box {
        background: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/vtx_logo2.png", width=150)
with col2:
    st.markdown('<h1 class="main-header">🗺️ Geographic Analysis</h1>', unsafe_allow_html=True)
    st.markdown("**Analyze supplier distribution and spending patterns by state**")

# Load data
df = load_data()

# Sidebar - Filters
st.sidebar.header("🔍 Filters")

# Category filter
all_categories = sorted(df[CATEGORY_COLUMN].dropna().unique())
selected_categories = st.sidebar.multiselect("Filter by Category", options=all_categories)

# Date filter
min_date = df['PO Order Date'].min().date()
max_date = df['PO Order Date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = filter_data(
    df,
    date_range=date_range,
    categories=selected_categories if selected_categories else None
)

# Calculate geographic metrics
state_spend = calculate_spend_by_state(filtered_df)
geo_metrics = calculate_geographic_metrics(filtered_df)

# Main content
st.markdown("---")

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🗺️ States Covered", format_number(len(state_spend)))
with col2:
    st.metric("💰 Total Spend", format_currency(state_spend.sum()))
with col3:
    top_state = state_spend.idxmax() if len(state_spend) > 0 else "N/A"
    st.metric("🏆 Top State", top_state)
with col4:
    avg_spend_per_state = state_spend.mean() if len(state_spend) > 0 else 0
    st.metric("📊 Avg Spend/State", format_currency(avg_spend_per_state))

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map View", "📊 State Comparison", "🔍 Multi-State Suppliers", "📈 Regional Insights"])

with tab1:
    st.subheader("Spend Distribution Across USA")

    if len(state_spend) > 0:
        # Choropleth map
        fig_map = create_state_choropleth(state_spend, title="Total Spend by State")
        st.plotly_chart(fig_map, use_container_width=True)

        # Top states bar chart
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### Top 15 States by Spend")
            top_15 = state_spend.nlargest(15)
            fig_bar = create_state_bar_chart(top_15, title="Top 15 States", n=15)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.markdown("#### State Breakdown")
            state_df = pd.DataFrame({
                'State': state_spend.index,
                'Spend': state_spend.values,
                '% of Total': (state_spend.values / state_spend.sum() * 100)
            }).sort_values('Spend', ascending=False)

            state_df['Spend'] = state_df['Spend'].apply(format_currency)
            state_df['% of Total'] = state_df['% of Total'].apply(lambda x: f"{x:.1f}%")

            st.dataframe(state_df.head(15), use_container_width=True, hide_index=True)
    else:
        st.warning("No geographic data available.")

with tab2:
    st.subheader("State-by-State Comparison")

    # State selection for comparison
    states_to_compare = st.multiselect(
        "Select states to compare (2-5 recommended)",
        options=sorted(state_spend.index.tolist()),
        default=state_spend.nlargest(3).index.tolist() if len(state_spend) >= 3 else state_spend.index.tolist()
    )

    if len(states_to_compare) > 0:
        # Filter data for selected states
        comparison_df = filtered_df[filtered_df['Supplier State'].isin(states_to_compare)]

        # Metrics comparison
        st.markdown("#### Key Metrics Comparison")

        comparison_metrics = []
        for state in states_to_compare:
            state_data = comparison_df[comparison_df['Supplier State'] == state]
            comparison_metrics.append({
                'State': state,
                'Total Spend': state_data[AMOUNT_COLUMN].sum(),
                'Suppliers': state_data[SUPPLIER_COLUMN].nunique(),
                'PO Count': len(state_data),
                'Avg PO Value': state_data[AMOUNT_COLUMN].mean(),
                'Categories': state_data[CATEGORY_COLUMN].nunique()
            })

        comparison_df_display = pd.DataFrame(comparison_metrics)

        # Format for display
        formatted_comparison = comparison_df_display.copy()
        formatted_comparison['Total Spend'] = formatted_comparison['Total Spend'].apply(format_currency)
        formatted_comparison['Avg PO Value'] = formatted_comparison['Avg PO Value'].apply(format_currency)

        st.dataframe(formatted_comparison, use_container_width=True, hide_index=True)

        # Visual comparison charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Spend Comparison")
            fig_spend = go.Figure(data=[
                go.Bar(
                    x=comparison_df_display['State'],
                    y=comparison_df_display['Total Spend'],
                    marker_color='#1f77b4',
                    text=comparison_df_display['Total Spend'].apply(format_currency),
                    textposition='auto'
                )
            ])
            fig_spend.update_layout(
                xaxis_title="State",
                yaxis_title="Total Spend ($)",
                height=400
            )
            st.plotly_chart(fig_spend, use_container_width=True)

        with col2:
            st.markdown("#### Supplier Count Comparison")
            fig_suppliers = go.Figure(data=[
                go.Bar(
                    x=comparison_df_display['State'],
                    y=comparison_df_display['Suppliers'],
                    marker_color='#2ca02c',
                    text=comparison_df_display['Suppliers'],
                    textposition='auto'
                )
            ])
            fig_suppliers.update_layout(
                xaxis_title="State",
                yaxis_title="Number of Suppliers",
                height=400
            )
            st.plotly_chart(fig_suppliers, use_container_width=True)

        # Category breakdown by state
        st.markdown("#### Category Breakdown by State")

        category_by_state = comparison_df.groupby(['Supplier State', CATEGORY_COLUMN])[AMOUNT_COLUMN].sum().reset_index()

        fig_category = px.bar(
            category_by_state,
            x='Supplier State',
            y=AMOUNT_COLUMN,
            color=CATEGORY_COLUMN,
            title="Spend by Category and State",
            labels={AMOUNT_COLUMN: "Spend ($)", 'Supplier State': 'State'},
            height=500
        )
        st.plotly_chart(fig_category, use_container_width=True)

    else:
        st.info("👆 Select states to compare their metrics and spending patterns.")

with tab3:
    st.subheader("Multi-State Supplier Analysis")

    st.markdown("""
    <div class="insight-box">
        <strong>💡 Why this matters:</strong> Suppliers operating in multiple states may offer
        opportunities for volume discounts, standardization, and simplified procurement processes.
    </div>
    """, unsafe_allow_html=True)

    # Find suppliers in multiple states
    supplier_states = filtered_df.groupby(SUPPLIER_COLUMN)['Supplier State'].apply(
        lambda x: list(x.dropna().unique())
    ).reset_index()
    supplier_states['State Count'] = supplier_states['Supplier State'].apply(len)

    # Get multi-state suppliers
    multi_state_suppliers = supplier_states[supplier_states['State Count'] > 1].copy()
    multi_state_suppliers['States'] = multi_state_suppliers['Supplier State'].apply(lambda x: ', '.join(sorted(x)))

    # Add spend data
    supplier_spend = filtered_df.groupby(SUPPLIER_COLUMN)[AMOUNT_COLUMN].sum()
    multi_state_suppliers = multi_state_suppliers.merge(
        supplier_spend.rename('Total Spend'),
        left_on=SUPPLIER_COLUMN,
        right_index=True
    )

    multi_state_suppliers = multi_state_suppliers.sort_values('Total Spend', ascending=False)

    if len(multi_state_suppliers) > 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏢 Multi-State Suppliers", format_number(len(multi_state_suppliers)))
        with col2:
            st.metric("💰 Total Spend", format_currency(multi_state_suppliers['Total Spend'].sum()))
        with col3:
            avg_states = multi_state_suppliers['State Count'].mean()
            st.metric("📊 Avg States/Supplier", f"{avg_states:.1f}")

        # Distribution chart
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### Top Multi-State Suppliers")

            top_multi = multi_state_suppliers.head(15)

            fig_multi = go.Figure()
            fig_multi.add_trace(go.Bar(
                x=top_multi['Total Spend'],
                y=top_multi[SUPPLIER_COLUMN],
                orientation='h',
                marker_color='#ff7f0e',
                text=top_multi['Total Spend'].apply(format_currency),
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>' +
                              'Spend: %{text}<br>' +
                              'States: %{customdata[0]}<br>' +
                              '<extra></extra>',
                customdata=top_multi[['State Count']].values
            ))

            fig_multi.update_layout(
                xaxis_title="Total Spend ($)",
                yaxis_title="Supplier",
                height=500
            )

            st.plotly_chart(fig_multi, use_container_width=True)

        with col2:
            st.markdown("#### State Coverage")

            # State count distribution
            state_count_dist = multi_state_suppliers['State Count'].value_counts().sort_index()

            fig_dist = go.Figure(data=[
                go.Bar(
                    x=state_count_dist.index,
                    y=state_count_dist.values,
                    marker_color='#9467bd',
                    text=state_count_dist.values,
                    textposition='auto'
                )
            ])

            fig_dist.update_layout(
                xaxis_title="Number of States",
                yaxis_title="Number of Suppliers",
                height=500
            )

            st.plotly_chart(fig_dist, use_container_width=True)

        # Detailed table
        st.markdown("#### Multi-State Supplier Details")

        display_multi = multi_state_suppliers[[SUPPLIER_COLUMN, 'State Count', 'States', 'Total Spend']].copy()
        display_multi['Total Spend'] = display_multi['Total Spend'].apply(format_currency)

        st.dataframe(display_multi, use_container_width=True, hide_index=True)

        # Download option
        csv = multi_state_suppliers.to_csv(index=False)
        st.download_button(
            label="📥 Download Multi-State Suppliers (CSV)",
            data=csv,
            file_name="multi_state_suppliers.csv",
            mime="text/csv"
        )

    else:
        st.info("No suppliers found operating in multiple states.")

with tab4:
    st.subheader("Regional Insights")

    # Define regions
    regions = {
        'Northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'],
        'Midwest': ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
        'South': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'],
        'West': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
    }

    # Add region column
    def get_region(state):
        for region, states in regions.items():
            if state in states:
                return region
        return 'Other'

    filtered_df['Region'] = filtered_df['Supplier State'].apply(get_region)

    # Regional metrics
    regional_spend = filtered_df.groupby('Region')[AMOUNT_COLUMN].sum().sort_values(ascending=False)
    regional_suppliers = filtered_df.groupby('Region')[SUPPLIER_COLUMN].nunique()
    regional_pos = filtered_df.groupby('Region').size()

    # Create regional summary
    regional_summary = pd.DataFrame({
        'Total Spend': regional_spend,
        'Suppliers': regional_suppliers,
        'PO Count': regional_pos,
        'Avg Spend/Supplier': regional_spend / regional_suppliers
    })

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Regional Spend Distribution")

        fig_region_pie = px.pie(
            regional_summary.reset_index(),
            values='Total Spend',
            names='Region',
            title='Spend by Region',
            hole=0.4
        )
        st.plotly_chart(fig_region_pie, use_container_width=True)

    with col2:
        st.markdown("#### Regional Metrics")

        formatted_regional = regional_summary.copy()
        formatted_regional['Total Spend'] = formatted_regional['Total Spend'].apply(format_currency)
        formatted_regional['Avg Spend/Supplier'] = formatted_regional['Avg Spend/Supplier'].apply(format_currency)

        st.dataframe(formatted_regional, use_container_width=True)

    # Regional comparison bar chart
    st.markdown("#### Regional Comparison")

    fig_regional_bars = go.Figure()

    fig_regional_bars.add_trace(go.Bar(
        name='Total Spend',
        x=regional_summary.index,
        y=regional_summary['Total Spend'],
        text=regional_summary['Total Spend'].apply(format_currency),
        textposition='auto',
        yaxis='y',
        offsetgroup=1
    ))

    fig_regional_bars.add_trace(go.Bar(
        name='Suppliers',
        x=regional_summary.index,
        y=regional_summary['Suppliers'],
        text=regional_summary['Suppliers'],
        textposition='auto',
        yaxis='y2',
        offsetgroup=2
    ))

    fig_regional_bars.update_layout(
        xaxis_title="Region",
        yaxis=dict(title="Total Spend ($)"),
        yaxis2=dict(title="Number of Suppliers", overlaying='y', side='right'),
        barmode='group',
        height=500
    )

    st.plotly_chart(fig_regional_bars, use_container_width=True)

    # Top categories by region
    st.markdown("#### Top Categories by Region")

    for region in regional_summary.index:
        with st.expander(f"📍 {region} Region"):
            region_data = filtered_df[filtered_df['Region'] == region]
            category_spend = region_data.groupby(CATEGORY_COLUMN)[AMOUNT_COLUMN].sum().nlargest(5)

            col1, col2 = st.columns([1, 2])

            with col1:
                category_df = pd.DataFrame({
                    'Category': category_spend.index,
                    'Spend': category_spend.values
                })
                category_df['Spend'] = category_df['Spend'].apply(format_currency)
                st.dataframe(category_df, use_container_width=True, hide_index=True)

            with col2:
                fig_cat = go.Figure(data=[
                    go.Bar(
                        x=category_spend.values,
                        y=category_spend.index,
                        orientation='h',
                        marker_color='#17becf'
                    )
                ])
                fig_cat.update_layout(
                    xaxis_title="Spend ($)",
                    yaxis_title="Category",
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig_cat, use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Use the filters to analyze geographic patterns by category. Check Multi-State Suppliers for consolidation opportunities.")
