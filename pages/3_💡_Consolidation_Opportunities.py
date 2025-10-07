"""
Consolidation Opportunities Page
Identify savings opportunities through supplier consolidation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data, filter_data, format_currency, format_number
from utils.calculations import calculate_consolidation_opportunities
from config import SUPPLIER_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN, MIN_SUPPLIERS_FOR_CONSOLIDATION, MIN_SPEND_FOR_CONSOLIDATION

# Page config
st.set_page_config(page_title="Consolidation Opportunities", page_icon="💡", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .opportunity-card {
        background: #2c5282;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        border-left: 5px solid #4299e1;
    }
    .savings-highlight {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
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
    st.markdown('<h1 class="main-header">💡 Consolidation Opportunities</h1>', unsafe_allow_html=True)
    st.markdown("**Identify potential savings through strategic supplier consolidation**")

# Load data
df = load_data()

# Early data validation
if df.empty:
    st.error("❌ No data available. Please check if the data file is loaded correctly.")
    st.stop()

if 'PO Order Date' not in df.columns:
    st.error("❌ Required columns missing from dataset.")
    st.stop()

# Sidebar - Configuration
st.sidebar.header("⚙️ Configuration")

st.sidebar.markdown("### Consolidation Criteria")
min_suppliers = st.sidebar.number_input(
    "Minimum Suppliers",
    min_value=2,
    max_value=20,
    value=MIN_SUPPLIERS_FOR_CONSOLIDATION,
    help="Minimum number of suppliers in a category to consider consolidation"
)

min_spend = st.sidebar.number_input(
    "Minimum Spend ($)",
    min_value=10000.0,
    max_value=1000000.0,
    value=float(MIN_SPEND_FOR_CONSOLIDATION),
    step=10000.0,
    help="Minimum total spend in a category to consider consolidation"
)

st.sidebar.markdown("### Savings Assumptions")
savings_rate = st.sidebar.slider(
    "Expected Savings Rate (%)",
    min_value=5,
    max_value=30,
    value=10,
    step=5,
    help="Estimated savings from consolidation"
)

# Date filter
st.sidebar.markdown("### Date Range")
min_date = df['PO Order Date'].min().date()
max_date = df['PO Order Date'].max().date()
date_range = st.sidebar.date_input(
    "Filter by Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Category and Subcategory filters
st.sidebar.markdown("### Filters")

# Category filter
all_categories = sorted(df[CATEGORY_COLUMN].dropna().unique()) if CATEGORY_COLUMN in df.columns else []
selected_categories = st.sidebar.multiselect(
    "Filter by Category",
    options=all_categories,
    default=None,
    help="Select one or more categories to filter"
)

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
    default=None,
    help="Select one or more subcategories to filter"
)

# State filter
all_states = sorted(df['SupplierState'].dropna().unique()) if 'SupplierState' in df.columns else []
selected_states = st.sidebar.multiselect("Filter by State", options=all_states)

# City filter (dependent on state selection)
if selected_states:
    available_cities = sorted(
        df[df['SupplierState'].isin(selected_states)]['SupplierCity'].dropna().unique()
    ) if 'SupplierCity' in df.columns else []
else:
    available_cities = sorted(df['SupplierCity'].dropna().unique()) if 'SupplierCity' in df.columns else []

selected_cities = st.sidebar.multiselect("Filter by City", options=available_cities)

# Apply filters
filtered_df = filter_data(
    df,
    date_range=date_range,
    categories=selected_categories if selected_categories else None,
    subcategories=selected_subcategories if selected_subcategories else None,
    states=selected_states if selected_states else None,
    cities=selected_cities if selected_cities else None
)

# Calculate opportunities
opportunities = calculate_consolidation_opportunities(
    filtered_df,
    min_suppliers=min_suppliers,
    min_spend=min_spend
)

# Recalculate savings with custom rate
if len(opportunities) > 0:
    opportunities['Potential Savings'] = opportunities['Total Spend'] * (savings_rate / 100)

# Main content
st.markdown("---")

# Summary metrics
if len(opportunities) > 0:
    total_consolidation_spend = opportunities['Total Spend'].sum()
    total_savings = opportunities['Potential Savings'].sum()
    avg_suppliers_per_category = opportunities['Suppliers'].mean()
    num_opportunities = len(opportunities)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Opportunities Found", format_number(num_opportunities))
    with col2:
        st.metric("💰 Total Addressable Spend", format_currency(total_consolidation_spend))
    with col3:
        st.metric("💵 Potential Savings", format_currency(total_savings))
    with col4:
        st.metric("📊 Avg Suppliers/Category", f"{avg_suppliers_per_category:.1f}")

    # Savings highlight
    st.markdown(f"""
    <div class="savings-highlight">
        <h3>💰 Projected Annual Savings: {format_currency(total_savings)}</h3>
        <p>Based on {savings_rate}% savings rate across {num_opportunities} consolidation opportunities</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("No consolidation opportunities found with current criteria. Try adjusting the filters in the sidebar.")

