import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="LBG Pricing", layout="wide")

st.title("🎯 LBG Pricing Calculator - Advanced")
st.markdown("---")

# ==================== DATA ====================
BASE_COSTS = {
    "UK": 44200,
    "India": 10400,
    "Philippines": 9650,
    "South Africa": 15600
}

COMPLEXITY = {
    "Low": 1.0,
    "Medium": 1.15,
    "High": 1.35,
    "Very High": 1.60
}

MARGINS = {
    "Account Servicing": 0.25,
    "Fraud Response": 0.30,
    "Compliance Support": 0.28,
    "Data Analytics": 0.35
}

DELIVERY_MODELS = {
    "EB (Existing Business)": 0.95,
    "NB_WAH (Work At Home)": 0.85,
    "NB_WAO (Work At Office)": 1.0
}

CHANNELS = {
    "Voice": 1.2,
    "Email": 0.9,
    "Chat": 1.0,
    "Blended": 1.05
}

ATTRITION_RATES = {
    "Low (5%)": 0.05,
    "Medium (10%)": 0.10,
    "High (15%)": 0.15,
    "Very High (20%)": 0.20
}

# ==================== SIDEBAR ====================
st.sidebar.header("📊 Deal Parameters")

# Basic parameters
geography = st.sidebar.selectbox("Geography", list(BASE_COSTS.keys()))
fte = st.sidebar.slider("Number of FTEs", 10, 500, 50)
complexity = st.sidebar.selectbox("Complexity Level", list(COMPLEXITY.keys()))
capability = st.sidebar.selectbox("Capability", list(MARGINS.keys()))
years = st.sidebar.slider("Contract Years", 1, 5, 3)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Advanced Options")

# TIER 1: Delivery Model
delivery_model = st.sidebar.selectbox("Delivery Model", list(DELIVERY_MODELS.keys()))

# TIER 1: Discount/Markup
discount_markup = st.sidebar.slider("Discount/Markup (%)", -50, 50, 0, step=5)

# TIER 2: Channel Mix
channel = st.sidebar.selectbox("Primary Channel", list(CHANNELS.keys()))

# TIER 2: Ramp-Up Curve
st.sidebar.subheader("Ramp-Up Schedule")
ramp_month1 = st.sidebar.slider("Month 1-3 Utilization (%)", 25, 100, 50, step=5)
ramp_month4 = st.sidebar.slider("Month 4-6 Utilization (%)", 50, 100, 75, step=5)
ramp_month7 = st.sidebar.slider("Month 7+ Utilization (%)", 75, 100, 100, step=5)

# TIER 2: Attrition Rate
attrition = st.sidebar.selectbox("Annual Attrition Rate", list(ATTRITION_RATES.keys()))

st.sidebar.markdown("---")

# ==================== CALCULATIONS ====================

# Calculate base annual cost
base_annual_cost = BASE_COSTS[geography] * fte * COMPLEXITY[complexity] * DELIVERY_MODELS[delivery_model] * CHANNELS[channel]

# Apply discount/markup
discount_factor = 1 + (discount_markup / 100)
annual_cost_adjusted = base_annual_cost * discount_factor

# Calculate with attrition (replacement cost)
attrition_rate = ATTRITION_RATES[attrition]
additional_attrit
