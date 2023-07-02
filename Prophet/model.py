import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings
import time


warnings.filterwarnings("ignore")
pd.options.display.float_format = "${:,.2f}".format
today = datetime.today().strftime("%Y-%m-%d")
start_date = "2020-01-01"


def calculate_moving_average(df, window):
    df['Moving Average'] = df['Close'].rolling(window=window).mean()
    return df

rad = st.sidebar.radio(
    "Menu",
    [
        "Homepage",
        "Graphical Representation of Price",
        "Moving Average",
        "Currency Price Prediction",
        "Purchase/Sell Timing",
        "Peaks and Valleys",
        "Correlation",
    ],
)
if rad == "Homepage":

    st.title("Cryptocurrency Price Prediction")

    st.markdown("<h1 style='text-align: center; color: white;'>Cryptocurrency Price Prediction</h1>", unsafe_allow_html=True)


    st.markdown(""" 
    ##  Contents
    ### Graphical Representation of Price
    ###  Moving Average
    ###  Currency Price Prediction
    ###  Purchase/Sell Timing
    ###  Peaks and Valleys
    ###  Correlation
    """,True)

elif rad == "Graphical Representation of Price":
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


    df = eth_df[["Date", "Close"]]
    df = df.rename(columns={"Date": "ds", "Close": "y"})


    x = df["ds"]
    y = df["y"]




    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    st.write("# History of currency with Candlesticks")
    st.write(fig2)
    st.write("### Move the slider to select the range of prices of historical dataset")

elif rad == "Moving Average":
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
    window = st.slider("Moving Average Window", min_value=1, max_value=30, value=7, step=1)
    eth_df = yf.download(currency, start_date, today)
    eth_df.reset_index(inplace=True)

    eth_df = calculate_moving_average(eth_df, window)  # Calculate moving average

    

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=eth_df["Date"], y=eth_df["Close"], name="Close Price"))
    fig3.add_trace(go.Scatter(x=eth_df["Date"], y=eth_df["Moving Average"], name="Moving Average"))
    fig3.update_layout(title_text="History of currency with Moving Average")
    st.plotly_chart(fig3)


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
    m = Prophet(seasonality_mode="multiplicative")
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")


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

    if df["y"].count() < 2:
        st.error("Insufficient data to perform time series analysis.")
    else:
        m = Prophet(seasonality_mode="multiplicative")
        m.fit(df)

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")


    aa = plot_plotly(m, forecast)
    st.write("# Currency Price Prediction")
    st.write(aa)




elif rad == "Purchase/Sell Timing":
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

    df = eth_df[["Date", "Open"]]

    new_names = {
        "Date": "ds",
        "Open": "y",
    }

    df.rename(columns=new_names, inplace=True)

    x = df["ds"]
    y = df["y"]

    if df["y"].count() < 2:
        st.error("Insufficient data to perform time series analysis.")
    else:
        m = Prophet(seasonality_mode="multiplicative")
        m.fit(df)

        # Calculate the date range for 2 years starting from today
        future_start_date = datetime.today()
        future_end_date = (future_start_date + relativedelta(years=2)).strftime("%Y-%m-%d")
        
        future = pd.date_range(start=future_start_date, end=future_end_date)

        future_df = pd.DataFrame({"ds": future})

        forecast = m.predict(future_df)

        st.write("# Currency Price Prediction")

        # Find the index of the lowest and highest predicted prices
        lowest_price_index = forecast["yhat"].idxmin()
        highest_price_index = forecast["yhat"].idxmax()

        # Extract the corresponding dates
        lowest_price_date = forecast.loc[lowest_price_index, "ds"]
        highest_price_date = forecast.loc[highest_price_index, "ds"]

        # Display the results
        # st.write(f"## Best time to purchase {currency} coin: {lowest_price_date}")
        # st.write(f"## Best time to sell {currency} coin: {highest_price_date}")

        st.write(f"## Best time to purchase: {lowest_price_date}")
        st.write(f"## Best time to sell: {highest_price_date}")

        aa = plot_plotly(m, forecast)
        st.write(aa)

elif rad == "Peaks and Valleys":
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


    # Perform future predictions
    future_dates = pd.date_range(start=today, periods=365)  # Future dates for prediction (1 year)
    future_df = pd.DataFrame({"ds": future_dates})

    prophet_df = eth_df[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet()
    model.fit(prophet_df)
    future_prices = model.predict(future_df)["yhat"]

    future_df["yhat"] = future_prices
    future_max_price = future_df["yhat"].max()
    future_min_price = future_df["yhat"].min()

    st.write("### Predictive Highest Price(Over Span of Two Years):", future_max_price)
    st.write("### Predictive Lowest Price(Over Span of Two Years):", future_min_price)


   

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
    for i in range(20):
        st.write('')

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

elif rad == "Correlation":
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)
    crypto_list = [
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
        "LINK-USD",
        ]
    crypto_data = {}
    for crypto in crypto_list:
        df = yf.download(crypto, start="2021-01-01", end=datetime.today().strftime("%Y-%m-%d"))
        crypto_data[crypto] = df

# Calculate correlation matrix
    correlation_matrix = pd.DataFrame(index=pd.Index(crypto_list), columns=crypto_list)

    for crypto1 in crypto_list:
        for crypto2 in crypto_list:
            correlation = crypto_data[crypto1]["Close"].corr(crypto_data[crypto2]["Close"])
            correlation_matrix.loc[crypto1, crypto2] = correlation

# Get the top 10 positive and negative correlated cryptocurrencies
    top_positive_correlated = correlation_matrix.unstack().sort_values(ascending=False)[:10]
    top_negative_correlated = correlation_matrix.unstack().sort_values()[:10]

# Create Streamlit app
    st.title("Positive and Negative Correlated Cryptocurrencies")
    st.subheader("Top 10 Positive Correlations:")
    st.table(top_positive_correlated)
    st.subheader("Top 10 Negative Correlations:")
    st.table(top_negative_correlated)

# Visualize correlation matrix as heatmap
    fig = go.Figure(data=go.Heatmap(z=correlation_matrix.values,
                                   x=correlation_matrix.columns,
                                   y=correlation_matrix.index,
                                   colorscale="RdBu",
                                   colorbar=dict(title="Correlation")))
    fig.update_layout(title="Cryptocurrency Correlation Matrix")
    st.plotly_chart(fig)
else:
    st.balloons()
    progress = st.progress(0)
    for i in range(0, 2):
        time.sleep(0.2)
        progress.progress((i + 1) * 100 - 100)

    st.success("Thank you")
# st.markdown(footer, unsafe_allow_html=True)
