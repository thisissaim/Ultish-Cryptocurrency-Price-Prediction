import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings
import streamlit.components.v1 as components
import time
import plotly.figure_factory as ff
from PIL import Image

warnings.filterwarnings("ignore")
pd.options.display.float_format = "${:,.2f}".format
today = datetime.today().strftime("%Y-%m-%d")
start_date = "2020-01-01"

def get_highest_lowest_prices(df):
    highest_price = df["Close"].max()
    lowest_price = df["Close"].min()
    return highest_price, lowest_price

def get_price_change_percentage(df):
    first_price = df.iloc[0]["Close"]
    last_price = df.iloc[-1]["Close"]
    percentage_change = ((last_price - first_price) / first_price) * 100
    return percentage_change




rad = st.sidebar.radio(
    "Menu",
    [
        "Homepage",
        "History of currency",
        "History of currency with Candlesticks",
        "Currency Price Prediction",
        "Custom",
        "test Page",
    ],
)
if rad == "Homepage":

    #st.title("Cryptocurrency Price Prediction")
    image1 = Image.open("ultish.jpeg")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image1 , width = 100)

    with col2:
        st.write(' ')

    with col3:
        st.write(' ')


    #st.image(image1, width=300)
    st.markdown("<h1 style='text-align: center; color: white;'>Cryptocurrency Price Prediction</h1>", unsafe_allow_html=True)


    st.markdown(""" 
    
    # Task 1 by Ultish Technologies
    ##  Contents
    ###  History of Cryptocurrency Prediction
    ###  Actual v/s Prediction Prices
    ###  Predicting Future Prices
    ###  Custom Entry for Prediction
    :running: <br>              
    **Model Used: Prophet**
    <br>
    [Link to My Github Profile](https://github.com/thisissaim)
    </div>
    """,True)
elif rad == "History of currency":
    currency = st.selectbox(
        "Which Currency do you want to predict",
        (
            "ADA-USD",
            "AERGO-USD", 
            "BTC-USD",
            "ETH-USD",
            "XRP-USD",
            "ADA-USD",
            "USDT-USD",
            "DOGE-USD",
            "SOL-USD",
            "MATIC-USD",
            "TRX-USD",
            "STETH-USD",
            "SHIB-USD",
            "LEO-USD",
            "LINK-USD"
                       
        ),
    )
    eth_df = yf.download(currency, start_date, today)
    eth_df.reset_index(inplace=True)
    
    # Get highest and lowest prices
    highest_price, lowest_price = get_highest_lowest_prices(eth_df)
    st.write("All time Highest Price:", highest_price)
    st.write("All time Lowest Price:", lowest_price)

    # Get price change percentage
    percentage_change = get_price_change_percentage(eth_df)
    st.write("Percentage Change over the years:", percentage_change)


    fig = go.Figure()

    # Set title
    fig.update_layout(
        title_text="Time series plot of currency open price",
    )
    fig2 = go.Figure(
        data=[
            go.Candlestick(
                x=eth_df["Date"],
                open=eth_df["Open"],
                high=eth_df["High"],
                low=eth_df["Low"],
                close=eth_df["Close"],
            )
        ]
    )
    # st.write("# History of Ethereum with Candlesticks")

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    df = eth_df[["Date", "Open"]]
    df = df.rename(columns={"Date": "ds", "Open": "y"})

    x = df["ds"]
    y = df["y"]
    
    bb = fig.add_trace(go.Scatter(x=x, y=y))
    #bb = fig.scatter(marker=dict(color='red'))
    # # st.write("# History of Ethereum")

    m = Prophet(seasonality_mode="multiplicative")
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    #aa = plot_plotly(m, forecast)
    # st.write("# Ethereum Coin Price Prediction")
    # st.write(aa)

    plot_components_plotly(m, forecast)
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    # st.write("# History of currency")
    st.write(bb)
    #
    # col1 = st.columns(1)
    from datetime import date

    today = date.today()

    col1 = st.columns(1)
    for i in forecast.index:
        if today == forecast["ds"][i]:
            r1 = forecast["yhat"][i]
            r2 = r1 / 100

            st.write("### ", r1, " $  is the predictive open pricing for today")

############################################################################################################################################           

