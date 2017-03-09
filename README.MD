# Travel money advisor API
## Using machine learning to predict currency exchange rate

## Currently available rates:
* EUR -> BGN, GBP, HUF,PLN
* GBP -> HUF, PLN
* USD -> GBP, HUF, PLN

## Endpoints:
### Available currencies to exchange from:
* GET /currencies   
* Returns the available currencies as a JSON 
* [Endpoint: http://laszloszoboszlai.me:5000/currencies](http://laszloszoboszlai.me:5000/currencies "Link to endpoint")

### Available currencies to exchange to:
* POST /tocurrencies   
* Returns the available currencies to translate from a specific curency
* request format : { "currency" : CURRENCY } 
* [Endpoint: http://laszloszoboszlai.me:5000/tocurrencies](http://laszloszoboszlai.me:5000/tocurrencies "Link to endpoint")

###Forecast a specific CURRENCY for X days:
* POST /forecast
	* expected JSON format : 
	* { 
	* "currencyfrom" : "CURRENCY",
	* "currencyto" : "CURRENCY",
    * "days": X
    * }
* Response:
		*   {'lasknownrate' : last known exchange rate (date)
        *    'accuracy' : accuracy of the prediction (float)
        *    'forecasts' : forecasted exchange rates (array of dictionaries of date:rate pairs for easy plotting)
        *    'tosell' : the predicted day for selling the currency (date)
        *    'tobuy' : to predicted day for buying the currency (date)
        *    }
	
* [Endpoint: http://laszloszoboszlai.me:5000/forecast](http://laszloszoboszlai.me:5000/forecast "Link to endpoint")

#Web application screenshot: 
![alt tag](http://laszloszoboszlai.me/travelmoney/main_screen.png)