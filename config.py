"""
Application Configuration
Centralized configuration for paths, settings, and defaults
"""
import os
from pathlib import Path

# ======================
# Paths
# ======================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

# Data file paths
DEFAULT_CSV_PATH = os.getenv('DATA_PATH', str(DATA_DIR / "PO_Data.csv"))
PARENT_CSV_PATH = BASE_DIR.parent / "PO_Data.csv"

# Use parent CSV if it exists, otherwise use mounted data path
CSV_PATH = str(PARENT_CSV_PATH) if PARENT_CSV_PATH.exists() else DEFAULT_CSV_PATH

# ======================
# Server Configuration
# ======================
DEFAULT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
ALTERNATIVE_PORTS = [8502, 8503, 8504, 8505]

# ======================
# Data Configuration
# ======================
CSV_ENCODING = 'utf-8-sig'
DATE_COLUMN = 'PO Order Date'
SUPPLIER_COLUMN = 'Corcentric Supplier Name'
AMOUNT_COLUMN = 'Line Item Subtotal'
CATEGORY_COLUMN = 'Category'

# State columns - IMPORTANT DISTINCTION
SHIP_TO_STATE_COLUMN = 'State'  # Where items are shipped TO
SUPPLIER_LOCATION_COLUMN = 'Supplier City/State'  # Where supplier is located
STATE_COLUMN = 'Supplier State'  # Extracted from Supplier City/State (created by data_loader)

# ======================
# Analysis Configuration
# ======================
MIN_SUPPLIERS_FOR_CONSOLIDATION = int(os.getenv('MIN_SUPPLIERS_FOR_CONSOLIDATION', 3))
MIN_SPEND_FOR_CONSOLIDATION = float(os.getenv('MIN_SPEND_FOR_CONSOLIDATION', 100000))
DEFAULT_DISCOUNT_PERCENT = int(os.getenv('DEFAULT_DISCOUNT_PERCENT', 10))

# Top N configurations
TOP_N_SUPPLIERS = 20
TOP_N_STATES = 10

# ======================
# UI Configuration
# ======================
PAGE_TITLE = "Procurement Analytics Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Chart colors
CHART_COLOR_SCHEME = "blues"
PRIMARY_COLOR = "#1f77b4"

# ======================
# Export Configuration
# ======================
EXPORT_FORMATS = ['Excel', 'CSV']
MAX_EXPORT_ROWS = 1000000

# ======================
# Cache Configuration
# ======================
CACHE_TTL = 3600  # 1 hour in seconds
