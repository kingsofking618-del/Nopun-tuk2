import streamlit as st
import pandas as pd
import requests

st.title("🚀 Upstox EMA Scanner")

# Secrets se token lo
ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Accept': 'application/json'}

def get_upstox_data(instrument_key, interval):
    # Upstox V3 Historical Data URL
    url = f"https://api.upstox.com/v2/historical-candle/{instrument_key}/{interval}/2026-07-02/2026-06-01"
    response = requests.get(url, headers=headers).json()
    data = pd.DataFrame(response['data']['candles'], columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'oi'])
    return data

# Example Instrument Key (Upstox se le lena)
stocks = {'RELIANCE': 'NSE_EQ|INE002A01018'} 

for name, key in stocks.items():
    df = get_upstox_data(key, 'day')
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    
    if df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]:
        st.success(f"{name} is Bullish (Upstox Data)")
    else:
        st.error(f"{name} is Bearish (Upstox Data)")
        
