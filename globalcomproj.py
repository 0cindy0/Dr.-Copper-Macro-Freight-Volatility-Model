import pandas as pd

# Load the commodity dataset
df_commodities = pd.read_csv("/Users/cindy/Downloads/Global_Commodity_Prices_2000_2026.csv")

# Keep only rows where the commodity column is exactly 'Copper'
df_copper = df_commodities[df_commodities['Commodity'] == 'Copper'].copy()

# Convert the date column to standard datetime format
df_copper['Date'] = pd.to_datetime(df_copper['Date'])

# Sort from oldest to newest
df_copper = df_copper.sort_values('Date')

# Load the logistics dataset
df_logistics = pd.read_csv("/Users/cindy/Downloads/global_supply_chain_risk_2026.csv")

# Convert logistics date column to standard datetime format
df_logistics['Date'] = pd.to_datetime(df_logistics['Date'])

# Sort from oldest to newest
df_logistics = df_logistics.sort_values('Date')

# Merge datasets on the Date column
df_master = pd.merge(df_copper, df_logistics, on='Date', how='inner')

import numpy as np
import statsmodels.api as sm

# 1. Calculate daily log returns based on the closing price
# Note: Check if your commodity dataset uses 'Close' or another name for the price column
df_master['Copper_Return'] = np.log(df_master['Close'] / df_master['Close'].shift(1))

# 2. Choose your primary logistics metric 
# Note: Replace 'Delay_Days' with the exact column name from your supply chain dataset (e.g., 'Risk_Score' or 'Transit_Time')
df_master['Logistics_Metric'] = df_master['Disruption_Occurred'] 

# 3. Drop rows with missing values created by the shift calculation
df_master = df_master.dropna(subset=['Copper_Return', 'Logistics_Metric'])

# 4. Calculate cross-correlation up to a 30-day window
ccf_values = sm.tsa.stattools.ccf(df_master['Logistics_Metric'], df_master['Copper_Return'], adjusted=False)[:30]

# Find the specific lag day with the highest absolute correlation strength
best_lag = np.argmax(np.abs(ccf_values))
print(f"Logistics disruptions impact Copper prices with a calculated lag of: {best_lag} days")

# ==========================================
# PHASE 4: RISK & VOLATILITY MODELING (GARCH)
# ==========================================
from arch import arch_model

# 1. Force the lag to 7 days if your CCF calculated 0, otherwise use the best_lag
simulation_lag = best_lag if best_lag > 0 else 7

# Shift the logistics metric forward to align today's risk with future prices
df_master['Lagged_Disruption'] = df_master['Logistics_Metric'].shift(simulation_lag)
df_master = df_master.dropna(subset=['Lagged_Disruption'])

# 2. Scale returns up by 100 to help the GARCH model converge mathematically
df_master['Scaled_Return'] = df_master['Copper_Return'] * 100

# 3. Fit a GARCH(1,1) model with your supply chain disruptions as an external factor
am = arch_model(df_master['Scaled_Return'], x=df_master['Lagged_Disruption'], vol='Garch', p=1, q=1)
res = am.fit(update_freq=0)

# 4. Extract the conditional volatility (the statistical risk)
df_master['Estimated_Volatility'] = res.conditional_volatility / 100

# ==========================================
# PHASE 5: VALUE-AT-RISK (VaR) CALCULATION
# ==========================================
# Simulate a corporate portfolio holding $5,000,000 worth of copper inventory
portfolio_value = 5000000
confidence_level = 1.645 # This represents 95% confidence using a standard normal distribution

# Calculate the dollar-denominated maximum risk for each day
df_master['VaR_Dollars'] = portfolio_value * confidence_level * df_master['Estimated_Volatility']

# Print the final baseline metrics for your project summary
mean_risk = df_master['VaR_Dollars'].mean()
max_risk = df_master['VaR_Dollars'].max()

print("\n--- Corporate Risk Summary ---")
print(f"Average daily capital at risk: ${mean_risk:,.2f}")
print(f"Peak capital at risk during supply chain crisis: ${max_risk:,.2f}")