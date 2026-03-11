from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_FILE = Path(__file__).parent / "data" / "sales-data.csv"
DASHBOARD_TITLE = "ShopSmart Sales Dashboard"
CURRENCY_FORMAT = "$,.0f"
CHART_HEIGHT = 400

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title=DASHBOARD_TITLE, layout="wide")
