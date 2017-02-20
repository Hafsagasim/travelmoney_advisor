import pandas as pd
import quandl, math, datetime, os, platform, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
import pickle

style.use('ggplot')
quandl.ApiConfig.api_key = 'EsjaNdxJTou8w47JBWLe'


######################
#  Data preparation  #
######################
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
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

def download_data():
    #dfUSD = quandl.get('BOE/XUDLBK35')
    #dfGBP = quandl.get('BOE/XUDLBK33')
    dfEUR = quandl.get('BOE/XUDLBK34')

   # df = pd.concat([dfUSD, dfEUR], axis=1)
   # df = pd.concat([df, dfGBP], axis=1)
    df= dfEUR
    df.columns= ['GBP']

    df.to_csv('currency.dat', sep='\t', encoding='utf-8')
    return df

    #print('Currency info saved to: currency.dat')


def load_data(filename):
    #logic to download new data if the saved data is too old
    refresh_interval = 86400 #86400 sec = 1 day
    if bool(math.floor(((time.time() - creation_date(filename)) / refresh_interval ))):
        download_data()
    return pd.read_csv(filename, sep='\t')

df = download_data()
temp_df = load_data('currency.dat')

df = df[['GBP']]

##############################
#      Machine learning      #
##############################

# currency to forecast
forecast_col = 'GBP'
df.fillna(-99999, inplace = True)
#how many days to forecast for
forecast_out = 10

df['label'] = df[forecast_col].shift(-forecast_out)

df = df [['GBP','label',]]

x = np.array(df.drop(['label'],1))

x = preprocessing.scale(x)
x = x[:-forecast_out]
x_lately = x[-forecast_out:]
df.dropna(inplace = True)
y = np.array(df['label'])

x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y, test_size=0.2)
clf = LinearRegression(n_jobs= -1) #n_jobs makes it threaded -1 as many as possible

clf.fit(x_train, y_train)
#saving classsifier after training
with open('linreg_currency.pickle','wb') as f:
    pickle.dump(clf,f)

#load the classifier:
#pickle_in = open('linreg_currency.pickle','rb')
#clf = pickle.load(pickle_in)

accuracy = clf.score(x_test, y_test)

forecast_set = clf.predict(x_lately)
print('The forecast is for ' + str(forecast_out) + ' days.')
print('The accuracy is: ' +  str(accuracy))
print('The forecast:')
print(forecast_set)

#plotting
df['Forecast'] = np.nan

print(temp_df.iloc[-1].Date)
last_date = datetime.strptime(temp_df.iloc[-1].Date, '%Y-%m-%d')
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix +one_day

for i in forecast_set:
    next_date = datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['GBP'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()


