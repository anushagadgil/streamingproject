#importing necessary modules
import streamlit as st
import pandas as pd
import requests

#Alpha Vantage API key
api_key = "1TZV2HQBAV8PK6Q0"

# Defining a function to import stock market data
def get_stock_data(symbol, interval):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Main Streamlit app
st.title("Live Stock Market Data Visualization")

# Input for stock symbol and data interval
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):")
interval = st.selectbox("Select Data Interval", ["1min", "5min", "15min", "30min", "60min"])

if symbol and interval:
    st.write(f"Fetching {interval} data for {symbol}...")
    data = get_stock_data(symbol, interval)

    if "Time Series (1min)" in data:
        df = pd.DataFrame(data["Time Series (1min)"]).T
        df.index = pd.to_datetime(df.index)
        st.line_chart(df)
        st.subheader(f"Snippet of {symbol} Stock Data")
        st.dataframe(df.head(10))  # Display the first 10 rows of the dataframe
    else:
        st.write("Data not available for this symbol and interval.")



