import numpy as np
from scipy.stats import norm

def bs_call_price(spot, strike, T, r, sigma):
    d1 = (np.log(spot / strike) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = spot * norm.cdf(d1) - strike * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def bs_vega(spot, strike, T, r, sigma):
    d1 = (np.log(spot / strike) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = spot * norm.pdf(d1) * np.sqrt(T)
    return vega

def implied_vol(market_price, spot, strike, T, r, max_iterations = 100, tolerance = 1e-6):
    sigma = 0.2

    for i in range(max_iterations):
        price = bs_call_price(spot, strike, T, r, sigma)
        error = price - market_price
        if abs(error) < tolerance:
            return sigma
        vega = bs_vega(spot, strike, T, r, sigma)
        sigma = sigma - (error / vega)

    return sigma

def add_iv_column(df, r = 0.05):
    ivs = []

    for index, row in df.iterrows():
        market_price = row['market_price']
        spot = row['spot']
        strike = row['strike']
        T = row['T']
        result = implied_vol(market_price, spot, strike, T, r)
        ivs.append(result)

    df['iv'] = ivs
    return df

