import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression

def stock_prices(stock='WIKI/GOOGL'):
    auth_tok = ("DieXgiWyjrFVyh3EdxjG")
    df = quandl.get(stock, authtoken=auth_tok)
    print(df.columns.values)
    df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
    df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
    df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

    df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

    forecast_col = 'Adj. Close'
    df.fillna(-99999, inplace=True)

    forecast_out = int(math.ceil(0.1 * len(df)))
    print('Forecast')
    print(forecast_out)

    df['label'] = df[forecast_col].shift(-forecast_out)

    X = np.array(df.drop(['label'], 1))
    X = preprocessing.scale(X)
    X_Lately = X[-forecast_out:]
    X = X[:-forecast_out:]

    df.dropna(inplace=True)  # drop missing data when creating labels
    y = np.array(df['label'])  # applying y label
    y = np.array(df['label'])  # applying y label

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

    clf = LinearRegression(n_jobs=1)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)
    forecast_set = clf.predict(X_Lately)
    # print(forecast_set, accuracy, forecast_out)  # printing predicted stock prices for next 30 days
    df['Forecast'] = np.nan

    # getting dates
    Last_date = df.iloc[-1].name
    Last_unix = Last_date.timestamp()
    random_day = 86400
    next_unix = Last_unix + random_day

    # populate data frame with new dates and forecast values
    for i in forecast_set:  # taking each forecast and setting it as the value in dataframe
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += random_day
        df.loc[next_date] = [' ' for _ in range(len(df.columns) - 1)] + [
            i]  # takes all columns and sets to not a numbers
    
    df = df[['Forecast']]
    return df.tail().to_html(classes="table table-bordered table-responsive", border=0)
