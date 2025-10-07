"""
Custom Reports & Export Page
Generate custom reports and export data in various formats
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
from utils.data_loader import load_data, filter_data, format_currency, format_number
from utils.calculations import (
    calculate_spend_by_category,
    calculate_top_suppliers,
    calculate_spend_by_state,
    calculate_consolidation_opportunities,
    calculate_supplier_metrics,
    calculate_category_metrics
)
from config import SUPPLIER_COLUMN, AMOUNT_COLUMN, CATEGORY_COLUMN, DATE_COLUMN

# Page config
st.set_page_config(page_title="Custom Reports", page_icon="📄", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .report-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .export-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
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
    st.markdown('<h1 class="main-header">📄 Custom Reports & Export</h1>', unsafe_allow_html=True)
    st.markdown("**Generate custom reports and export data for further analysis**")

# Load data
df = load_data()

# Sidebar - Report Configuration
st.sidebar.header("📋 Report Configuration")

# Report type
report_type = st.sidebar.selectbox(
    "Select Report Type",
    options=[
        "Executive Summary",
        "Supplier Analysis",
        "Category Analysis",
        "Geographic Analysis",
        "Consolidation Opportunities",
        "Custom Query"
    ]
)

# Date range
st.sidebar.markdown("### Date Range")
min_date = df[DATE_COLUMN].min().date()
max_date = df[DATE_COLUMN].max().date()
date_range = st.sidebar.date_input(
    "Report Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filters
st.sidebar.markdown("### Filters")

selected_categories = st.sidebar.multiselect(
    "Categories",
    options=sorted(df[CATEGORY_COLUMN].dropna().unique())
)

selected_states = st.sidebar.multiselect(
    "States",
    options=sorted(df['Supplier State'].dropna().unique())
)

selected_suppliers = st.sidebar.multiselect(
    "Suppliers",
    options=sorted(df[SUPPLIER_COLUMN].dropna().unique())
)

# Apply filters
filtered_df = filter_data(
    df,
    date_range=date_range,
    categories=selected_categories if selected_categories else None,
    states=selected_states if selected_states else None,
    suppliers=selected_suppliers if selected_suppliers else None
)

# Export format
st.sidebar.markdown("### Export Options")
export_format = st.sidebar.radio(
    "Export Format",
    options=["Excel (.xlsx)", "CSV (.csv)"]
)

# Main content
st.markdown("---")

# Report preview
st.subheader(f"📊 {report_type} Report Preview")

# Display filters applied
if selected_categories or selected_states or selected_suppliers:
    st.markdown("**Filters Applied:**")
    if selected_categories:
        st.markdown(f"- **Categories:** {', '.join(selected_categories)}")
    if selected_states:
        st.markdown(f"- **States:** {', '.join(selected_states)}")
    if selected_suppliers:
        st.markdown(f"- **Suppliers:** {', '.join(selected_suppliers)}")

st.markdown(f"**Period:** {date_range[0]} to {date_range[1]}")
st.markdown("---")

# Generate report based on type
report_data = {}

if report_type == "Executive Summary":
    st.markdown("### Executive Summary Report")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_spend = filtered_df[AMOUNT_COLUMN].sum()
        st.metric("💰 Total Spend", format_currency(total_spend))
    with col2:
        num_suppliers = filtered_df[SUPPLIER_COLUMN].nunique()
        st.metric("🏢 Suppliers", format_number(num_suppliers))
    with col3:
        num_pos = len(filtered_df)
        st.metric("📝 Purchase Orders", format_number(num_pos))
    with col4:
        avg_po = filtered_df[AMOUNT_COLUMN].mean()
        st.metric("📊 Avg PO Value", format_currency(avg_po))

    # Top 10 suppliers
    st.markdown("#### Top 10 Suppliers by Spend")
    top_suppliers = calculate_top_suppliers(filtered_df, n=10)
    top_suppliers_df = pd.DataFrame({
        'Supplier': top_suppliers.index,
        'Total Spend': top_suppliers.values,
        '% of Total': (top_suppliers.values / total_spend * 100)
    })
    top_suppliers_df['Total Spend'] = top_suppliers_df['Total Spend'].apply(format_currency)
    top_suppliers_df['% of Total'] = top_suppliers_df['% of Total'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(top_suppliers_df, use_container_width=True, hide_index=True)

    # Category breakdown
    st.markdown("#### Spend by Category")
    category_spend = calculate_spend_by_category(filtered_df)
    category_df = pd.DataFrame({
        'Category': category_spend.index,
        'Total Spend': category_spend.values,
        '% of Total': (category_spend.values / total_spend * 100)
    })
    category_df['Total Spend'] = category_df['Total Spend'].apply(format_currency)
    category_df['% of Total'] = category_df['% of Total'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(category_df, use_container_width=True, hide_index=True)

    # Prepare export data
    report_data['Summary Metrics'] = pd.DataFrame({
        'Metric': ['Total Spend', 'Suppliers', 'Purchase Orders', 'Avg PO Value'],
        'Value': [total_spend, num_suppliers, num_pos, avg_po]
    })
    report_data['Top 10 Suppliers'] = top_suppliers.reset_index()
    report_data['Category Breakdown'] = category_spend.reset_index()

elif report_type == "Supplier Analysis":
    st.markdown("### Supplier Analysis Report")

    supplier_metrics = calculate_supplier_metrics(filtered_df)

    st.markdown("#### Supplier Performance Metrics")
    display_metrics = supplier_metrics.head(50).copy()
    display_metrics['total_spend'] = display_metrics['total_spend'].apply(format_currency)
    display_metrics['avg_po_value'] = display_metrics['avg_po_value'].apply(format_currency)
    display_metrics.columns = ['Total Spend', 'PO Count', 'Avg PO Value', 'Category Count']

    st.dataframe(display_metrics, use_container_width=True)

    # Export data
    report_data['Supplier Metrics'] = supplier_metrics.reset_index()

    # Supplier distribution by spend range
    st.markdown("#### Supplier Distribution by Spend Range")
    spend_ranges = pd.cut(
        supplier_metrics['total_spend'],
        bins=[0, 10000, 50000, 100000, 500000, float('inf')],
        labels=['<$10K', '$10K-$50K', '$50K-$100K', '$100K-$500K', '>$500K']
    )
    spend_dist = spend_ranges.value_counts().sort_index()

    spend_dist_df = pd.DataFrame({
        'Spend Range': spend_dist.index,
        'Number of Suppliers': spend_dist.values
    })
    st.dataframe(spend_dist_df, use_container_width=True, hide_index=True)

    report_data['Spend Distribution'] = spend_dist_df

elif report_type == "Category Analysis":
    st.markdown("### Category Analysis Report")

    category_metrics = calculate_category_metrics(filtered_df)

    st.markdown("#### Category Performance Metrics")
    display_metrics = category_metrics.copy()
    display_metrics['total_spend'] = display_metrics['total_spend'].apply(format_currency)
    display_metrics['avg_po_value'] = display_metrics['avg_po_value'].apply(format_currency)
    display_metrics.columns = ['Total Spend', 'PO Count', 'Avg PO Value', 'Suppliers', 'Subcategories']

    st.dataframe(display_metrics, use_container_width=True)

    # Export data
    report_data['Category Metrics'] = category_metrics.reset_index()

    # Subcategory breakdown for top categories
    st.markdown("#### Top Categories - Subcategory Breakdown")

    top_3_categories = category_metrics.nlargest(3, 'total_spend').index

    for category in top_3_categories:
        with st.expander(f"📁 {category}"):
            cat_data = filtered_df[filtered_df[CATEGORY_COLUMN] == category]
            subcat_spend = cat_data.groupby('SubCategory')[AMOUNT_COLUMN].sum().sort_values(ascending=False)

            subcat_df = pd.DataFrame({
                'Subcategory': subcat_spend.index,
                'Spend': subcat_spend.values
            })
            subcat_df['Spend'] = subcat_df['Spend'].apply(format_currency)
            st.dataframe(subcat_df, use_container_width=True, hide_index=True)

            report_data[f'{category} - Subcategories'] = subcat_spend.reset_index()

elif report_type == "Geographic Analysis":
    st.markdown("### Geographic Analysis Report")

    state_spend = calculate_spend_by_state(filtered_df)

    st.markdown("#### Spend by State")
    state_df = pd.DataFrame({
        'State': state_spend.index,
        'Total Spend': state_spend.values,
        '% of Total': (state_spend.values / state_spend.sum() * 100)
    })
    state_df['Total Spend'] = state_df['Total Spend'].apply(format_currency)
    state_df['% of Total'] = state_df['% of Total'].apply(lambda x: f"{x:.1f}%")

    st.dataframe(state_df, use_container_width=True, hide_index=True)

    # Export data
    report_data['State Spend'] = state_spend.reset_index()

    # Suppliers by state
    st.markdown("#### Supplier Count by State")
    suppliers_by_state = filtered_df.groupby('Supplier State')[SUPPLIER_COLUMN].nunique().sort_values(ascending=False)

    supplier_state_df = pd.DataFrame({
        'State': suppliers_by_state.index,
        'Supplier Count': suppliers_by_state.values
    })
    st.dataframe(supplier_state_df, use_container_width=True, hide_index=True)

    report_data['Suppliers by State'] = supplier_state_df

elif report_type == "Consolidation Opportunities":
    st.markdown("### Consolidation Opportunities Report")

    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        min_suppliers = st.number_input("Minimum Suppliers", min_value=2, max_value=20, value=3)
    with col2:
        min_spend = st.number_input("Minimum Spend ($)", min_value=10000, max_value=1000000, value=100000, step=10000)

    opportunities = calculate_consolidation_opportunities(
        filtered_df,
        min_suppliers=min_suppliers,
        min_spend=min_spend
    )

    if len(opportunities) > 0:
        st.markdown("#### Identified Opportunities")

        display_opp = opportunities.copy()
        display_opp.reset_index(inplace=True)
        display_opp['Total Spend'] = display_opp['Total Spend'].apply(format_currency)
        display_opp['Potential Savings (10%)'] = display_opp['Potential Savings (10%)'].apply(format_currency)

        st.dataframe(display_opp, use_container_width=True, hide_index=True)

        # Summary
        total_savings = opportunities['Potential Savings (10%)'].sum()
        st.metric("💰 Total Potential Savings", format_currency(total_savings))

        # Export data
        report_data['Consolidation Opportunities'] = opportunities.reset_index()
    else:
        st.warning("No consolidation opportunities found with current criteria.")

elif report_type == "Custom Query":
    st.markdown("### Custom Query Builder")

    st.markdown("""
    Build a custom report by selecting the columns and groupings you need.
    Use the filters in the sidebar to narrow down the data.
    """)

    # Column selection
    available_columns = [
        'PO Number', 'PO Order Date', SUPPLIER_COLUMN, 'Supplier State',
        CATEGORY_COLUMN, 'SubCategory', AMOUNT_COLUMN, 'PO Status',
        'Year', 'Month', 'Quarter'
    ]

    selected_columns = st.multiselect(
        "Select columns to include",
        options=available_columns,
        default=[SUPPLIER_COLUMN, CATEGORY_COLUMN, AMOUNT_COLUMN]
    )

    # Grouping options
    group_by = st.multiselect(
        "Group by (optional)",
        options=[col for col in selected_columns if col != AMOUNT_COLUMN]
    )

    if st.button("Generate Custom Report"):
        if selected_columns:
            if group_by:
                # Grouped report
                agg_dict = {}
                if AMOUNT_COLUMN in selected_columns:
                    agg_dict[AMOUNT_COLUMN] = ['sum', 'mean', 'count']

                custom_report = filtered_df[selected_columns].groupby(group_by).agg(agg_dict)
                custom_report.columns = ['_'.join(col).strip() for col in custom_report.columns.values]
                custom_report = custom_report.reset_index()
            else:
                # Detail report
                custom_report = filtered_df[selected_columns].copy()

            st.markdown("#### Custom Report Results")
            st.dataframe(custom_report, use_container_width=True)

            report_data['Custom Report'] = custom_report
        else:
            st.warning("Please select at least one column.")

# Export section
st.markdown("---")
st.markdown("### 📥 Export Report")

if report_data:
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{report_type.replace(' ', '_')}_{timestamp}"

    if export_format == "Excel (.xlsx)":
        # Create Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for sheet_name, data in report_data.items():
                # Truncate sheet name to 31 characters (Excel limit)
                safe_sheet_name = sheet_name[:31]
                data.to_excel(writer, sheet_name=safe_sheet_name, index=False)

        output.seek(0)

        st.download_button(
            label="📥 Download Excel Report",
            data=output,
            file_name=f"{base_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:  # CSV
        if len(report_data) == 1:
            # Single sheet - direct CSV download
            csv_data = list(report_data.values())[0].to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name=f"{base_filename}.csv",
                mime="text/csv"
            )
        else:
            # Multiple sheets - show option to download each
            st.markdown("**Multiple datasets available - select one to download:**")
            for sheet_name, data in report_data.items():
                csv_data = data.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download {sheet_name}",
                    data=csv_data,
                    file_name=f"{base_filename}_{sheet_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    key=f"download_{sheet_name}"
                )

    st.markdown(f"""
    <div class="export-box">
        <strong>✅ Report Ready for Export</strong><br>
        Report Type: {report_type}<br>
        Period: {date_range[0]} to {date_range[1]}<br>
        Records: {len(filtered_df):,}<br>
        Datasets: {len(report_data)}
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Configure your report using the sidebar and the options above. Once generated, export options will appear here.")

# Raw data export option
st.markdown("---")
st.markdown("### 📊 Raw Data Export")

st.markdown("""
Export the filtered raw data (all transactions) for advanced analysis in external tools.
""")

col1, col2 = st.columns(2)

with col1:
    st.metric("Filtered Records", format_number(len(filtered_df)))

with col2:
    # Raw data export
    raw_csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Raw Data (CSV)",
        data=raw_csv,
        file_name=f"raw_data_{timestamp}.csv",
        mime="text/csv"
    )

# Data preview
with st.expander("👁️ Preview Filtered Data (First 100 rows)"):
    st.dataframe(filtered_df.head(100), use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Use filters in the sidebar to narrow down your data before generating reports. Export to Excel for multi-sheet reports or CSV for single datasets.")
