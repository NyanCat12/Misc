import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statsmodels.api as sm
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_csv('arima.csv', index_col = 0)
df.index.name=None
df.reset_index(inplace=True)
start = datetime.datetime.strptime("2016-06-22", "%Y-%m-%d")
date_list = [start + relativedelta(days=x) for x in range(0,251)]

df['index'] =date_list

df.set_index(['index'], inplace=True)
df.index.name=None
print (df.head(3))

df.columns= ['R2']
df['R2'] = df.R2.apply(lambda x: x)

df.R2.plot(figsize = (12,8))
plt.savefig('test.jpg')

decomposition = seasonal_decompose(df.R2, freq = 7)

decomposition.plot()
#plt.show()
plt.savefig('arima.jpg')


from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries, savename):
    
    #Determing rolling statistics
    rolmean = timeseries.rolling(center=False,window=12).mean()
    rolstd = timeseries.rolling(center=False,window=12).std()

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.savefig(savename)
    
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

test_stationarity(df.R2, 'RollMeanAndStdOfOrigin.jpg')


df.R2_log= df.R2.apply(lambda x: np.log(x))  
test_stationarity(df.R2_log, 'RollMeanAndStdOfLog.jpg')

df['first_difference'] = df.R2 - df.R2.shift(1)  
test_stationarity(df.first_difference.dropna(inplace=False), 'RollMeanAndStdOfFirstDif.jpg')

df['log_first_difference'] = df.R2_log - df.R2_log.shift(1)  
test_stationarity(df.log_first_difference.dropna(inplace=False), 'RollMeanAndStdOfFirstDifLog.jpg')

df['seasonal_difference'] = df.R2 - df.R2.shift(7)  
test_stationarity(df.seasonal_difference.dropna(inplace=False), 'RollMeanAndStdOfSeasonalDif.jpg')

df['log_seasonal_difference'] = df.R2_log - df.R2_log.shift(7)  
test_stationarity(df.log_seasonal_difference.dropna(inplace=False), 'RollMeanAndStdOfSeasonalDifLog.jpg')

df['seasonal_first_difference'] = df.first_difference - df.first_difference.shift(7)  
test_stationarity(df.seasonal_first_difference.dropna(inplace=False), 'RollMeanAndStdOfSeasonalFirstDif.jpg')

df['log_seasonal_first_difference'] = df.log_first_difference - df.log_first_difference.shift(12)  
test_stationarity(df.log_seasonal_first_difference.dropna(inplace=False), 'RollMeanAndStdOfSeasonalFirstDifLog.jpg')


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df.seasonal_first_difference.iloc[8:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df.seasonal_first_difference.iloc[8:], lags=40, ax=ax2)
plt.savefig('Autocorrelation.jpg')

#Building model
mod = sm.tsa.statespace.SARIMAX(df.R2, trend='n', order=(2,1,0), seasonal_order=(1,1,1,7))#To be optimized
results = mod.fit()
print (results.summary())

df['forecast'] = results.predict(start = 230, end= 251, dynamic= True)  
df[['R2', 'forecast']].plot(figsize=(12, 8)) 
plt.savefig('ts_df_predict.png', bbox_inches='tight')
