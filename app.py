import streamlit as st
import pandas as pd
import numpy as np

# Set up the dashboard page
st.set_page_config(page_title="Supply Chain Risk Control Room", layout="wide")
st.title("🚢 Dr. Copper: Global Supply Chain Risk Control Room")
st.markdown("This dashboard quantifies corporate financial risk exposure based on dynamic maritime shipping disruptions.")

# Sidebar Controls for the Recruiter
st.sidebar.header("Interactive Scenario Simulation")
portfolio = st.sidebar.slider("Total Copper Inventory Value ($)", 1000000, 10000000, 5000000, step=500000)
disruption_status = st.sidebar.radio("Current Port/Logistics Status", ["Normal Operations", "Active Supply Chain Disruption"])

# Statistical backend replication based on your GARCH outputs
baseline_vol = 0.0078  # Maps to your ~$64k average risk
peak_vol = 0.0375     # Maps to your ~$309k peak risk
confidence_level = 1.645 # 95% Confidence threshold

# Calculate dynamic risk based on recruiter inputs
current_vol = peak_vol if disruption_status == "Active Supply Chain Disruption" else baseline_vol
calculated_var = portfolio * confidence_level * current_vol

# KPIs
st.subheader("Real-Time Capital Exposure Matrix")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Current Value-at-Risk (1-Day VaR)", value=f"${calculated_var:,.2f}")
with col2:
    status_color = "🔴 HIGH RISK WINDOW" if disruption_status == "Active Supply Chain Disruption" else "🟢 STABLE"
    st.metric(label="System Risk Status (11-Day Predicted Lag)", value=status_color)

# Add context for the user
st.info(f"**Statistical Insight:** Your analysis mathematically isolated an 11-day transmission lag between maritime logistics shocks and copper return volatility. Adjusting the parameters above simulates how capital exposure responds across this baseline framework.")