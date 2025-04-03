# app/visualizer.py

import matplotlib.pyplot as plt
import streamlit as st
from app.config import COLORS

def plot_price_with_indicators(df, show_sma=True, show_ema=False):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # Plot base close price
    ax.plot(df.index, df['Close'], color=COLORS['line'], linewidth=2.5, label="Close")

    # Optional overlays
    if show_sma and 'SMA' in df.columns:
        ax.plot(df.index, df['SMA'], color=COLORS['sma'], linestyle="--", label="SMA (14)")
    if show_ema and 'EMA' in df.columns:
        ax.plot(df.index, df['EMA'], color=COLORS['ema'], linestyle="-.", label="EMA (14)")

    # Axes + styling
    ax.set_title("Closing Price with Indicators", fontsize=14, color="white")
    ax.set_xlabel("Date", color="white")
    ax.set_ylabel("Price (USD)", color="white")
    ax.tick_params(axis='x', colors='white', rotation=45)
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
    ax.legend(loc="upper left", facecolor=COLORS['bg'], edgecolor="white")

    st.pyplot(fig)
