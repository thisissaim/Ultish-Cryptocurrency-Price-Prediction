# Cryptocurrency-Price-Prediction

## Models Employed (Currently)
1. ARIMA Model
2. Support Vector
3. Random Forests
4. Ridge Regressor
5. Prophet Model by Facebook (Preferred)

## Dataset
The dataset is taken from Yahoo Finance, originally hosted by CoinMarketCap.

## Interfacing
Final Interfacing is done through Streamlit of the Prophet Model.

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


# Second Commit

## Added code file for Ridge Regression
## Added code file for Prophet model. (R2 score = 0.92)
Below is the output of the Prophet model visualization via Streamlit.
<img width="937" alt="a1" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/b82d5239-e2cf-4760-8f0d-9c2b486ad8cb">

<img width="747" alt="a2" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/6e2089eb-f261-457c-9167-fa38fb2b15b3">

![a3](https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/476731a6-f6c2-44f5-a4e1-9f8080e9e291)


<img width="686" alt="a5" src="https://github.com/thisissaim/Ultish-Cryptocurrency-Price-Prediction/assets/78817243/c3dddcd9-a8b4-4409-b945-dbbda991a31b">

## Final Model
The Facebooks's Prophet Model is chosen to be the preferred model for both, its accuracy and simplicity while implementing.

## References
1. [Crypto Finance Dataset From Yahoo](https://finance.yahoo.com/crypto/)

2. [Stock Price Prediction](https://www.youtube.com/watch?v=0E_31WqVzCY&t=241s&pp=ygU2Y3J5cHRvY3VycmVuY3kgcHJpY2UgcHJlZGljdGlvbiB1c2luZyBtYWNoaW5lIGxlYXJuaW5n)

3. [Time Series Analysis with Facebook's Prophet](https://towardsdatascience.com/time-series-analysis-with-facebook-prophet-how-it-works-and-how-to-use-it-f15ecf2c0e3a)

4. [How Does the Prophet Model Works?](https://medium.com/analytics-vidhya/how-does-prophet-work-44addaab6148)
