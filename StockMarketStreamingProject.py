#Importing necessary modules 
pip install statsmodels
import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests

#Providing the API Key
api_key = "5U7CIQX3LTNFIGGZ"

#setting the background
page_bg_img = '''
<style>
body {
background-image: url("https://www.google.co.in/search?q=stock+market+images+urls&tbm=isch&ved=2ahUKEwj3_tGSsvSCAxUQD1kFHcc_DT0Q2-cCegQIABAA&oq=stock+market+images+urls&gs_lcp=CgNpbWcQAzoKCAAQgAQQigUQQzoFCAAQgAQ6BggAEAgQHlCVA1jFIWDQJGgCcAB4AIABigGIAZcHkgEDMC44mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=VwttZbf3MJCe5NoPx_-06AM&bih=786&biw=1707#imgrc=dwYg_uSHLgKcfM");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


# Function that imports the stockmarket data
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

# Text box for users to provide input for stock symbol and data interval
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):")
interval = st.selectbox("Select Data Interval", ["1min", "5min", "15min", "30min", "60min"])



if symbol:
    st.write(f"Fetching data for {symbol}...")

    data = get_stock_data(symbol, interval)

    if f"Time Series ({interval})" in data:
        df = pd.DataFrame(data[f"Time Series ({interval})"]).T.reset_index()
        df.columns = ["Timestamp", "1. open", "2. high", "3. low", "4. close", "5. volume"]
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.set_index("Timestamp")

        st.subheader(f"{symbol} Stock Data ({interval})")
        st.dataframe(df.head(1000))

        # Plotting the graph
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.plot(df.index, df['4. close'], label='CloseS Price')
        ax.set_xlabel('Time')
        ax.set_ylabel('Close Price')
        ax.set_title(f'{symbol} Close Price over Time ({interval} intervals)')
        ax.legend()
        st.pyplot(fig)

    else:
        st.write(f"No {interval} data available for this symbol.")




# Creating a function for ARIMA Forecasting
def arima_forecast(data):
    # Set the Timestamp as a proper datetime column
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d-%m-%Y')

    # Set Timestamp as the index with a monthly frequency
    data.set_index('Timestamp', inplace=True)
    data.index = pd.to_datetime(data.index)
    data = data.asfreq('M')

    # Setting the model with appropriate parameters
    model = ARIMA(data['4. close'], order=(3, 1, 2)) 
    results = model.fit()

    # defining the range of forecasting
    forecast_dates = pd.date_range(start='2023-12-01', periods=24, freq='M')  

    # generating predictions
    forecast = results.get_forecast(steps=len(forecast_dates)).predicted_mean

    # plotting the results
    plt.figure(figsize=(20, 6))
    plt.plot(forecast_dates, forecast, label='Forecast', color='red', linestyle='--')
    plt.title('Stock Price Forecast from 2024 to 2025 using ARIMA', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Stock Price', fontsize=12)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set x-axis to month locator
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Date format
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=14)
    plt.tight_layout()

    # Displaying the plot on Streamlit
    st.pyplot(plt)

# Main Streamlit app
st.title("Stock Price Forecast using ARIMA")

#taking user uploads for files
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head())

    if st.button("Generate ARIMA Forecast"):
        st.write("Generating ARIMA Forecast...")
        arima_forecast(data)
