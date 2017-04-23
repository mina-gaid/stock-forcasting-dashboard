from django.shortcuts import render
from .stock_prices_test import stock_prices
import quandl
import matplotlib.pyplot as plt
import uuid
import os
import datetime
import csv
import sys
from numpy import loadtxt

auth_tok = ("DieXgiWyjrFVyh3EdxjG")


def codes(request):
    """
    This function searches the SP500 csv file to see if it a company matches that query.
    """
    csv_file = csv.reader(open('SP500.csv', "r"), delimiter=",")
    next(csv_file)

    if request.GET.get('ticker'):

        ticker = request.GET.get('ticker').lower()
        print(ticker)
        results = []
        for row in csv_file:
            if ticker in row[0].lower() or ticker in row[1].lower() or ticker in row[2].lower():
                print(row)
                results.append(row)
        if results:
            return render(request, 'dashboard/tickers.html', {'tickers': results})
        else:
            return render(request, 'dashboard/tickers.html')


    else:
        return render(request, 'dashboard/tickers.html', {'tickers': csv_file})


def panel(request):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    if request.GET.get('stockName'):
        try:
            stock_name = request.GET.get('stockName')
        except:
            return render(request, 'dashboard/tables.html', {'error': 'Incorrect code.'})
    else:
        stock_name = 'WIKI/GOOGL'

    df = quandl.get(stock_name, start_date=week_ago, end_date=today)
    df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
    table = df.tail().to_html(classes="table table-bordered table-responsive", border=0)
    return render(request, 'dashboard/control-panel.html', {'table': table, 'stock_name': stock_name})


def tables(request):
    if request.GET.get('stockName'):
        try:
            stock_name = request.GET.get('stockName')
            prices = stock_prices(stock_name)
        except:
            return render(request, 'dashboard/tables.html', {'error': 'Incorrect code.'})
    else:
        
        stock_name = 'WIKI/GOOGL'
        prices = stock_prices()
    return render(request, 'dashboard/tables.html', {'prices': prices, 'name': stock_name})


def charts(request):
    if request.GET.get('stockName'):
        stock_name = request.GET.get('stockName')
        df = quandl.get(stock_name, authtoken=auth_tok)
        df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
        df['Adj. Open'].plot()
        df['Adj. Close'].plot()
        plt.xlabel('Date')
        plt.ylabel('Price')
        ud = str(uuid.uuid4())
        image = '/static/images/' + ud + '.png'
        dir_name = os.getcwd() + '/dashboard' + image
        plt.savefig(dir_name)
        return render(request, 'dashboard/charts.html', {'image': image})
    return render(request, 'dashboard/charts.html')
