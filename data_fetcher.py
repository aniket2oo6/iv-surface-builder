import yfinance as yf
import pandas as pd
from datetime import datetime

def get_option_chain(ticker_symbol, option_type = "call", max_expires = 8):
    ticker = yf.Ticker(ticker_symbol)
    spot = ticker.history(period = "1d")['Close'].iloc[-1]
    expiries = ticker.options[:max_expires]

    today = datetime.today()
    rows = []

    for expire in expiries:
        date = datetime.strptime(expire, "%Y-%m-%d")
        delta = date - today
        T = delta.days / 365

        if T <= 0:
            continue

        chain = ticker.option_chain(expire)

        if option_type == 'call':
            options_df = chain.calls
        else:
            options_df = chain.puts

        for index, row in options_df.iterrows():
            strike = row['strike']
            bid = row['bid']
            ask = row['ask']

            if bid <= 0 or ask <= 0:
                continue

            open_interest = row['openInterest']
            if open_interest < 10:
                continue

            moneyness = abs(strike - spot) / spot
            if moneyness > 0.30:
                continue

            market_price = (bid + ask) / 2
            rows.append({
                'strike': strike,
                'expiry': expire,
                'T': T,
                'market_price': market_price,
                'spot': spot,
                'option_type': option_type
            })

    result = pd.DataFrame(rows)
    return result

