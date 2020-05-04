# Return Simulation

import pandas as pd
import random as rd
import numpy as np

tax_rate = 0.25
years = 30
investment = 1000
rate = 450
simulations = 500
final_returns = []

# Imports the Data with Date, Returns and Inflation
data = pd.read_excel(r"D:\PyCharm\Return_Simulation\Data.xlsx")

# Extract Inflation rates
inflation = pd.DataFrame(data, columns=["Inflation"]) + 1

# Calculates net returns (after tax returns)
returns = pd.DataFrame(data, columns=["S&P_500"]) * (1 - tax_rate)

# Calculates net returns after inflation
returns["S&P_500"] = returns["S&P_500"] / inflation["Inflation"]

# Calculates final return
def calc_return(years, investment, rate):

    for period in range(years):
        per_return = (1 + rd.choice(returns["S&P_500"]))
        investment = investment * per_return + rate

    return(investment)

# Monte Carlo
for simulation in range(simulations):
    final_returns.append(calc_return(years, investment, rate))

final_returns = np.round(final_returns, 1)
print(final_returns)

