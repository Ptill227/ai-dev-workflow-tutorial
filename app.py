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


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


# ---------------------------------------------------------------------------
# Chart/metric functions
# ---------------------------------------------------------------------------
def show_kpis(df: pd.DataFrame) -> None:
    total_sales = df["total_amount"].sum()
    total_orders = len(df)
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")


def make_trend_chart(df: pd.DataFrame):
    df_trend = (
        df.assign(month=df["date"].dt.to_period("M"))
        .groupby("month")["total_amount"]
        .sum()
        .reset_index()
    )
    df_trend["month"] = df_trend["month"].dt.to_timestamp()
    fig = px.line(
        df_trend,
        x="month",
        y="total_amount",
        title="Sales Trend Over Time",
        labels={"month": "Month", "total_amount": "Sales ($)"},
        markers=True,
        height=CHART_HEIGHT,
    )
    fig.update_xaxes(tickformat="%b %Y")
    fig.update_yaxes(tickformat=CURRENCY_FORMAT)
    return fig


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if not DATA_FILE.exists():
    st.error("Data file not found: data/sales-data.csv")
    st.stop()

df = load_data()

st.title(DASHBOARD_TITLE)
show_kpis(df)
st.divider()

st.plotly_chart(make_trend_chart(df), use_container_width=True)
st.divider()
