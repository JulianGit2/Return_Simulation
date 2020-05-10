# Return Simulation

import pandas as pd
import random as rd
import numpy as np
import matplotlib.pyplot as plt

# Parameters
taxRate = 0.27          # Tax Rate
taxThreshold = 801      # Threshold for taxation
years = 40              # Number of years for investing
investment = 10000      # Initial investment
rate = 12 * 450         # Yearly investment
simulations = 10000
finalReturns = []
finalReturns2 = []

# Imports Data with Date, Returns and Inflation Columns
data = pd.read_excel(r"D:\PyCharm\Return_Simulation\Data.xlsx")

# Extract Inflation rates
inflation = pd.DataFrame(data, columns=["Inflation"]) + 1

# Extract returns
returns = pd.DataFrame(data, columns=["S&P_500"])

# Calculates final return
def Calc_Return(years, investment, rate):

    taxlcf = 0          # Tax Loss carried forward

    for period in range(years):
        perReturn = rd.choice(returns["S&P_500"])
        perInflation = rd.choice(inflation["Inflation"])

        # Tax calculation
        perReturn = perReturn * investment

        if perReturn < 0:
            taxlcf = taxlcf + abs(perReturn * taxRate)
        elif perReturn > taxThreshold:

            # Pre Tax Return above tax Threshold
            excessReturn = perReturn - taxThreshold

            if taxlcf > excessReturn * taxRate:
                taxlcf = taxlcf - excessReturn * taxRate
            elif taxlcf <= excessReturn * taxRate:
                excessReturn = excessReturn * (1-taxRate) + taxlcf
                taxlcf = 0

            # After tax Return
            perReturn = excessReturn + taxThreshold

        # Notional after taxes and inflation at the end of the period
        investment = (investment + perReturn + rate) / perInflation

    return(investment)

# Summary Statistics
def Summary_Statistics(finalReturns, name):
    total_investment = investment + years * rate
    finalReturns = np.round(finalReturns, 0)
    quint_low = np.quantile(finalReturns, 0.05)
    quint_high = np.quantile(finalReturns, 0.95)
    quint_med = np.median(finalReturns)
    quint_mean = np.mean(finalReturns)

    print("Data Set: " + name)
    print("Total Investment: " + str(total_investment))
    print("Lowest 5%: " + str(np.round((quint_low), 0)))
    print("Median: " + str(np.round(quint_med)))
    print("Mean: " + str(np.round(quint_mean)))
    print("Highest 5%: " + str(np.round(quint_high, 0)))

# Monte Carlo
for simulation in range(simulations):
    finalReturns.append(Calc_Return(years, investment, rate))

# Alternative tax Rate
taxRate = 0.5

for simulation in range(simulations):
    finalReturns2.append(Calc_Return(years, investment, rate))

Summary_Statistics(finalReturns, "Low Taxation:")
Summary_Statistics(finalReturns2, "High Taxation:")

# Plot histogram
bins = np.linspace(0, 5000000, 200)
plt.hist(finalReturns, bins, alpha=0.5, label="Low Taxation")
plt.hist(finalReturns2, bins, alpha=0.5, label="High Taxation")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.xticks(np.arange(0, 5000000, step=200000))
plt.legend(loc='upper right')
plt.show()
