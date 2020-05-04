# Return Simulation

import pandas as pd
import random as rd
import numpy as np

tax_rate = 0.27
years = 40
investment = 10000
rate = 12 * 450
simulations = 10000
final_returns = []

# Imports the Data with Date, Returns and Inflation
data = pd.read_excel(r"D:\PyCharm\Return_Simulation\Data.xlsx")

# Extract Inflation rates
inflation = pd.DataFrame(data, columns=["Inflation"]) + 1

# Calculates net returns (after tax returns)
returns = (pd.DataFrame(data, columns=["S&P_500"]) * (1 - tax_rate)) + 1

# Calculates net returns after inflation
returns["S&P_500"] = returns["S&P_500"] / inflation["Inflation"]

# Calculates final return
def calc_return(years, investment, rate):

    for period in range(years):
        per_return = (rd.choice(returns["S&P_500"]))
        investment = investment * per_return + rate

    return(investment)

# Monte Carlo
for simulation in range(simulations):
    final_returns.append(calc_return(years, investment, rate))

total_investment = investment + years * rate
final_returns = np.round(final_returns, 0)
quint_low = np.quantile(final_returns, 0.05)
quint_high = np.quantile(final_returns, 0.95)
quint_med = np.median(final_returns)
quint_mean = np.mean(final_returns)

print("Total Investment: " + str(total_investment))
print("Lowest 5%: " + str(np.round((quint_low), 0)))
print("Median: " + str(np.round(quint_med)))
print("Mean: " + str(np.round(quint_mean)))
print("Highest 5%: " + str(np.round((quint_high), 0)))


