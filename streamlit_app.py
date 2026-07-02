import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Scanner", layout="wide")
st.title("🚀 EMA Scanner (15m to Daily)")

stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS'] # Yahan apni list badha lena
timeframes = {'15m': '15m', '1h': '1h', '1d': '1d'}

for tf, val in timeframes.items():
    st.subheader(f"Timeframe: {tf}")
    for stock in stocks:
        df = yf.download(stock, period='5d', interval=val, progress=False)
        if len(df) > 50:
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
            
            if df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]:
                st.success(f"{stock} is Bullish")
            else:
                st.error(f"{stock} is Bearish")
                
