import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from app.data import add_technical_indicators

def run_model(df, forecast_days=3):
    df = df.copy().dropna()

    if len(df) < 40:
        raise ValueError("Not enough data points. Try a longer time period (e.g., 3mo or 6mo).")

    features = df[[
        'SMA', 'EMA', 'RSI', 'MACD', 'MACD_SIGNAL',
        'Return', 'Volatility', 'Lag_1', 'Lag_2'
    ]]
    target = df['Close'].shift(-forecast_days)

    df = df.iloc[:-forecast_days]
    features = features.iloc[:-forecast_days]
    target = target.dropna()

    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model.fit(features, target)

    # Recalculate indicators using full data
    df_full = add_technical_indicators(df.copy())
    df_full = df_full.ffill().bfill().dropna()

    if df_full.shape[0] == 0:
        raise ValueError("Not enough clean data after indicator calculation. Try a longer period.")

    # Use last row for forecasting
    last_known = df_full.copy()
    future_predictions = []

    for i in range(forecast_days):
        required_features = [
            'SMA', 'EMA', 'RSI', 'MACD', 'MACD_SIGNAL',
            'Return', 'Volatility', 'Lag_1', 'Lag_2'
        ]

        latest_row = last_known.iloc[-1:][required_features]

        if latest_row.isnull().any().any() or latest_row.shape[0] == 0:
            raise ValueError("Forecast input still contains missing values.")

        pred = model.predict(latest_row.to_numpy())[0]
        future_predictions.append(pred)

        next_row = last_known.iloc[-1:].copy()
        next_row['Lag_2'] = next_row['Lag_1']
        next_row['Lag_1'] = pred
        next_row['Return'] = (pred - next_row['Close'].values[0]) / next_row['Close'].values[0]
        next_row['Volatility'] = df_full['Return'].rolling(5).std().iloc[-1]
        next_row['Close'] = pred

        last_known = pd.concat([last_known, next_row], ignore_index=True)

    forecast_df = pd.DataFrame({
        'Forecast Day': [f'Day +{i+1}' for i in range(forecast_days)],
        'Predicted Price': future_predictions
    })

    return forecast_df