import streamlit as st
import warnings
warnings.filterwarnings('ignore')  # Hide warnings
import datetime as dt

import numpy as np
import matplotlib.pyplot as plot

import seaborn as sns

from PIL import Image
import os

from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

st.set_page_config(layout="wide")
#title
st.title('Stock Market Analyser App')
'---------------------------------------------------------'

#st.write("Developed by Elias Demian")

image = Image.open(os.path.join('STOCK.png'))
st.image(image)

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", dt.date(2019, 1, 1))
'You Enterted the starting date: ', start_date
end_date = st.sidebar.date_input("End date", dt.date(2022, 1, 31))
'You Enterted the ending date: ', end_date

stocks = ('GOOG', 'AAPL', 'MSFT', 'TSLA','FB','AMZN','BTC-USD','ETH-USD')
com = st.selectbox('Select dataset for prediction', stocks)



#start_date= st.text_input("Enter Starting date as YYYY-MM-DD", "2019-01-10")
#end_date= st.text_input("Enter Ending date as YYYY-MM-DD", "2022-01-20")


df = web.DataReader(com, 'yahoo', start_date, end_date)  # Collects data
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

#title
st.title('Stock Market Data')

'The Complete Stock Data as extracted from Yahoo Finance: '
df

'1. The Stock Open Values over time: '
st.line_chart(df["Open"])

'2. The Stock Close Values over time: '
st.line_chart(df["Close"])

#title
st.title('Moving Averages')
'---------------------------------------------------------'
'Stock Data Based on Moving Averages'

mov_avg= st.text_input("Enter number of days Moving Average:", "30")

'You Enterted the Moving Average: ', mov_avg


df["mov_avg_close"] = df['Close'].rolling(window=int(mov_avg),min_periods=0).mean()

'1. Plot of Stock Closing Value for '+ mov_avg+ " Days of Moving Average"
'   Actual Closing Value also Present'
st.line_chart(df[["mov_avg_close","Close"]])

df["mov_avg_open"] = df['Open'].rolling(window=int(mov_avg),min_periods=0).mean()

'2. Plot of Stock Open Value for '+ mov_avg+ " Days of Moving Average"
'   Actual Opening Value also Present'
st.line_chart(df[["mov_avg_open","Open"]])



st.title("Candle Stick Graph")
'------------------------------------------------------------------------------------------'
'Traders use candlestick charts to forecast price movement based on previous patterns.'
'They are important in trading because they display four price points (open, close, high, and low) across the time period specified by the trader.'


ohlc_day= st.text_input("Enter number of days for Resampling", "30")

'You Enterted the Moving Average: ', ohlc_day

# Resample to get open-high-low-close (OHLC) on every n days of data


df_ohlc = df.Close.resample(ohlc_day+'D').ohlc() 
df_volume = df.Volume.resample(ohlc_day+'D').sum()



df_ohlc.reset_index(inplace=True)
df_ohlc.Date = df_ohlc.Date.map(mdates.date2num)



# Create and visualize candlestick charts
st.set_option('deprecation.showPyplotGlobalUse', False) #additional warning hide
plot.figure(figsize=(8,6))

'OHLC Candle Stick Graph for '+ ohlc_day+ " Days"

ax1 = plot.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
plot.xlabel('Time')
plot.ylabel('Stock Candle Sticks')
st.pyplot()

st.markdown('''# **Binance Price App**
And here's a view on the world's biggest cryptoccurrency market
''')

st.header('**Selected Price**')

# Load market data from Binance API
df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')

# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a

#SideBar pt2
st.sidebar.subheader('9 choices of prices:')
crpytoList = {
    'Price 1': 'BTCBUSD',
    'Price 2': 'ETHBUSD',
    'Price 3': 'BNBBUSD',
    'Price 4': 'XRPBUSD',
    'Price 5': 'ADABUSD',
    'Price 6': 'DOGEBUSD',
    'Price 7': 'SHIBBUSD',
    'Price 8': 'DOTBUSD',
    'Price 9': 'MATICBUSD'
}

col1, col2, col3 = st.columns(3)

for i in range(len(crpytoList.keys())):
    selected_crypto_label = list(crpytoList.keys())[i]
    selected_crypto_index = list(df.symbol).index(crpytoList[selected_crypto_label])
    selected_crypto = st.sidebar.selectbox(selected_crypto_label, df.symbol, selected_crypto_index, key = str(i))
    col_df = df[df.symbol == selected_crypto]
    col_price = round_value(col_df.weightedAvgPrice)
    col_percent = f'{float(col_df.priceChangePercent)}%'
    if i < 3:
        with col1:
            st.metric(selected_crypto, col_price, col_percent)
    if 2 < i < 6:
        with col2:
            st.metric(selected_crypto, col_price, col_percent)
    if i > 5:
        with col3:
            st.metric(selected_crypto, col_price, col_percent)

st.header('**All Prices**')
st.dataframe(df)



st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

st.title("Note")
'------------------------------------------------------'
'Accurately enter the stock code and dates based on your personal knowledge'
'Stock Prices in USD'
