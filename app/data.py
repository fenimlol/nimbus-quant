# app/data.py

import yfinance as yf
import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

def get_stock_data(ticker, period, interval):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df.dropna()
    except Exception:
        return pd.DataFrame()

def add_technical_indicators(df):
    df['SMA'] = SMAIndicator(close=df['Close'], window=14).sma_indicator()
    df['EMA'] = EMAIndicator(close=df['Close'], window=14).ema_indicator()
    df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_SIGNAL'] = macd.macd_signal()

    # New engineered features
    df['Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Return'].rolling(window=5).std()
    df['Lag_1'] = df['Close'].shift(1)
    df['Lag_2'] = df['Close'].shift(2)
    
    return df.dropna()