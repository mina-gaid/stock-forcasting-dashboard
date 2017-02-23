from django.db import models
import pandas as pd
import os
import quandl, math, datetime
import time
import numpy as np
import random
from statistics import mean
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot') # setting plot style for matplotlib

# Create your models here.

# -------------------------------------------------

# quandl auth tokin
auth_tok = ("DieXgiWyjrFVyh3EdxjG")

# -------------------------------------------------

# data = quandl.get("FRED/GDP", trim_start = "2000-12-12", trim_end = "2016-12-30", authtoken=auth_tok)
# 
# print(data["Adj. Close"])

# -------------------------------------------------

def Stock_price():
	df = pd.DataFrame()
	statspath = path+"_KeyStats"
	stock_list = [x[0] for x in os.walk(statspath) ]
	
	print(stock_list)

	for each_dir in stock_list[1:]:
		try:
			ticker = each_dir.split("\\") [1]
			print(ticker)
			name = "WIKI/"+ticker.upper()
			data = quandl.get(name,
							trim_start = "2000-12-12",
							trim_end = "2016-12-30",
							authtoken=auth_tok)
			data[ticker.upper()] = data["Adj. Close"]
			df = pd.concat([df, data[ticker.upper()]], axis = 1)
			
		except Exception as e:
			print(str(e))
			time.sleep(10)
			try:
				ticker = each_dir.split("\\") [1]
				print(ticker)
				name = "WIKI/"+ticker.upper()
				data = quandl.get(name,
								trim_start = "2000-12-12",
								trim_end = "2016-12-30",
								authtoken=auth_tok)
				data[ticker.upper()] = data["Adj. Close"]
				df = pd.concat([df, data[ticker.upper()]], axis = 1)
				
			except Exception as e:
				print(str(e))
			
			
	# df.to_csv("stock_prices.csv") # output stock_prices to csv file
	
	Stock_price()
	
	sp = Stock_price()
	print(sp)
	
# -------------------------------------------------

df = quandl.get('WIKI/GOOGL', authtoken=auth_tok)
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.1*len(df)))
print(forecast_out)

df['label'] = df[forecast_col].shift(-forecast_out)

print(df.head())

X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X_Lately = X[-forecast_out:]
X = X[:-forecast_out:]

df.dropna(inplace=True) # drop missing data when creating labels
y = np.array(df['label']) # applying y label
y = np.array(df['label']) # applying y label

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=1)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test,y_test)
# print(accuracy) # printing accuracy
forecast_set = clf.predict(X_Lately)
print(forecast_set, accuracy, forecast_out) # printing predicted stock prices for next 30 days
df['Forecast'] = np.nan

# getting dates
Last_date = df.iloc[-1].name
Last_unix = Last_date.timestamp()
random_day = 86400
next_unix = Last_unix + random_day

# populate data frame with new dates and forecast values
for i in forecast_set: # taking each forecast and setting it as the value in dataframe
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += random_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i] # takes all columns and sets to not a numbers

print(df.tail())

# Graphing price by date - Close and Forecast
df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Graphing price by date - Close
df['Adj. Close'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Graphing price by date - Volume
df['Adj. Volume'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# -------------------------------------------------

df = quandl.get('WIKI/GOOGL', authtoken=auth_tok)
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]

# Graphing price by date - Volume
df['Adj. Open'].plot()
df['Adj. Close'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Graphing price by date - Volume
df['Adj. High'].plot()
df['Adj. Low'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# -------------------------------------------------

# Using "random" to create a dataset
def create_dataset(hm,variance,step=2,correlation=False):
    val = 1
    sy = []
    for i in range(hm):
        y = val + random.randrange(-variance,variance)
        sy.append(y)
        if correlation and correlation == 'pos':
            val+=step
        elif correlation and correlation == 'neg':
            val-=step

    sx = [i for i in range(len(sy))]
    
    return np.array(sx, dtype=np.float64),np.array(sy,dtype=np.float64)

# finding best fit slope and intercept of dataset
def best_fit_slope_and_intercept(sx,sy):
    m = (((mean(sx)*mean(sy)) - mean(sx*sy)) /
         ((mean(sx)*mean(sx)) - mean(sx*sx)))
    
    b = mean(sy) - m*mean(sx)

    return m, b

# dataset - coefficient of determination
def coefficient_of_determination(sy_orig,sy_line):
    y_mean_line = [mean(sy_orig) for y in sy_orig]

    squared_error_regr = sum((sy_line - sy_orig) * (sy_line - sy_orig))
    squared_error_y_mean = sum((y_mean_line - sy_orig) * (y_mean_line - sy_orig))

    print(squared_error_regr)
    print(squared_error_y_mean)

    r_squared = 1 - (squared_error_regr/squared_error_y_mean)

    return r_squared

sx, sy = create_dataset(20,10,3,correlation='pos')
m, b = best_fit_slope_and_intercept(sx,sy)
regression_line = [(m*x)+b for x in sx]
r_squared = coefficient_of_determination(sy,regression_line)
print(r_squared)

# ploting the data in a scatter plot
plt.scatter(sx,sy,color='#003F72', label = 'data')
plt.plot(sx, regression_line, label = 'regression line')
plt.legend(loc=4)
plt.show()