st.markdown("---")

# Opportunities table and visualizations
if len(opportunities) > 0:
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📋 Detailed List", "🎯 Priority Matrix", "🔬 Deep Dive"])

    with tab1:
        st.subheader("Top Consolidation Opportunities")

        # Top 10 opportunities chart
        top_10 = opportunities.head(10)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_10['Total Spend'],
            y=top_10['SubCategory'],
            orientation='h',
            name='Total Spend',
            marker_color='#1f77b4',
            text=top_10['Total Spend'].apply(lambda x: format_currency(x)),
            textposition='auto'
        ))

        fig.add_trace(go.Bar(
            x=top_10['Potential Savings'],
            y=top_10['SubCategory'],
            orientation='h',
            name='Potential Savings',
            marker_color='#2ca02c',
            text=top_10['Potential Savings'].apply(lambda x: format_currency(x)),
            textposition='auto'
        ))

        fig.update_layout(
            title="Top 10 Consolidation Opportunities by Spend",
            xaxis_title="Amount ($)",
            yaxis_title="Subcategory",
            barmode='group',
            height=500,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Summary by category
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### By Category")
            category_summary = opportunities.groupby(
                opportunities['SubCategory'].apply(lambda x: filtered_df[filtered_df['SubCategory'] == x][CATEGORY_COLUMN].mode()[0] if len(filtered_df[filtered_df['SubCategory'] == x]) > 0 else 'Unknown')
            ).agg({
                'Total Spend': 'sum',
                'Potential Savings': 'sum',
                'Suppliers': 'sum'
            }).sort_values('Potential Savings', ascending=False)

            st.dataframe(
                category_summary.style.format({
                    'Total Spend': lambda x: format_currency(x),
                    'Potential Savings': lambda x: format_currency(x),
                    'Suppliers': lambda x: format_number(x)
                }),
                use_container_width=True
            )

        with col2:
            st.markdown("#### Savings Distribution")
            # Pie chart of savings by category
            category_chart_data = category_summary.reset_index()
            category_chart_data.columns = ['Category', 'Total Spend', 'Potential Savings', 'Suppliers']
            fig_pie = px.pie(
                category_chart_data,
                values='Potential Savings',
                names='Category',
                title='Savings Potential by Category'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.subheader("All Consolidation Opportunities")

        # Prepare display dataframe
        display_df = opportunities.copy()
        display_df['Savings Rate'] = f"{savings_rate}%"
        display_df.reset_index(inplace=True)

        # Format for display
        formatted_df = display_df[[
            'SubCategory', 'Suppliers', 'Total Spend', 'Savings Rate', 'Potential Savings'
        ]].copy()

        formatted_df['Total Spend'] = formatted_df['Total Spend'].apply(format_currency)
        formatted_df['Potential Savings'] = formatted_df['Potential Savings'].apply(format_currency)

        st.dataframe(formatted_df, use_container_width=True, hide_index=True)

        # Download button
        csv = opportunities.to_csv()
        st.download_button(
            label="📥 Download Full Report (CSV)",
            data=csv,
            file_name="consolidation_opportunities.csv",
            mime="text/csv"
        )

    with tab3:
        st.subheader("Priority Matrix: Spend vs Supplier Count")

        # Create scatter plot
        fig_scatter = go.Figure()

        fig_scatter.add_trace(go.Scatter(
            x=opportunities['Suppliers'],
            y=opportunities['Total Spend'],
            mode='markers+text',
            marker=dict(
                size=opportunities['Potential Savings'] / 1000,  # Size by savings
                color=opportunities['Potential Savings'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Savings ($)")
            ),
            text=opportunities['SubCategory'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                          'Suppliers: %{x}<br>' +
                          'Total Spend: $%{y:,.0f}<br>' +
                          '<extra></extra>'
        ))

        fig_scatter.update_layout(
            title="Consolidation Priority Matrix",
            xaxis_title="Number of Suppliers",
            yaxis_title="Total Spend ($)",
            height=600,
            showlegend=False
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("""
        <div class="warning-box">
            <strong>💡 How to Read This Chart:</strong><br>
            • <strong>Top-right quadrant:</strong> High spend + many suppliers = Highest priority<br>
            • <strong>Bubble size:</strong> Larger bubbles = greater savings potential<br>
            • <strong>Color:</strong> Darker colors = higher savings potential
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.subheader("🔬 Deep Dive Analysis")

        # Select a subcategory to analyze
        if len(opportunities) > 0:
            selected_subcategory = st.selectbox(
                "Select Subcategory to Analyze",
                options=opportunities['SubCategory'].tolist(),
                index=0
            )
        else:
            selected_subcategory = None

        if selected_subcategory and len(opportunities) > 0:
            # Filter data for selected subcategory
            subcat_data = filtered_df[filtered_df['SubCategory'] == selected_subcategory]

            # Get metrics
            opp_metrics = opportunities[opportunities['SubCategory'] == selected_subcategory].iloc[0]

            # Display opportunity card
            st.markdown(f"""
            <div class="opportunity-card">
                <h2>{selected_subcategory}</h2>
                <p><strong>Total Spend:</strong> {format_currency(opp_metrics['Total Spend'])}</p>
                <p><strong>Number of Suppliers:</strong> {format_number(opp_metrics['Suppliers'])}</p>
                <p><strong>Potential Savings ({savings_rate}%):</strong> {format_currency(opp_metrics['Potential Savings'])}</p>
            </div>
            """, unsafe_allow_html=True)

            # Supplier breakdown
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Supplier Breakdown")
                supplier_spend = subcat_data.groupby(SUPPLIER_COLUMN)[AMOUNT_COLUMN].agg([
                    ('Total Spend', 'sum'),
                    ('PO Count', 'count')
                ]).sort_values('Total Spend', ascending=False)

                supplier_spend['% of Total'] = (supplier_spend['Total Spend'] / supplier_spend['Total Spend'].sum() * 100).round(1)

                if len(supplier_spend) > 0:
                    # Format for display
                    display_suppliers = supplier_spend.copy()
                    display_suppliers['Total Spend'] = display_suppliers['Total Spend'].apply(format_currency)
                    display_suppliers['% of Total'] = display_suppliers['% of Total'].astype(str) + '%'

                    st.dataframe(display_suppliers, use_container_width=True)
                else:
                    st.info("No supplier data available for this subcategory.")

            with col2:
                st.markdown("#### Spend Distribution")
                if len(supplier_spend) > 0:
                    # Create pie chart with original numeric values
                    supplier_spend_chart = supplier_spend.reset_index()
                    fig_suppliers = px.pie(
                        supplier_spend_chart,
                        values='Total Spend',
                        names=SUPPLIER_COLUMN,
                        title=f'Supplier Spend - {selected_subcategory}'
                    )
                    fig_suppliers.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_suppliers, use_container_width=True)
                else:
                    st.info("No spend data available to visualize.")

            # Consolidation scenario builder
            st.markdown("---")
            st.markdown("#### 🎯 Consolidation Scenario Builder")

            col1, col2, col3 = st.columns(3)

            with col1:
                target_suppliers = st.number_input(
                    "Target Number of Suppliers",
                    min_value=1,
                    max_value=int(opp_metrics['Suppliers']),
                    value=max(1, int(opp_metrics['Suppliers'] * 0.3)),
                    help="How many suppliers do you want to consolidate to?"
                )

            with col2:
                custom_savings_rate = st.number_input(
                    "Custom Savings Rate (%)",
                    min_value=5,
                    max_value=30,
                    value=savings_rate,
                    step=1
                )

            with col3:
                implementation_cost_pct = st.number_input(
                    "Implementation Cost (%)",
                    min_value=0,
                    max_value=10,
                    value=2,
                    step=1,
                    help="One-time cost of consolidation as % of spend"
                )

            # Calculate scenario
            suppliers_reduced = opp_metrics['Suppliers'] - target_suppliers
            reduction_pct = (suppliers_reduced / opp_metrics['Suppliers'] * 100)
            gross_savings = opp_metrics['Total Spend'] * (custom_savings_rate / 100)
            implementation_cost = opp_metrics['Total Spend'] * (implementation_cost_pct / 100)
            net_savings = gross_savings - implementation_cost
            roi = (net_savings / implementation_cost * 100) if implementation_cost > 0 else 0

            st.markdown("##### 📊 Scenario Results")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Suppliers Reduced", f"{format_number(suppliers_reduced)} ({reduction_pct:.0f}%)")
            with col2:
                st.metric("Gross Annual Savings", format_currency(gross_savings))
            with col3:
                st.metric("Implementation Cost", format_currency(implementation_cost))
            with col4:
                st.metric("Net Savings (Year 1)", format_currency(net_savings))

            st.metric("ROI", f"{roi:.0f}%")

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Adjust the consolidation criteria in the sidebar to find different opportunities. Use the Deep Dive tab to create custom consolidation scenarios.")
