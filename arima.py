import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
import numpy as np
import pmdarima as pm
import datetime


def arima(crypto_name, data):
    df_close = data['Close']

    # Split data into train and test set (90% - train, 10% - test)
    df_log = df_close
    train_data, test_data = df_log[3:int(len(df_log) * 0.9)], df_log[int(len(df_log) * 0.9):]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train_data.index, y=train_data, mode='lines+markers', name='train'))
    fig.add_trace(go.Scatter(x=test_data.index, y=test_data, mode='lines+markers', name='test'))
    fig.update_layout(title=f'{crypto_name} ARIMA Data',
                      xaxis_title='Date',
                      yaxis_title='Crypto Price')
    st.plotly_chart(fig)

    model = pm.auto_arima(df_log, start_p=0, d=None, start_q=0, max_p=5, max_d=5, max_q=5, start_P=0, D=1, start_Q=0, max_P=5, max_D=5, max_Q=5, m=7, seasonal=True, error_action='warn', trace=True, suppress_warnings=True, stepwise=True, random_state=20, n_fits=50)
    model.summary()

    preds = model.predict(n_periods=22)

    hist_data = yf.download(crypto_name, start="2021-04-01", end="2021-05-04")
    hist_data = hist_data['Close']

    rmse = np.sqrt(np.mean(((preds - hist_data) ** 2)))
    st.write(f'RMSE ARIMA: {rmse}')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data, mode='lines+markers', name='historical'))
    fig.add_trace(go.Scatter(x=hist_data.index, y=preds, mode='lines+markers', name='predictions'))
    fig.update_layout(title=f'{crypto_name} ARIMA Prediction',
                      xaxis_title='Date',
                      yaxis_title='Crypto Price')
    st.plotly_chart(fig)

    return preds, rmse


st.title("ARIMA Crypto Price Prediction")
crypto_name = st.sidebar.text_input("Crypto Ticker", "ETH-USD")
start_date = st.sidebar.text_input("Start Date (YYYY-MM-DD)", "2020-03-26")
end_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Set end date as current date


data = yf.download(crypto_name, start=start_date, end=end_date)
preds, rmse = arima(crypto_name, data)

st.write("Predictions:", preds)
st.write("RMSE:", rmse)
