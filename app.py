from neuralintents.assistants import BasicAssistant
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yfin
from portopt import *
import mplfinance as mpf
import pickle 
import sys
import datetime as dt 
from datetime import date

portfolio={"AAPL": 20, "TSLA": 10, "GS": 5}

with open('portfolio.pkl', 'rb') as f:
    portfolio=pickle.load(f)

def save_portfolio():
    with open('portfolio.pkl','wb') as f:
        pickle.dump(portfolio,f)

def add_portfolio():
    ticker=input('Which stock do you want to add:')
    amount=input('How many shares to add:')

    if ticker in portfolio.keys():
        portfolio[ticker]+=int(amount)
    else:
        portfolio[ticker]=int(amount)

    save_portfolio()

def remove_portfolio():
    ticker=input('Which stock do you want to sell:')
    amount=input('How many shares to sell:')

    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker]-=int(amount)
        else:
            print('You dont have enough shares of {ticker}')
    else:
        print(f'You dont have any shares of {ticker}')
    save_portfolio()

def show_portfolio():
    print("Your Portfolio has:")
    for ticker in portfolio.keys():
        print(f'{ticker}: {portfolio[ticker]}'+' shares' )

def portfolio_worth():
    sum=0
    yfin.pdr_override()
    for ticker in portfolio.keys():
        data=pdr.get_data_yahoo(ticker)
        print(f"{ticker}:",data)
        price=data['Close'].iloc[-1]
        sum+=int(price)*portfolio[ticker]
    print(f"Portfolio worth is {sum} USD")

def portfolio_gains():
    starting_date=input('Enter date for comparison (YYYY-MM-DD)')
    end_date=date.today()
    yfin.pdr_override()

    sum_now=0
    sum_then=0

    try:
        for ticker in portfolio.keys():
            data=pdr.get_data_yahoo(ticker, start=starting_date)
            price_now=data['Close'].iloc[-1]
            price_then=data.loc[data.index == starting_date]['Close'].values[0]
            sum_now+=int(price_now)
            sum_then+=int(price_then)
        print(f'Relative gains: {((sum_now-sum_then)/sum_then)*100}%')
        print(f'Absolute gains: {(sum_now-sum_then)} USD')
    except:
        print('There was no trading on this day')


def plot_chart():
    ticker=input('Choose a ticker symbol:')
    starting_date=input('Choose a start date (DD/MM/YYYY):')

    yfin.pdr_override()

    plt.style.use('dark_background')
    start=dt.datetime.strptime(starting_date, "%d/%m/%Y")
    end=dt.datetime.now()

    data=pdr.get_data_yahoo(ticker, start=start, end=end)

    colors=mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')

    mpf_style=mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    mpf.plot(data,type='candle', style=mpf_style, volume=True)

def bye():
    print("Goodbye!")
    sys.exit(0)

def hi():
    print("Hi!")

def optimize():
    shares = []
    for ticker in portfolio.keys():
        shares.append(ticker)
    portfolio_optimization(shares)

mappings={
    'greetings': hi,
    'plot_chart':  plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'optimize': optimize,
    'bye': bye
}

assistant=BasicAssistant('intents.json', mappings)

assistant.fit_model(epochs=50)
assistant.save_model()

while True:
    msg=input('')
    assistant.process_input(msg)
