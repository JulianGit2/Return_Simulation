# Return Simulation

import pandas as pd
import random as rd
import numpy as np
import matplotlib.pyplot as plt

# Parameters
tax_rate = 0.27          # Tax Rate
tax_threshold = 801      # Threshold for taxation
years = 40              # Number of years for investing
investment = 10000      # Initial investment
rate = 12 * 450         # Yearly investment
simulations = 10000
final_returns = []
final_returns2 = []

# Imports Data with Date, Returns and Inflation Columns
data = pd.read_excel(r"D:\PyCharm\Return_Simulation\Data.xlsx")

# Extract Inflation rates
inflation = pd.DataFrame(data, columns=["Inflation"]) + 1

# Extract returns
returns = pd.DataFrame(data, columns=["S&P_500"])

# Calculates final return
def calc_return(years, investment, rate):

    taxlcf = 0          # Tax Loss carried forward

    for period in range(years):
        perReturn = rd.choice(returns["S&P_500"])
        perInflation = rd.choice(inflation["Inflation"])

        # Tax calculation
        perReturn = perReturn * investment

        if perReturn < 0:
            taxlcf = taxlcf + abs(perReturn * tax_rate)
        elif perReturn > tax_threshold:

            # Pre Tax Return above tax Threshold
            excessReturn = perReturn - tax_threshold

            if taxlcf > excessReturn * tax_rate:
                taxlcf = taxlcf - excessReturn * tax_rate
            elif taxlcf <= excessReturn * tax_rate:
                excessReturn = excessReturn * (1-tax_rate) + taxlcf
                taxlcf = 0

            # After tax Return
            perReturn = excessReturn + tax_threshold

        # Notional after taxes and inflation at the end of the period
        investment = (investment + perReturn + rate) / perInflation

    return(investment)

# Summary Statistics
def summary_statistics(final_returns, name):
    total_investment = investment + years * rate
    final_returns = np.round(final_returns, 0)
    quint_low = np.quantile(final_returns, 0.05)
    quint_high = np.quantile(final_returns, 0.95)
    quint_med = np.median(final_returns)
    quint_mean = np.mean(final_returns)

    print("Data Set: " + name)
    print("Total Investment: " + str(total_investment))
    print("Lowest 5%: " + str(np.round((quint_low), 0)))
    print("Median: " + str(np.round(quint_med)))
    print("Mean: " + str(np.round(quint_mean)))
    print("Highest 5%: " + str(np.round(quint_high, 0)))

# Monte Carlo
for simulation in range(simulations):
    final_returns.append(calc_return(years, investment, rate))

# Alternative tax Rate
tax_rate = 0.5

for simulation in range(simulations):
    final_returns2.append(calc_return(years, investment, rate))

summary_statistics(final_returns, "Low Taxation:")
summary_statistics(final_returns2, "High Taxation:")

# Plot histogram
bins = np.linspace(0, 5000000, 200)
plt.hist(final_returns, bins, alpha=0.5, label="Low Taxation")
plt.hist(final_returns2, bins, alpha=0.5, label="High Taxation")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.xticks(np.arange(0, 5000000, step=200000))
plt.legend(loc='upper right')
plt.show()
