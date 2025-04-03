# main.py

import streamlit as st
import matplotlib.pyplot as plt
from app.config import DEFAULT_TICKER, DEFAULT_PERIOD, DEFAULT_INTERVAL
from app.data import get_stock_data, add_technical_indicators
from app.visualizer import plot_price_with_indicators
from app.ml_model import run_model

# ---------------- Streamlit Page Setup ----------------
st.set_page_config("Nimbus — Stock Dashboard", layout="wide", page_icon="🌩️")
st.title("🌩️ Nimbus — Real-Time Stock Prediction & Analysis")

# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker", value=DEFAULT_TICKER)
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=2)
interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "1h", "1d"], index=4)
st.sidebar.markdown("### Indicators")
show_sma = st.sidebar.checkbox("SMA", value=True)
show_ema = st.sidebar.checkbox("EMA", value=False)

# Forecast day selection
forecast_days = st.sidebar.slider("Days to Forecast", min_value=1, max_value=7, value=3)

# ---------------- Load & Process Data ----------------
df = get_stock_data(ticker, period, interval)

if not df.empty:
    df = add_technical_indicators(df)
    plot_price_with_indicators(df, show_sma, show_ema)

    # ---------------- ML Prediction ----------------
    st.subheader("🔮 Forecasting Future Prices")

    try:
        forecast_df = run_model(df, forecast_days=forecast_days)
        st.success(f"📅 Forecast for the next {forecast_days} day(s):")
        st.table(forecast_df)

    except ValueError as e:
        st.warning(f"⚠️ {e}")

    # ---------------- Table ----------------
    st.subheader("📊 Recent Price Data")
    st.dataframe(df.tail(), use_container_width=True)

else:
    st.warning("No data available. Try another ticker or time range.")
