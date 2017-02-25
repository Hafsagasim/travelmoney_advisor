# Travel money advisor API
## Using machine learning to predict currency exchange rate

## Currently available rates:
				 * USD : USD/HUF
                 * GBP : GBP/HUF
                 * EUR : EUR/HUF
                 * PLN : GBP/PLN

## Endpoints:
### Available currencies:
* GET /currencies

###Forecast a specific CURRENCY for X days:
* POST /forecast
	expected JSON format : 
	{ 
	"currency" : "CURRENCY",
    "days": X
    }
* Example response:
	{
	 'lasknownrate': '307.75', 
	 'forecasts': '[ 307.88528343  308.23194486  307.96452032  308.14280335  307.8654742 ]', 
	 'accuracy': '0.975319053163'
	 }
	 
[Will be hosted here:](http:\\laszlo.szoboszlai.me "Laszlo's page")
