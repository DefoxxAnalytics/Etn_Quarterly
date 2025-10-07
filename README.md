# 📊 Procurement Analytics Dashboard

Interactive Streamlit dashboard for procurement supplier spend analysis with Docker containerization.

**🔗 GitHub Repository**: https://github.com/DefoxxAnalytics/Etn_Quarterly

---

## 📥 Installation

### Clone the Repository
```bash
git clone https://github.com/DefoxxAnalytics/Etn_Quarterly.git
cd Etn_Quarterly
```

---

## 🐳 Quick Start with Docker (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- Docker Compose (included with Docker Desktop)
- Git (for cloning the repository)

### 1. Build and Run
```bash
docker-compose up -d
```

### 2. Access Dashboard
Open your browser and navigate to:
```
http://localhost:8501
```

### 3. Stop Application
```bash
docker-compose down
```

---

## 🔧 Using Different Port (if 8501 is taken)

### Method 1: Environment Variable
```bash
HOST_PORT=8502 docker-compose up -d
```
Access at: `http://localhost:8502`

### Method 2: Edit docker-compose.yml
```yaml
ports:
  - "8502:8501"  # Change 8502 to your desired port
```

### Method 3: Use .env File
```bash
# Create .env file
cp .env.example .env

# Edit .env
HOST_PORT=8502

# Run
docker-compose up -d
```

---

## 💻 Development Mode (with Live Reload)

### Run with Hot Reload
```bash
docker-compose -f docker-compose.dev.yml up
```

**Benefits:**
- Code changes automatically reload the app
- No need to rebuild Docker image
- Faster development iteration

### Stop Development Environment
```bash
docker-compose -f docker-compose.dev.yml down
```

---

## 🛠️ Alternative: Local Python Setup (Without Docker)

### 1. Install Python Dependencies
```bash
cd analytics_app
pip install -r requirements.txt
```

### 2. Check Port Availability
```bash
# Windows
netstat -ano | findstr :8501

# Mac/Linux
lsof -i :8501
```

### 3. Run Application
```bash
# Default port (8501)
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502
```

---

## 📊 Dashboard Features

### 🏠 Home Page
- Quick overview KPIs (Total Spend, Suppliers, States, POs)
- Data period summary
- File upload capability for custom datasets
- Navigation guide to all pages

### 📈 1. Executive Dashboard
- **Real-time KPIs**: Total Spend, Unique Suppliers, States Covered, Purchase Orders
- **Spend Trend Analysis**: Interactive line charts with trend lines (Monthly/Quarterly/Yearly views)
- **Category Breakdown**: Interactive pie charts with drill-down tables
- **Top Suppliers**: Bar charts showing top N suppliers with concentration analysis
- **Geographic Visualization**: US choropleth maps and state-level breakdowns
- **Dynamic Filters**: Date range, categories, states, PO status

### 🔍 2. Supplier Explorer
- **Advanced Search**: Full-text search across supplier names
- **Multi-Filter System**: Filter by category, state, date range
- **Detailed Profiles**: Per-supplier analytics with spend trends
- **Tabbed Analysis**:
  - Spend trends over time
  - Category breakdown per supplier
  - Geographic distribution
  - Recent order history
- **Pagination**: Browse through hundreds of suppliers efficiently
- **Sort Options**: By spend, PO count, average PO value, or category count

### 💡 3. Consolidation Opportunities
- **Opportunity Detection**: Automatically identifies categories with fragmented spending
- **Configurable Criteria**: Adjust minimum suppliers and spend thresholds
- **Interactive Savings Calculator**: Customize savings rates (5-30%)
- **Visual Analytics**:
  - Top opportunities bar charts
  - Priority matrix (scatter plot)
  - Category summaries
  - Savings distribution pie charts
- **Deep Dive Mode**: Detailed analysis per subcategory with supplier breakdowns
- **Scenario Builder**: "What-if" modeling with custom consolidation targets
- **ROI Calculator**: Implementation costs vs savings analysis
- **Export**: Download opportunities as CSV

### 🗺️ 4. Geographic Analysis
- **Interactive US Map**: Choropleth visualization of spend by state
- **State Comparison**: Side-by-side metrics for multiple states
- **Multi-State Suppliers**: Identify suppliers operating across multiple states
- **Regional Insights**: Northeast, Midwest, South, West regional breakdowns
- **Category-by-State**: Spend breakdown by category and geography
- **Visual Analytics**:
  - State bar charts
  - Regional pie charts
  - Dual-axis regional comparisons
- **Export**: Multi-state supplier lists

### 🏷️ 5. Category Deep Dive
- **Category Overview**: Pie charts and spend tables
- **Supplier Concentration**: Scatter plots showing supplier count vs spend
- **Category Explorer**:
  - Subcategory treemaps
  - Top suppliers per category
  - Geographic distribution per category
