# Ultish-Cryptocurrency-Price-Prediction

## Models Employed (Currently)
1. ARIMA Model
2. Support Vector
3. Random Forests

## Dataset
The dataset is taken from Yahoo Finance, originally hosted by CoinMarketCap.

## Interfacing
Currently, interfacing of two models (ARIMA and Support Vector) is done through Streamlit Web Application for hosting Machine Learning Models

## Outputs (For a Single Ticker)
1. Monthwise High-Low Prices
<img width="779" alt="Monthwise Hi_Low" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/a8b411c0-6186-4f20-a8a3-0cdfbb4dd0cd">



### 1. Support Vectors
<img width="629" alt="SVR_Crypto1" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/e0fea51b-60c9-4e93-ae94-c200d9930fed">
<img width="554" alt="SVR_Crypto2" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/f73548df-a0ed-4c0a-8adb-02b4cb621c9c">

### 2. ARIMA Model
<img width="542" alt="Arima Crypto_1" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/de67e80d-41a4-4a01-8e35-0ac62ef58045">

### 3. Random Forest (Output via Notebook)
![Random Forest](https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/2744b51d-4a71-4a35-abb3-9c2691bc33a4)

## Evaluation
Evaluation is done through the `R2` metric score. Out of these three models, Random Forest achieves the Highest scoring(closest to 1). However, fine tuning needs to be included so as to decrease the error rate of these models.

## References
1. [Crypto Finance Dataset From Yahoo](https://finance.yahoo.com/crypto/)

2. [Stock Price Prediction](https://www.youtube.com/watch?v=0E_31WqVzCY&t=241s&pp=ygU2Y3J5cHRvY3VycmVuY3kgcHJpY2UgcHJlZGljdGlvbiB1c2luZyBtYWNoaW5lIGxlYXJuaW5n)

## What's Next ?
1. For cryptocurrency prediction, which includes time series analysis, these three models were found to be a good fit for prediction. However, ARIMA model does'nt perform well as expected, it's improved version `(SARIMA)` maybe taken into consideration for better results.]
2. These models right now contain a single or few cryptocurrency for user to choose from. In future commit, the top 100 cryptocurrencies will be included for selection.
3. One of the models, namely `Facebook's Prophet` is also a very well known model and I'll try to include that particular model for measuring it's accuracy.
4. Out of all testing models, one particular model with best results will be chosen for final commit.
5. Rest of the work follows the Web Interfacing part via streamlit. 


