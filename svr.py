# Importing necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import math
import datetime as dt
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from sklearn.preprocessing import MinMaxScaler
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import yfinance as yf

# Streamlit app
def main():
    st.title("Crypto Analysis")
    
    # User input for crypto ticker
    ticker = st.text_input("Enter crypto ticker (e.g., BTC-USD):", "BTC-USD")
    
    # Fetching stock data
    start = dt.date(2015, 1, 1)
    end = dt.date.today().strftime("%Y-%m-%d")
    df = yf.download(ticker, start, end)
    df.insert(0, 'Date', df.index)
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close"}, inplace=True)
    df.sort_values(by='date', inplace=True)
    
    st.subheader("Crypto Data")
    st.write(df)
    
    # Data preprocessing
    closedf = df[['date', 'close']]
    close_stock = closedf.copy()
    del closedf['date']
    scaler = MinMaxScaler(feature_range=(0, 1))
    closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
    
    training_size = int(len(closedf) * 0.80)
    test_size = len(closedf) - training_size
    train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]
    
    # Model training and prediction
    time_step = 15
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)
    
    svr_rbf = SVR(kernel='rbf', C=1e2, gamma='scale')
    svr_rbf.fit(X_train, y_train)
    
    train_predict = svr_rbf.predict(X_train)
    test_predict = svr_rbf.predict(X_test)
    
    train_predict = train_predict.reshape(-1, 1)
    test_predict = test_predict.reshape(-1, 1)
    
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    original_ytrain = scaler.inverse_transform(y_train.reshape(-1, 1))
    original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Evaluation metrics
    train_rmse = math.sqrt(mean_squared_error(original_ytrain, train_predict))
    train_mae = mean_absolute_error(original_ytrain, train_predict)
    test_rmse = math.sqrt(mean_squared_error(original_ytest, test_predict))
    test_mae = mean_absolute_error(original_ytest, test_predict)

    train_r2_score = r2_score(original_ytrain, train_predict)
    test_r2_score = r2_score(original_ytest, test_predict)
    
    # Plotting
    trainPredictPlot = np.empty_like(closedf)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[time_step:len(train_predict) + time_step, :] = train_predict
    
    testPredictPlot = np.empty_like(closedf)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (time_step * 2) + 1:len(closedf) - 1, :] = test_predict
    
    plotdf = pd.DataFrame({'date': close_stock['date'],
                           'original_close': close_stock['close'],
                           'train_predicted_close': trainPredictPlot.reshape(1, -1)[0].tolist(),
                           'test_predicted_close': testPredictPlot.reshape(1, -1)[0].tolist()})
    
    names = cycle(['Original close price', 'Train predicted close price', 'Test predicted close price'])

    
    fig = px.line(plotdf, x=plotdf['date'], y=[plotdf['original_close'], plotdf['train_predicted_close'],
                                                plotdf['test_predicted_close']],
                  labels={'value': 'Stock price', 'date': 'Date'})
    fig.update_layout(title_text='Comparison between original close price vs predicted close price',
                      plot_bgcolor='white', font_size=15, font_color='black', legend_title_text='Close Price')
    fig.for_each_trace(lambda t: t.update(name=next(names)))
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    # Displaying the plots and metrics
    st.subheader("Stock Analysis Chart")
    st.plotly_chart(fig)
    
    st.subheader("Evaluation Metrics")
    # st.write("Train data RMSE:", train_rmse)
    # st.write("Train data MAE:", train_mae)
    # st.write("Test data RMSE:", test_rmse)
    # st.write("Test data MAE:", test_mae)
    st.write("Train data R2 score:", train_r2_score)
    st.write("Test data R2 score:", test_r2_score)

# Convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

if __name__ == "__main__":
    main()