- **Trend Analysis**: Multi-line comparisons across categories (Monthly/Quarterly/Yearly)
- **Growth Metrics**: Period-over-period growth calculations
- **Supplier Capability Matrix**:
  - Heatmap showing which suppliers serve multiple categories
  - Multi-category supplier identification
  - Consolidation opportunity finder
- **Export**: Capability matrix CSV

### 📄 6. Custom Reports & Export
- **6 Report Types**:
  1. Executive Summary (KPIs, top suppliers, categories)
  2. Supplier Analysis (full metrics, spend distribution)
  3. Category Analysis (category metrics, subcategory breakdowns)
  4. Geographic Analysis (state spend, supplier counts)
  5. Consolidation Opportunities (configurable criteria)
  6. Custom Query Builder (select your own columns and groupings)
- **Advanced Filters**: Date range, categories, states, suppliers
- **Export Formats**:
  - Excel (.xlsx) with multiple sheets
  - CSV for single datasets
- **Raw Data Export**: Download filtered transaction-level data
- **Data Preview**: View first 100 rows before export

---

## 🐳 Docker Commands Reference

### Build and Run
```bash
# Build image
docker-compose build

# Run in detached mode
docker-compose up -d

# Run with logs visible
docker-compose up

# Rebuild and run (after code changes)
docker-compose up -d --build
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# View specific service logs
docker-compose logs streamlit-app

# Last 100 lines
docker-compose logs --tail 100
```

### Container Management
```bash
# Stop container
docker-compose stop

# Start stopped container
docker-compose start

# Restart container
docker-compose restart

# Remove container
docker-compose down

# Remove container and volumes
docker-compose down -v
```

### Access Container Shell
```bash
# Open bash in running container
docker exec -it procurement-analytics bash

# Run Python in container
docker exec -it procurement-analytics python

# Check file structure
docker exec -it procurement-analytics ls -la /app
```

### Check Container Health
```bash
# View container status
docker-compose ps

# Check health status
docker inspect procurement-analytics | grep -A 10 Health
```

---

## 📁 Project Structure

```
analytics_app/
├── app.py                          # Home page (264 lines)
├── pages/                          # Multi-page app (2,450+ lines)
│   ├── 1_📊_Executive_Dashboard.py        (324 lines)
│   ├── 2_🔍_Supplier_Explorer.py          (283 lines)
│   ├── 3_💡_Consolidation_Opportunities.py (410 lines)
│   ├── 4_🗺️_Geographic_Analysis.py        (476 lines)
│   ├── 5_🏷️_Category_Deep_Dive.py         (488 lines)
│   └── 6_📄_Custom_Reports.py             (469 lines)
├── utils/                          # Utilities (1,035 lines)
│   ├── __init__.py
│   ├── data_loader.py              (196 lines - caching, filtering)
│   ├── calculations.py             (342 lines - 20+ functions)
│   └── visualizations.py           (493 lines - 15+ chart types)
├── assets/                         # Static assets
│   ├── vtx_logo1.png
│   └── vtx_logo2.png
├── config.py                       # Configuration (74 lines)
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Production config
├── docker-compose.dev.yml          # Development config
├── requirements.txt                # Python dependencies
├── .dockerignore                   # Docker build optimization
├── .gitignore                      # Git exclusions
├── README.md                       # This file
├── USER_GUIDE.md                   # Comprehensive user guide
├── IMPLEMENTATION_SUMMARY.md       # Implementation details
└── CODE_VALIDATION_REPORT.md       # Validation results
```

---

## 🔒 Data Security

### Data Mounting
- Main CSV is mounted as **read-only** (`:ro` flag)
- Upload directory is writable for user uploads
- Data never committed to Docker image

### Volumes
```yaml
volumes:
  - ../PO_Data.csv:/app/data/PO_Data.csv:ro  # Read-only
  - ./data/uploads:/app/data/uploads          # Writable
```

---

## 🐛 Troubleshooting

### Port Already in Use
**Problem:** `Error: port 8501 already in use`

**Solution 1:** Use different port
```bash
HOST_PORT=8502 docker-compose up -d
```

**Solution 2:** Find and kill process using port
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8501 | xargs kill -9
```

---

### Container Won't Start
**Problem:** Container exits immediately

**Solution:** Check logs
```bash
docker-compose logs streamlit-app

# Common issues:
# 1. Data file not found - check ../PO_Data.csv exists
# 2. Port conflict - use different port
# 3. Syntax error in code - check logs for Python errors
```

---

### Cannot Access from Other Computers
**Problem:** Dashboard only accessible from localhost

**Solution:** Ensure correct network configuration
```bash
# 1. Check firewall allows port 8501
# 2. Verify server.address=0.0.0.0 in config
# 3. Access via server IP, not localhost
http://YOUR_SERVER_IP:8501
```

---

### Data Not Loading
**Problem:** "No data available" error

**Solution:** Verify data file path
```bash
# Check if CSV exists in parent directory
ls -la ../PO_Data.csv

