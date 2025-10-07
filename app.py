"""
Procurement Analytics Dashboard - Home Page
Main entry point for the Streamlit application
"""
import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.data_loader import load_data, get_data_summary, format_currency, format_number
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .logo-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/vtx_logo2.png", width=150)
with col2:
    st.markdown('<h1 class="main-header">Procurement Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive insights into supplier spending, consolidation opportunities, and geographic distribution**")

st.markdown("---")

# Sidebar branding
with st.sidebar:
    st.image("assets/vtx_logo2.png", width=200)
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    st.markdown("Use the pages in the sidebar to explore different analytics views.")
    st.markdown("---")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**Powered by:** Streamlit")

# Load data
with st.spinner("🔄 Loading procurement data..."):
    df = load_data()

    if df.empty:
        st.error("No data available. Please check data source or upload a file below.")
        st.stop()

    summary = get_data_summary(df)

# Welcome message
st.markdown("""
### 👋 Welcome!

This dashboard provides **real-time, interactive analytics** for procurement spend analysis.
Use the sidebar to navigate between different views and filters.

**Key Capabilities:**
- 📊 **Executive Dashboard** - High-level KPIs and trends
- 🔍 **Supplier Explorer** - Deep dive into supplier data
- 💡 **Consolidation Opportunities** - Identify savings potential
- 🌎 **Geographic Analysis** - State-by-state breakdown
- 📂 **Category Analysis** - Spending by category
- 📋 **Custom Reports** - Build and export custom views
""")

st.markdown("---")

# Quick Stats Section
st.subheader("📈 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Spend",
        value=format_currency(summary['total_spend']),
        help="Total procurement spending across all suppliers"
    )

with col2:
    st.metric(
        label="🏢 Suppliers",
        value=format_number(summary['unique_suppliers']),
        help="Number of unique suppliers"
    )

with col3:
    st.metric(
        label="🗺️ States",
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

# Data Period Info
col1, col2 = st.columns([2, 1])

with col1:
    st.info(f"""
    📅 **Data Period**
    **From:** {summary['date_min'].strftime('%B %d, %Y')}
    **To:** {summary['date_max'].strftime('%B %d, %Y')}

    📊 **Coverage**
    **Records:** {format_number(summary['total_records'])}
    **Categories:** {summary['categories']}
    **Subcategories:** {summary['subcategories']}
    """)

with col2:
    # Quick links
    st.markdown("### 🚀 Quick Links")
    st.markdown("""
    Navigate to dashboard pages using the sidebar ⬅️

    Start with the **Executive Dashboard** for an overview!
    """)

st.markdown("---")

# Navigation Guide
st.subheader("🧭 Dashboard Pages")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📊 **Executive Dashboard**", expanded=False):
        st.markdown("""
        High-level overview with interactive visualizations:
        - Total spend trends over time
        - Top 20 suppliers by spend
        - Geographic heat map
        - Category breakdown
        - Filterable by date range and category
        """)

    with st.expander("🔍 **Supplier Explorer** (Coming Soon)", expanded=False):
        st.markdown("""
        Search and analyze individual suppliers:
        - Search by supplier name
        - Filter by category, state, spend range
        - View supplier spend trends
        - See detailed supplier profiles
        """)

    with st.expander("💡 **Consolidation Opportunities** (Coming Soon)", expanded=False):
        st.markdown("""
        Identify cost savings potential:
        - Find categories with multiple suppliers
        - Interactive savings calculator
        - "What-if" scenarios
        - Action plan generator
        """)

with col2:
    with st.expander("🌎 **Geographic Analysis** (Coming Soon)", expanded=False):
        st.markdown("""
        State-by-state spending analysis:
        - Interactive US heat map
        - State comparison tool
        - Multi-state supplier finder
        - Regional consolidation opportunities
        """)

    with st.expander("📂 **Category Deep Dive** (Coming Soon)", expanded=False):
        st.markdown("""
        Category and subcategory analysis:
        - Hierarchical category view
        - Supplier capability matrix
        - Trend analysis by category
        - Bundling opportunities
        """)

    with st.expander("📋 **Custom Reports** (Coming Soon)", expanded=False):
        st.markdown("""
        Build custom reports:
        - Apply custom filters
        - Select specific metrics
        - Export to Excel or CSV
        - Save report configurations
        """)

st.markdown("---")

# File Upload Section
st.subheader("📤 Upload Custom Data (Optional)")

uploaded_file = st.file_uploader(
    "Upload a CSV file to analyze different data",
    type=['csv'],
    help="Upload a CSV file with the same format as PO_Data.csv to analyze different datasets"
)

if uploaded_file:
    with st.spinner("🔄 Processing uploaded file..."):
        try:
            new_df = load_data(uploaded_file)
            if not new_df.empty:
                new_summary = get_data_summary(new_df)
                st.success(f"✅ Successfully loaded {format_number(new_summary['total_records'])} records from uploaded file!")
                st.session_state['uploaded_df'] = new_df
                st.session_state['using_uploaded_data'] = True

                # Show quick stats for uploaded data
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Spend", format_currency(new_summary['total_spend']))
                with col2:
                    st.metric("Suppliers", format_number(new_summary['unique_suppliers']))
                with col3:
                    st.metric("Records", format_number(new_summary['total_records']))
            else:
                st.error("❌ Uploaded file is empty or has invalid format")
        except Exception as e:
            st.error(f"❌ Error processing uploaded file: {str(e)}")

# Footer
st.markdown("---")
st.caption(f"""
**Procurement Analytics Dashboard v1.0** | Powered by Streamlit
Last data update: {summary['date_max'].strftime('%B %d, %Y')} |
Total records: {format_number(summary['total_records'])}
""")
