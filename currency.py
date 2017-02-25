import pandas as pd
import quandl, math, datetime, os, platform, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
import pickle
from flask import Flask, jsonify, request

app = Flask(__name__)

style.use('ggplot')

currencies = {
                'USD' : 'BOE/XUDLBK35',
                'GBP' : 'BOE/XUDLBK33',
                'EUR' : 'BOE/XUDLBK34',
                'PLN' : 'BOE/XUDLBK47'
            }

######################
#  Data preparation  #
######################
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def download_data(currency, save = False ):
    df = quandl.get(currencies[currency])

    #df = pd.concat([dfUSD, dfEUR], axis=1)
   # df = pd.concat([df, dfGBP], axis=1)
    #df= dfGBP
    df.columns= [currency]

    if save:
        df.to_csv('currency.dat', sep='\t', encoding='utf-8')
    return df

    #print('Currency info saved to: currency.dat')


def load_data(filename):
    #logic to download new data if the saved data is too old
    refresh_interval = 86400 #86400 sec = 1 day
    if bool(math.floor(((time.time() - creation_date(filename)) / refresh_interval ))):
        download_data()
    return pd.read_csv(filename, sep='\t')

@app.route("/currencies", methods=['GET'])
def get_currencies():
    return jsonify(currencies)

#expecting : { 'currency' : 'EUR', 'days':5} format
@app.route("/forecast", methods=['POST', 'GET'])
def forecast():

    if not request.json or not 'currency' in request.json:
        abort(4)
    currency = request.json['currency']
    forecast_out = int(request.json['days'])

    df = download_data(currency)
    #temp_df = df
    #temp_df = download_data(currency)

    #print('Last known rate:')
    #print(df.iloc[-1])

    df = df[[currency]]

    # currency to forecast
    forecast_col = currency
    df.fillna(-99999, inplace = True)
    #how many days to forecast for

    df['label'] = df[forecast_col].shift(-forecast_out)

    df = df [[currency,'label',]]

    x = np.array(df.drop(['label'],1))

    x = preprocessing.scale(x)
    x = x[:-forecast_out]
    x_lately = x[-forecast_out:]
    df.dropna(inplace = True)
    y = np.array(df['label'])

    x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y, test_size=0.2, random_state=0)
    clf = LinearRegression(n_jobs= -1) #n_jobs makes it threaded -1 as many as possible

    clf.fit(x_train, y_train)
    #scores = cross_validation.cross_val_score(clf, x, y, cv=5)
    scores = clf.score(x_test, y_test)
    #saving classsifier after training
    #if saveclf:
    #    with open('linreg_currency.pickle','wb') as f:
    #        pickle.dump(clf,f)

    #load the classifier:
    #pickle_in = open('linreg_currency.pickle','rb')
    #clf = pickle.load(pickle_in)

    #accuracy = clf.score(x_test, y_test)

    forecast_set = clf.predict(x_lately)
    #print('The forecast is for ' + str(forecast_out) + ' days.')

    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    #print('The forecast:')
    #print(forecast_set)

    response = {
        'lastknownrate': str(df.iloc[-1]['label']),
        'accuracy': str(scores),
        'deviation' :  str(scores.std() * 2),
        'forecasts' : str(forecast_set)
    }

    return jsonify(response), 201

def plot_forecast(currency, df):
    temp_df = download_data(currency)
    df['Forecast'] = np.nan
    print(temp_df.iloc[-1])
    last_date = datetime.strptime(temp_df.iloc[-1].Date, '%Y-%m-%d')
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix +one_day

    for i in forecast_set:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += one_day
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
    df[currency].plot()
    df['Forecast'].plot()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

def main():
    df = forecast('USD')
    #plot_forecast('USD', df)

if __name__ == "__main__":
    #main()
    app.run()