# Check if mounted correctly in container
docker exec -it procurement-analytics ls -la /app/data/
```

---

### Slow Performance
**Problem:** Dashboard is slow or laggy

**Solution:** Increase Docker resources
1. Open Docker Desktop → Settings → Resources
2. Increase Memory to 4GB+
3. Increase CPUs to 2+
4. Restart Docker

---

## 📈 Performance Optimization

### Caching
- Data cached for 1 hour (configurable in `config.py`)
- Calculations cached automatically
- Clear cache: Restart container

### Large Datasets
For datasets > 100K records:
- Use date range filters to reduce data
- Consider data sampling for exploratory analysis
- Export large filtered datasets for offline analysis

---

## 🚀 Deployment Options

### Local Machine (Development)
```bash
docker-compose -f docker-compose.dev.yml up
```

### Network Server (Team Access)
```bash
# On server
docker-compose up -d

# Team access via
http://SERVER_IP:8501
```

### Cloud Deployment

**AWS ECS:**
```bash
# Push to ECR
docker tag procurement-analytics:latest YOUR_ECR_URL
docker push YOUR_ECR_URL

# Deploy to ECS task
```

**Azure Container Instances:**
```bash
# Push to ACR
docker tag procurement-analytics:latest YOUR_ACR_URL
docker push YOUR_ACR_URL
```

**Google Cloud Run:**
```bash
# Push to GCR
docker tag procurement-analytics:latest gcr.io/PROJECT_ID/procurement-analytics
docker push gcr.io/PROJECT_ID/procurement-analytics
```

---

## 📝 Environment Variables

Create `.env` file from template:
```bash
cp .env.example .env
```

**Available Variables:**
- `HOST_PORT` - Host port (default: 8501)
- `MIN_SUPPLIERS_FOR_CONSOLIDATION` - Minimum suppliers for consolidation flag (default: 3)
- `MIN_SPEND_FOR_CONSOLIDATION` - Minimum spend to flag consolidation (default: 100000)
- `DEFAULT_DISCOUNT_PERCENT` - Default discount percentage for savings calculator (default: 10)

---

## 🤝 Contributing

### Development Workflow
1. Make code changes
2. Test locally: `docker-compose -f docker-compose.dev.yml up`
3. Rebuild: `docker-compose build`
4. Test production build: `docker-compose up`
5. Commit changes

---

## 📞 Support

**Issues:**
- Container issues: Check logs with `docker-compose logs`
- Data issues: Verify CSV format matches expected structure
- Performance: Increase Docker resources in Docker Desktop

**Documentation:**
- Streamlit docs: https://docs.streamlit.io
- Docker docs: https://docs.docker.com
- Plotly docs: https://plotly.com/python/

---

## 📄 License

Internal use only - Proprietary

---

## 🔗 Repository Information

**GitHub**: https://github.com/DefoxxAnalytics/Etn_Quarterly
**Clone Command**: `git clone https://github.com/DefoxxAnalytics/Etn_Quarterly.git`

### Contributing
This is an internal project. For issues or feature requests, please contact the Procurement Analytics Team.

### Version Control
- **Branch**: main
- **Latest Commit**: Initial release v1.0.0
- **CI/CD**: Docker-based deployment

---

## 📊 Project Statistics

**Version:** 1.0.0
**Last Updated:** 2025-10-07
**Status:** ✅ Production Ready - All Features Complete
**Pages:** 7 (Home + 6 analysis pages)
**Total Code:** 3,900+ lines across 14 Python files
**Container Status:** Healthy and Running
**Repository**: https://github.com/DefoxxAnalytics/Etn_Quarterly
**Maintained By:** Procurement Analytics Team

---

## ✅ Completed Features Summary

**All 7 Phases Complete:**
- ✅ Phase 0: Docker Setup & Infrastructure
- ✅ Phase 1: Core Application (Home Page, Data Loader, Config)
- ✅ Phase 2: Executive Dashboard with KPIs and Visualizations
- ✅ Phase 3: Supplier Explorer with Search & Detailed Profiles
- ✅ Phase 4: Consolidation Opportunities with Savings Calculator
- ✅ Phase 5: Geographic Analysis with US Maps & Regional Insights
- ✅ Phase 6: Category Deep Dive with Capability Matrix
- ✅ Phase 7: Custom Reports & Export (Excel/CSV)

**Total Components:**
- 7 Interactive Pages
- 50+ Interactive Charts & Visualizations
- 20+ Cached Analysis Functions
- 15+ Chart Generator Functions
- Multi-format Export (Excel, CSV)
- Full Docker Containerization

**Data Insights Provided:**
1. ✅ How many suppliers do the "same thing" and where? → Consolidation Opportunities + Supplier Capability Matrix
2. ✅ How many calibration companies by state? → Geographic Analysis + Category Deep Dive
3. ✅ How many janitorial companies by state? → Geographic Analysis + Category Deep Dive
4. ✅ Top spend suppliers and common services? → Executive Dashboard + Supplier Explorer
5. ✅ Additional insights → All 6 analytical pages with 50+ visualizations
