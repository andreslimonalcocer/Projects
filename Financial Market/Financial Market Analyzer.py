import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override() 
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define the Borwnian-Movement method.

def brownianMovement(data, intervals, iterations):
    for i in assets:
        df = data[i].to_frame()
        log_returns = np.log(1 + df.pct_change())
        u = log_returns.mean() # Calculate the log returns mean.
        var = log_returns.var() # Calculate the log returns variance.
        drift = u - (0.5 * var) # Calculate the drift of the movement.
        stdev = log_returns.std() # Calculate the log returns standard deviation. 
        daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(intervals, iterations)))
        S0 = df.iloc[-1] # Assign the first value using the last price available.
        price_list = np.zeros_like(daily_returns) # Creates a zero-matrix of the daily_returns dimension.
        price_list[0] = S0 # Assign the first value of the matriz to S0.
        for t in range(1, intervals):
            price_list[t] = price_list[t-1] * daily_returns[t]
        plt.figure(figsize = (10, 6))
        plt.title("Brownian Movement Method "+ i)
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.plot(price_list);
    return plt.show()

# Define the Euler-Discretization method.

def eulerDiscretization(data, T, iterations):
    for i in assets:
        df = data[i].to_frame()
        log_returns = np.log(1 + df.pct_change())
        r = 0.025 # Risk free.
        intervals = T * 252
        stdev = log_returns.std() * 252 ** 0.5
        delta_t = T / intervals
        Z = np.random.standard_normal((intervals + 1, iterations))
        S = np.zeros_like(Z)
        S0 = df.iloc[-1]
        S[0] = S0
        for t in range(1, intervals + 1):
            S[t] = S[t-1] * np.exp((r - 0.5 * stdev.values ** 2) * delta_t + stdev.values * delta_t ** 0.5 * Z[t])
        fig = plt.figure(figsize = (10, 6))
        plt.title("Euler Discretization Method " + i)
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.plot(S);
    return plt.show()

# Input the time values and the number of assets to analyze.
start_date = input("Select the beginning period (YYYY-MM-DD): ")
end_date = input("Select the ending period (YYYY-MM-DD): ")
n = int(input("Type the number of assets you want to analyze: "))
counter = 0
assets = []
while counter < n:
    ticker = input("Type the ticker of the asset: ")
    assets.append(ticker)
    counter += 1

# Download data from Yahoo Finance.
data = pd.DataFrame()
for s in assets:
    temp_data = pdr.get_data_yahoo(s, start=start_date, end=end_date)
    temp_data = temp_data.rename(columns={'Adj Close': s})
    data = pd.concat([data, temp_data[s]], axis=1)

# Graphs the assets prices normalize to 100.
(data / data.iloc[0] * 100).plot(figsize=(10, 5))
    
# Calculate de log returns.
log_returns = np.log(data / data.shift(1))

# Randomly generates different portfolios with different weights.
num_portfolios = int(input("How many random portfolios do you wish to generate? "))
all_weights = np.zeros((num_portfolios, len(data.columns))) # Create a zero matrix to store the weights of all the portfolios.
ret_arr = np.zeros(num_portfolios) # Creates an empty array to store the log returns of the each portfolio.
vol_arr = np.zeros(num_portfolios) # Creates an empty array to store the volatilities of the each portfolio.
sharpe_arr = np.zeros(num_portfolios) # Creates an empty array to store the Sharpe ratio of each portfolio.
for i in range(num_portfolios):
    weights = np.array(np.random.random(len(data.columns)))
    weights = weights / np.sum(weights)
    all_weights[i,:] = weights
    ret_arr[i] = np.sum((log_returns.mean() * weights) * 252)
    vol_arr[i] = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 252, weights)))
    sharpe_arr[i] = ret_arr[i] / vol_arr[i]

# Find the optimal portfolio using the Sharpe ratio.
max_sharpe = sharpe_arr.argmax()
best_weights = all_weights[max_sharpe,:]
best_ret = ret_arr[max_sharpe]
best_vol = vol_arr[max_sharpe]

# Stores the optimal portfolio in a DataFrame.
optimal_portfolio = pd.DataFrame({
    'Ticker': data.columns,
    'Weight': best_weights
})
optimal_portfolio = optimal_portfolio.set_index('Ticker')
optimal_portfolio['Weight'] = optimal_portfolio['Weight'].map('{:.2%}'.format)
optimal_portfolio['Weight'] = optimal_portfolio['Weight'].astype(str)
print('Optimal Portfolio:')
print(optimal_portfolio)

# Graph the results.
fig, ax = plt.subplots(figsize=(12,4))
mappable = ax.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='plasma', alpha=0.8)
ax.scatter(best_vol, best_ret, c='red', s=100, marker='*', label='Optimal')
ax.set_title('Markowitz Portfolio')
ax.set_xlabel('Expected Volatility')
ax.set_ylabel('Expected Return')
ax.legend()
plt.colorbar(mappable, ax=ax)
plt.show()

# Simulation section.
simulatation = input("Do you wish to make a Monte Carlo simulation to predict future prices? Type 'yes' or 'no': ")
if simulatation == 'yes':
    simulation_iter = int(input("Select the numer of iterations: "))
    simulation_bool = True
    while simulation_bool:
        simulation_method = input("Select the method, 'brownian-movement' or 'euler-discretization': ")
        if simulation_method == 'brownian-movement':
            simulation_time = int(input("Select the number of days you want to predict: "))
            brownianMovement(data, simulation_time, simulation_iter)
            simulation_bool = False
        elif simulation_method == 'euler-discretization':
            simulation_period = int(input("Select the number of years you want to predict: "))
            eulerDiscretization(data, simulation_period, simulation_iter)
            simulation_bool = False
        else:
            print("Unrecognized method, please select a valid method.")