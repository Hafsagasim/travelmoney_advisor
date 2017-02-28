import pandas as pd
import quandl, math, datetime, os, platform, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
import pickle

currencies = {
                'USD' : 'BOE/XUDLBK35',
                'GBP' : 'BOE/XUDLBK33',
                'EUR' : 'BOE/XUDLBK34',
                'PLN' : 'BOE/XUDLBK47',
                'BGN' : 'BOE/EURBGN'
             }

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

def download_data(currency, save = False, silent = True ):
    '''Function to download currency data from Quandl site.
        currency = the name of the currency to download
        save = if True saves the data in 'CURRENCYNAME'.csv file, default = False
        silent = if False, prints logs on stdout, default = True
        returns dataframe
    '''
    df = quandl.get(currencies[currency])
    df.columns= [currency]

    if save:
        df.to_csv(currency + '.csv', sep='\t', encoding='utf-8')
        if not silent:
            print('Currency info saved to:' + currency + '.csv')
    return df

def load_data(currency, save = False, silent = True, refresh_interval = 1):
    '''Function to download new data if the saved data is "too old" .
       Use this instead of download_data for cacheing.
        currency = the name of the currency to load
        save = passes it to download_data if its called.
        silent = if False, prints logs on stdout, default = True
        refesh_interval = sets the interval in days
        returns dataframe
    '''
    #turn days into seconds
    refresh_interval = refresh_interval * 86400
    filename = currency + '.csv'

    if bool(math.floor(((time.time() - creation_date(filename)) / refresh_interval ))):
        if not silent:
            print('Download of ' + filename + ' triggered.')
        download_data(currency, save, silent)
    return pd.read_csv(filename, sep='\t')

def lin_reg_predict(currency, forecast_out, save_ds = False,savemodel = False, silent = True, cache = True,
                    train_a_lot = 1, retrain = False, refresh_interval = 1,):
    '''
    Function to predict out future currency rates.
    :param currency: the currency we want prediction for.
    :param forecast_out: the number of days we want the prediction for.
    :param save_ds: triggers cacheing of newly downloaded dataset.
    :param savemodel: triggers saving the classifier.
    :param silent: turns logging to stdout on.
    :param cache: use load instead of download
    :param retrain: forces the retrain of the model
    :param train_a_lot: number of times it trains the model to get best performing one
    :param refresh_interval: refresh interval in days of the dataset if cacheing is on
    :return:
    '''
    df = load_data(currency, save_ds, silent, refresh_interval) if cache else download_data(currency, save_ds, silent)

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

    currency_file = 'linreg_' + currency + '.pickle'
    #the model needs saving if the model for currency does not exist
    needs_saving = not os.path.isfile('./' + currency_file) or savemodel

    if needs_saving or retrain:
        #if retrain is triggered the minimum training = 10
        if retrain:
            train_a_lot = max(10, train_a_lot)
        scores = {}
        #train the classifier train_a_lot times (default = 1), and chose the optimal to be the model
        # for train in train_a_lot:
        if not silent:
            print('Training the model ' + str(train_a_lot) + ' time(s).')
        for i in range(train_a_lot):
            x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y, test_size=0.2, random_state=0)
            clf = LinearRegression(n_jobs= -1) #n_jobs makes it threaded -1 as many as possible
            clf.fit(x_train, y_train)
            #scores[( cross_validation.cross_val_score(clf, x, y, scoring='mean_squared_error', cv=loo,))] = clf
            scores [clf.score(x_test, y_test).mean()] = clf
        if not silent:
            print('The accuracies: ' + str(scores.keys()))
        score =  max(scores)
        model = max(scores, key=scores.get)
    else:
        if not silent:
            print('Loading model from file.')
        pickle_in = open(currency_file,'rb')
        model = pickle.load(pickle_in)


    #save the best model after training
    if needs_saving:
        with open(currency_file,'wb') as f:
            pickle.dump(model,f)
        if not silent:
            print('Model saved as : ' + currency_file)

    if not silent:
        print('Creating forecast.')
    forecast_set = clf.predict(x_lately)

    if not silent:
        print('Generating response.')

    lastknownrate = str(df.iloc[-1]['label'])
    accuracy = str(score)
    forecasts = str(forecast_set)

    return {'lasknownrate' : lastknownrate,
            'accuracy' : accuracy,
            'forecasts' : forecasts}
def main():
    currency = 'EUR'
    forecast_out = 5
    prediction = lin_reg_predict(currency, forecast_out, save_ds=True, savemodel=True, silent=False, cache=False,
                    train_a_lot=10, retrain=False, refresh_interval=1)
    print(prediction)

if __name__ == "__main__":
    main()