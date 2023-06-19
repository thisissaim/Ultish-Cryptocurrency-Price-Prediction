# Importing dataframe, math and Datetime libraries.
import pandas as pd
import numpy as np 
import datetime as dt
from sklearn.metrics import  r2_score 
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# Yahoo finance data connector for fetching the data.
import yfinance as yf

start = dt.date(2015,1,1)
end = dt.date.today().strftime("%Y-%m-%d")
ticker = 'BTC-USD'
df = yf.download(ticker,start,end)

df.insert(0,'Date',df.index)
df.reset_index(drop= True, inplace= True)

df.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close"}, inplace= True)

df.sort_values(by='date', inplace=True)

monthvise= df.groupby(df['date'].dt.strftime('%B,%Y'))[['open','close']].mean().sort_values(by='close')
monthvise.head(12)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['open'],
    name='Crypto Open Price',
    marker_color='teal'
))
fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['close'],
    name='Crypto Close Price',
    marker_color='lightsalmon'
))

fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title='Monthwise comparision between Crypto actual, open and close price')
fig.show()

names = cycle(['Crypto Open Price','Crypto Close Price','Crypto High Price','Crypto Low Price'])

fig = px.line(df, x=df.date, y=[df['open'], df['close'], df['high'], df['low']], labels={'date': 'Date','value':'Crypto value'})
fig.update_layout(title_text='Crypto analysis chart', font_size=15, font_color='black',legend_title_text='Crypto Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(names)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

fig.show()

closedf = df[['date','close']]
print("Shape of close dataframe:", closedf.shape)

close_Crypto = closedf.copy()
del closedf['date']
scaler=MinMaxScaler(feature_range=(0,1))
closedf=scaler.fit_transform(np.array(closedf).reshape(-1,1))
print(closedf.shape)

training_size=int(len(closedf)*0.80)
test_size=len(closedf)-training_size
train_data,test_data=closedf[0:training_size,:],closedf[training_size:len(closedf),:1]
print("train_data: ", train_data.shape)
print("test_data: ", test_data.shape)

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 15
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

print("X_train: ", X_train.shape)
print("y_train: ", y_train.shape)
print("X_test: ", X_test.shape)
print("y_test", y_test.shape)


regressor = RandomForestRegressor(n_estimators = 1200, random_state = 0)
regressor.fit(X_train, y_train)

# Prediction 

train_predict=regressor.predict(X_train)
test_predict=regressor.predict(X_test)

train_predict = train_predict.reshape(-1,1)
test_predict = test_predict.reshape(-1,1)

print("Train data prediction:", train_predict.shape)
print("Test data prediction:", test_predict.shape)

# Transform back to original form

train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
original_ytrain = scaler.inverse_transform(y_train.reshape(-1,1)) 
original_ytest = scaler.inverse_transform(y_test.reshape(-1,1))

print("Train data R2 score:", r2_score(original_ytrain, train_predict))
print("Test data R2 score:", r2_score(original_ytest, test_predict))