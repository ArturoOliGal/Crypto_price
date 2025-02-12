
import pandas as pd 
import numpy as np
import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup
import requests
import json
import time
import seaborn as sns



st.set_page_config(layout="wide")
st.title("Crypto price app")
st.markdown("""
#This appp retrives cryptocurrency price for the top 100 cryptocurrency from the *CoinMarketCap*          
""")
expander_bar= st.expander("About")
expander_bar.markdown("""
#* **Python libreries:** pandas, matplotlib, streamlit, base 64, numpy, PIL, bs4, request, json, time, seaborn
#* **Data source:** [CoinMarketCap](https://www.wikipedia.org) 
""")

col1=st.sidebar
col2, col3= st.columns((2,1))

col1.header('Input Options')
currency_price_unit=col1.selectbox('select currency for price', ('USD','BTC', 'ETH'))

@st.cache_data
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data


    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
        coin_name.append(i['Name'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote'][currency_price_unit]['price'])
        percent_change_1h.append(i['quote'][currency_price_unit]['percent_change_1h'])
        percent_change_24h.append(i['quote'][currency_price_unit]['percent_change_7d'])
        percent_change_7d.append(i['quote'][currency_price_unit]['percent_change_7d'])
        market_cap.append(i['quote'][currency_price_unit]['market_cap'])
        volume_24h.append(i['quote'][currency_price_unit]['volume_24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h',
                            'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df


df = load_data()

sorted_coin=sorted(df['coin_symbol'])
selected_coin=col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)


