Stock Market Price Analysis
![image](https://github.com/anushagadgil/streamingproject/assets/64644918/1103c109-6265-4bba-a32c-a0b7093b2d20)

Abstract:
I recently ventured into the world of Fintech and saw what an important role time series Analysis plays in trading .In my app, I have used one such model (ARIMA) to perform an analysis on Stock market data. My App fetches real time stock market Data from the Alpha Vantage API and produces plots of the same.

Stock Market Analysis is :
Crucial for investors to take informed risks
Helps in calculating valuation of companies
Is an indicator of the economic Indicator of the health of a country
Helps in Long Term Planning.

Data Description:
I fetched my Data from the Alpha Vantage free API service:
Parameters used to Fetch Data:

"function": "TIME_SERIES_INTRADAY",
"symbol": symbol
"interval": interval
"apikey": api_key

Model Used: ARIMA
Reason for picking the Model:
ARIMA accounts for autocorrelation and can handle non-stationary data by differencing to achieve stationarity.
Notations :
p = 3: The autoregressive (AR) component order. It represents the number of lag observations included in the model.
d = 1: The differencing order. It signifies the degree of differencing required to achieve stationarity in the time series.
q = 2: The moving average (MA) component order. It indicates the size of the moving average window.

Performed a grid search to find optimal PDQ values
Did a visual Inspection of my Data