elif rad == "History of currency with Candlesticks":
    currency = st.selectbox(
        "Which Currency do you want to predict",
        (
            "ADA-USD",
            "AERGO-USD", 
            "BTC-USD",
            "ETH-USD",
            "XRP-USD",
            "ADA-USD",
            "USDT-USD",
            "DOGE-USD",
            "SOL-USD",
            "MATIC-USD",
            "TRX-USD",
            "STETH-USD",
            "SHIB-USD",
            "LEO-USD",
            "LINK-USD"
                       
        ),
    )
    eth_df = yf.download(currency, start_date, today)

    eth_df.reset_index(inplace=True)
    
     
    fig = go.Figure()
        # Set title
    fig.update_layout(
        title_text="Time series plot of currency Open Price",
    )
    fig2 = go.Figure(
        data=[
            go.Candlestick(
                x=eth_df["Date"],
                open=eth_df["Open"],
                high=eth_df["High"],
                low=eth_df["Low"],
                close=eth_df["Close"],
            )
        ]
    )
    # st.write("# History of Ethereum with Candlesticks")

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    df = eth_df[["Date", "Close"]]
    df = df.rename(columns={"Date": "ds", "Close": "y"})


    x = df["ds"]
    y = df["y"]
    bb = fig.add_trace(go.Scatter(x=x, y=y,showlegend=True))
    #bb = fig.update_traces(marker=dict(color='red'))
    # st.write("# History of Ethereum")

    m = Prophet(seasonality_mode="multiplicative")
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    aa = plot_plotly(m, forecast)
    # st.write("# Ethereum Coin Price Prediction")
    st.write(aa)

    plot_components_plotly(m, forecast)

    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    st.write("# History of currency with Candlesticks")
    st.write(fig2)

#########################################################################################################
elif rad == "Currency Price Prediction":
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    currency = st.selectbox(
        "Which Currency do you want to predict",
        (
            "ADA-USD",
            "AERGO-USD", 
            "BTC-USD",
            "ETH-USD",
            "XRP-USD",
            "ADA-USD",
            "USDT-USD",
            "DOGE-USD",
            "SOL-USD",
            "MATIC-USD",
            "TRX-USD",
            "STETH-USD",
            "SHIB-USD",
            "LEO-USD",
            "LINK-USD"
                       
        ),
    )
    eth_df = yf.download(currency, start_date, today)
    eth_df.reset_index(inplace=True)
    # eth_df.columns

    df = eth_df[["Date", "Open"]]

    new_names = {
        "Date": "ds",
        "Open": "y",
    }

    fig = go.Figure()


    # Set title
    fig.update_layout(
        title_text="Time series plot of currency open price",
    )
    fig2 = go.Figure(
        data=[
            go.Candlestick(
                x=eth_df["Date"],
                open=eth_df["Open"],
                high=eth_df["High"],
                low=eth_df["Low"],
                close=eth_df["Close"],
            )
        ]
    )
    # st.write("# History of Ethereum with Candlesticks")

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    df.rename(columns=new_names, inplace=True)

    x = df["ds"]
    y = df["y"]
    # st.area_chart(y)

    bb = fig.add_trace(go.Scatter(x=x, y=y))
    # st.write("# History of Ethereum")

    if df["y"].count() < 2:
        st.error("Insufficient data to perform time series analysis.")
    else:
        m = Prophet(seasonality_mode="multiplicative")
        m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    aa = plot_plotly(m, forecast)
    st.write("# Currency Price Prediction")
    st.write(aa)

elif rad == "Custom":
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    currency = st.selectbox(
        "Which Currency do you want to predict",
        (
            "ADA-USD",
            "AERGO-USD", 
            "BTC-USD",
            "ETH-USD",
            "XRP-USD",
            "ADA-USD",
            "USDT-USD",
            "DOGE-USD",
            "SOL-USD",
            "MATIC-USD",
            "TRX-USD",
            "STETH-USD",
            "SHIB-USD",
            "LEO-USD",
            "LINK-USD"
                       
        ),
    )

    eth_df = yf.download(currency, start_date, today)
    eth_df.reset_index(inplace=True)
    # eth_df.columns

    df = eth_df[["Date", "Open"]]

    new_names = {
        "Date": "ds",
        "Open": "y",
    }

    df.rename(columns=new_names, inplace=True)

    # plot the open price

    x = df["ds"]
    y = df["y"]
    # st.area_chart(y)
    fig = go.Figure()

    bb = fig.add_trace(go.Scatter(x=x, y=y))
    # st.write("# History of Ethereum")

    # Set title
    fig.update_layout(
        title_text="Time series plot of currency Open Price",
    )
    fig2 = go.Figure(
        data=[
            go.Candlestick(
                x=eth_df["Date"],
                open=eth_df["Open"],
                high=eth_df["High"],
                low=eth_df["Low"],
                close=eth_df["Close"],
            )
        ]
    )
    # st.write("# History of Ethereum with Candlesticks")

    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    m = Prophet(seasonality_mode="multiplicative", changepoint_range=1, changepoint_prior_scale = 0.75)

    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    aa = plot_plotly(m, forecast)

    strdate = st.date_input("Enter Date")
    # datetimeobj=datetime.strptime(strdate,"%y-%m-%d")
    #
    for i in forecast.index:
        if strdate == forecast["ds"][i]:
            st.write(
                "## Currency Price on",
                forecast["ds"][i],
                "is",
                forecast["yhat"][i],
                "United States Dollar",
                "and",
                forecast["yhat"][i] * 82.1,
                "in Indian Rupee",
            )

else:
    st.balloons()
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)

    st.success("Thank you")
# st.markdown(footer, unsafe_allow_html=True)
