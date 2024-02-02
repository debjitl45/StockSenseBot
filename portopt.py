import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import yfinance as yfin

def portfolio_optimization(shares):
    tickers_list = shares
    print(shares)

    data = yfin.download(tickers_list,'2022-1-1','2024-1-1')['Close']

    # Print first 5 rows of the data
    print(data)

    # convert df to csv
    data.to_csv('data.csv')

    # Read in price data
    df = pd.read_csv('data.csv', index_col=0, parse_dates=True)

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights.csv")  # saves to file
    print(cleaned_weights)
    ef.portfolio_performance(verbose=True)


