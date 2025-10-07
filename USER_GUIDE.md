# 📖 Procurement Analytics Dashboard - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Navigation](#navigation)
3. [Page-by-Page Guide](#page-by-page-guide)
4. [Common Use Cases](#common-use-cases)
5. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Accessing the Dashboard
1. Open your web browser
2. Navigate to: `http://localhost:8501`
3. The home page will load automatically

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection not required (runs locally)
- Dashboard auto-refreshes when you interact with filters

---

## Navigation

### Sidebar Navigation
All pages are accessible from the left sidebar:
- 🏠 **Home** - Overview and quick stats
- 📊 **Executive Dashboard** - High-level KPIs and trends
- 🔍 **Supplier Explorer** - Detailed supplier analysis
- 💡 **Consolidation Opportunities** - Savings opportunities
- 🗺️ **Geographic Analysis** - State and regional insights
- 🏷️ **Category Deep Dive** - Category and subcategory analysis
- 📄 **Custom Reports** - Generate and export reports

### Common Controls
- **Date Range Picker**: Filter data by date
- **Multi-Select Dropdowns**: Hold Ctrl/Cmd to select multiple items
- **Clear Filters**: Use the X button in filter fields
- **Download Buttons**: Export data as Excel or CSV

---

## Page-by-Page Guide

### 🏠 Home Page

**Purpose**: Quick overview and data summary

**Key Features**:
- 4 KPI cards showing total spend, suppliers, states, POs
- Data period information
- File upload for custom datasets
- Navigation guide

**How to Use**:
1. Review the KPIs to understand dataset scope
2. Check the data period to confirm date range
3. Use sidebar to navigate to detailed analysis pages

---

### 📊 Executive Dashboard

**Purpose**: High-level overview for executives and stakeholders

**Key Features**:
- Real-time KPIs with filters
- Spend trend chart (Monthly/Quarterly/Yearly)
- Category pie chart with breakdown
- Top suppliers bar chart
- US choropleth map
- State-level analysis

**How to Use**:

**1. Apply Filters (Sidebar)**
- Select date range
- Choose specific categories
- Filter by states
- Select PO status

**2. Analyze Spend Trends**
- Use the period selector (Monthly/Quarterly/Yearly)
- Look for upward or downward trends
- Identify seasonal patterns

**3. Review Top Suppliers**
- Adjust "Top N" slider to see more/fewer suppliers
- Check concentration metric (top 10 as % of total)
- Click on bars for detailed tooltips

**4. Geographic Insights**
- Hover over states on the map to see spend
- Review "Top 10 States" bar chart
- Identify high-spend regions

**Use Case Example**:
*"Show me spending trends for Janitorial services in California over the last 6 months"*
1. Sidebar → Date Range: Last 6 months
2. Sidebar → Categories: Select "Janitorial"
3. Sidebar → States: Select "CA"
4. Review the spend trend chart

---

### 🔍 Supplier Explorer

**Purpose**: Deep dive into individual supplier performance

**Key Features**:
- Advanced supplier search
- Filter by category, state, date
- Paginated supplier list
- Detailed supplier profiles with tabs
- Sort options

**How to Use**:

**1. Find Suppliers**
- Use search box for specific names
- Apply category/state filters to narrow results
- Sort by spend, PO count, or categories served

**2. Explore Supplier Details**
- Click on any supplier in the list
- Review 4 key metrics at the top
- Use tabs to explore:
  - **Spend Trend**: Monthly spending patterns
  - **Categories**: Services provided
  - **Locations**: States where supplier operates
  - **Recent Orders**: Latest purchase orders

**3. Compare Suppliers**
- Use sort dropdown to rank suppliers
- Switch between pages to browse full list

**Use Case Example**:
*"Find all calibration suppliers in Texas and review their spending history"*
1. Sidebar → Categories: "Calibration"
2. Sidebar → States: "TX"
3. Review the filtered list
4. Click on each supplier to see spend trends

---

### 💡 Consolidation Opportunities

**Purpose**: Identify potential savings through supplier consolidation

**Key Features**:
- Automated opportunity detection
- Configurable criteria
- Interactive savings calculator
- Priority matrix
- Scenario builder with ROI calculator

**How to Use**:

**1. Configure Detection Criteria (Sidebar)**
- Minimum Suppliers: How many suppliers trigger an opportunity (default: 3)
- Minimum Spend: Minimum category spend to consider (default: $100K)
- Savings Rate: Expected savings percentage (default: 10%)

**2. Review Opportunities**
- **Overview Tab**: Top 10 opportunities with charts
- **Detailed List Tab**: Full table of all opportunities
- **Priority Matrix Tab**: Visual prioritization (bigger bubbles = more savings)

**3. Deep Dive Analysis**
- Select a subcategory from dropdown
- Review supplier breakdown
- See geographic distribution

**4. Build Scenarios**
- Set target number of suppliers
- Adjust custom savings rate
- Enter implementation cost
- Review ROI calculation

**Use Case Example**:
*"Find categories where we have too many suppliers and calculate potential savings"*
1. Sidebar → Min Suppliers: 5
2. Sidebar → Min Spend: $200,000
3. Sidebar → Savings Rate: 15%
4. Review "Overview" tab
5. Select top opportunity in "Deep Dive" tab
6. Use Scenario Builder to model consolidation

---

### 🗺️ Geographic Analysis

**Purpose**: Understand supplier distribution and spending by location

**Key Features**:
- Interactive US choropleth map
- State comparison tool
- Multi-state supplier finder
- Regional insights (Northeast, Midwest, South, West)

**How to Use**:

**1. Map View**
- Hover over states to see spend amounts
- Review "Top 15 States" bar chart
- Check state breakdown table

**2. State Comparison**
- Select 2-5 states to compare
- Review metrics table (spend, suppliers, POs)
- Analyze bar charts
- Check category breakdown by state

**3. Multi-State Suppliers**
- Review list of suppliers in multiple states
- Check "State Coverage" distribution
- Download list for further analysis

**4. Regional Insights**
- Review regional pie chart
- Compare regions using dual-axis chart
- Expand each region to see top categories

**Use Case Example**:
*"Compare janitorial spending in California, Texas, and New York"*
1. Sidebar → Categories: "Janitorial"
2. Navigate to "State Comparison" tab
3. Select CA, TX, NY from dropdown
4. Review comparison metrics and charts

---

### 🏷️ Category Deep Dive

**Purpose**: Analyze spending patterns within categories and subcategories

**Key Features**:
- Category overview with pie charts
- Supplier concentration analysis
- Interactive category explorer
- Trend analysis across categories
- Supplier capability matrix

**How to Use**:

**1. Overview Tab**
- Review category pie chart
- Check category breakdown table
- Analyze supplier concentration scatter plot

**2. Category Explorer**
- Select a category from dropdown
- Review subcategory treemap
- Check top suppliers in that category
- See geographic distribution

**3. Trend Analysis**
- Select 1-5 categories to compare
- Choose period (Monthly/Quarterly/Yearly)
- Review multi-line trend chart
- Check growth analysis table

**4. Supplier Capability Matrix**
- Review heatmap showing suppliers serving multiple categories
- Identify multi-category suppliers
- Download capability matrix CSV

**Use Case Example**:
*"Find suppliers who provide both Maintenance and Janitorial services"*
1. Navigate to "Supplier Capability Matrix" tab
2. Look for suppliers with cells colored in both categories
3. Review detailed table below heatmap
4. Download CSV for procurement team

---

### 📄 Custom Reports & Export

**Purpose**: Generate custom reports and export data for offline analysis

**Key Features**:
- 6 pre-built report types
- Advanced filtering
- Excel and CSV export
- Raw data export
- Custom query builder

**How to Use**:

**1. Select Report Type**
- Executive Summary
- Supplier Analysis
- Category Analysis
- Geographic Analysis
- Consolidation Opportunities
- Custom Query

**2. Apply Filters (Sidebar)**
- Date range
- Categories
- States
- Suppliers

**3. Generate Report**
- Review preview in main area
- For Custom Query: Select columns and groupings

**4. Export**
- Choose format: Excel (.xlsx) or CSV
- Click download button
- File downloads to your browser's download folder

**Use Case Examples**:

*Example 1: "Generate executive summary for Q1 2024"*
1. Report Type: Executive Summary
2. Date Range: Jan 1 - Mar 31, 2024
3. Click "Download Excel Report"

*Example 2: "Export all janitorial suppliers in California"*
1. Report Type: Supplier Analysis
2. Categories: Janitorial
3. States: CA
4. Export Format: CSV
5. Download report

*Example 3: "Create custom report showing spend by supplier and category"*
1. Report Type: Custom Query
2. Columns: Select "Supplier Name", "Category", "Amount"
3. Group By: Select "Supplier Name", "Category"
4. Click "Generate Custom Report"
5. Download Excel

---

## Common Use Cases

### Use Case 1: Quarterly Business Review
**Goal**: Prepare spending summary for leadership

**Steps**:
1. Home Page → Note total spend and supplier count
2. Executive Dashboard → Set date range to last quarter
3. Screenshot KPI cards
4. Review spend trend (set to Monthly)
5. Export top 20 suppliers chart
6. Navigate to Custom Reports
7. Generate Executive Summary report
8. Download Excel file for presentation

---

### Use Case 2: Supplier Consolidation Initiative
**Goal**: Identify opportunities to reduce supplier count

**Steps**:
1. Consolidation Opportunities page
2. Set Min Suppliers: 5
3. Set Min Spend: $100,000
4. Review Priority Matrix
5. Select top 3 opportunities
6. For each, use Deep Dive → Scenario Builder
7. Calculate total potential savings
8. Download opportunities CSV
9. Share with procurement team

---

### Use Case 3: Geographic Expansion Planning
**Goal**: Understand which states have most suppliers in a category

**Steps**:
1. Geographic Analysis page
2. Sidebar → Select category (e.g., "Manufacturing")
3. Map View → Review state distribution
4. Multi-State Suppliers tab → Identify national suppliers
5. Download multi-state supplier list
6. Category Deep Dive → Geographic distribution

---

### Use Case 4: Vendor Performance Review
**Goal**: Analyze spending trends for top 10 suppliers

**Steps**:
1. Executive Dashboard → Identify top 10 suppliers
2. Supplier Explorer → Search for each supplier
3. Review Spend Trend tab (look for increases/decreases)
4. Check Categories tab (services provided)
5. Review Recent Orders
6. Custom Reports → Supplier Analysis → Filter to top 10
7. Export Excel report

---

### Use Case 5: Category Spend Analysis
**Goal**: Break down spending within a major category

**Steps**:
1. Category Deep Dive page
2. Overview tab → Identify largest categories
3. Category Explorer → Select category
4. Review subcategory treemap
5. Check top suppliers
6. Trend Analysis → Compare subcategories over time
7. Export category metrics

---

## Tips & Tricks

### Performance Tips
1. **Use Date Filters**: Narrow date range for faster loading
2. **Clear Filters**: Reset filters when switching pages
3. **Cache Refresh**: Restart Docker if data seems stale

### Data Exploration Tips
1. **Start Broad, Then Narrow**: Begin with Executive Dashboard, then dive deeper
2. **Compare Time Periods**: Use date filters to compare quarters/years
3. **Cross-Reference Pages**: Use insights from one page to explore another
4. **Download Early**: Export data you'll need for offline analysis

### Visualization Tips
1. **Hover for Details**: All charts show tooltips on hover
2. **Click to Interact**: Some charts allow clicking for drill-down
3. **Zoom on Maps**: Choropleth maps can be zoomed
4. **Use Full Screen**: Expand browser to full screen for better visibility

### Export Tips
1. **Excel for Multi-Sheet**: Use Excel format when report has multiple datasets
2. **CSV for Single Dataset**: Use CSV for single tables (easier to import elsewhere)
3. **Raw Data Export**: Use for advanced analysis in Excel/Python/R
4. **Save Configurations**: Document your filter settings for repeatable reports

### Filter Combinations
**Powerful Filter Combos**:
- Date Range + Category → Trend analysis for specific service type
- State + Category → Regional service provider landscape
- Date Range + Supplier → Vendor performance over time
- Category + State + Date → Hyper-focused analysis

---

## Keyboard Shortcuts

- `Ctrl/Cmd + F`: Search on page
- `Ctrl/Cmd + R`: Refresh page
- `Ctrl/Cmd + Click`: Open link in new tab (for exports)
- `Esc`: Close modals/dropdowns

---

## Troubleshooting

### Dashboard is slow
- Reduce date range
- Clear some filters
- Close other browser tabs
- Restart Docker container

### Charts not showing
- Hard refresh: `Ctrl + Shift + R`
- Check filters (may be too restrictive)
- Verify data is loaded (check Home page)

### Export not working
- Check browser's download folder
- Disable popup blockers
- Try different export format
- Refresh page and try again

### Data seems wrong
- Check applied filters in sidebar
- Verify date range
- Clear all filters and start over
- Check source data (PO_Data.csv)

---

## Getting Help

### Quick Checks
1. Check applied filters
2. Review date range
3. Refresh page
4. Clear cache

### Support
- Check README.md for technical documentation
- Review Docker logs: `docker-compose logs`
- Contact: Procurement Analytics Team

---

**Version**: 1.0.0
**Last Updated**: 2025-10-06
**Happy Analyzing!** 📊✨
