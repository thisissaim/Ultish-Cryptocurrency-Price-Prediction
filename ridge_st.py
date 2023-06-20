import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
import plotly.graph_objects as go



# Set page title
st.set_page_config(page_title="Cryptocurrency Price Prediction")

# Title
st.title("Cryptocurrency Price Prediction")

# Cryptocurrency selection
crypto = st.sidebar.selectbox("Select Cryptocurrency", ["BTC-USD", "ETH-USD", "LTC-USD"])

# Date selection
start_date = st.sidebar.date_input("Start Date", date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Download data
data = yf.download(crypto, start_date, end_date, auto_adjust=True)

# Display raw data
st.subheader("Raw Data")
st.write(data.head())

# Data visualization

# Training and test data split
X = data.drop("Close", axis=1)
Y = data['Close']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# High and Low bar chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['High'],
    name='High',
    marker_color='green'
))
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Low'],
    name='Low',
    marker_color='red'
))

fig.update_layout(
    title='High and Low Prices',
    xaxis_tickangle=-45,
    xaxis_title='Date',
    yaxis_title='Price',
    barmode='overlay'
)

st.subheader("High and Low Prices")
st.plotly_chart(fig)

# Prediction chart
ra = Ridge()
ra.fit(X_train, Y_train)
ra_pred = ra.predict(X_test)

# Actual vs Predicted Price chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index[-len(Y_test):], y=Y_test, mode='lines', name='Actual Price'))
fig.add_trace(go.Scatter(x=data.index[-len(Y_test):], y=ra_pred, mode='lines', name='Predicted Price'))
fig.update_layout(title='Actual vs Predicted Prices', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=True)
st.subheader("Actual vs Predicted Prices")
st.plotly_chart(fig)

# Calculate metrics
mse = mean_squared_error(Y_test, ra_pred)
rmse = np.sqrt(mse)
r2_scores = r2_score(Y_test, ra_pred)

# Display metrics
st.subheader("Model Metrics")
st.write("MSE: ", mse)
st.write("RMSE: ", rmse)
st.write("R2 Score: ", r2_scores)
