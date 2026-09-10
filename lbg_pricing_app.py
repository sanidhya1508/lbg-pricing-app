import streamlit as st
import pandas as pd

st.set_page_config(page_title="LBG Pricing", layout="wide")

st.title("🎯 LBG Pricing Calculator")
st.markdown("---")

# Base costs by geography
BASE_COSTS = {
    "UK": 44200,
    "India": 10400,
    "Philippines": 9650,
    "South Africa": 15600
}

# Complexity multipliers
COMPLEXITY = {
    "Low": 1.0,
    "Medium": 1.15,
    "High": 1.35,
    "Very High": 1.60
}

# Margin targets by capability
MARGINS = {
    "Account Servicing": 0.25,
    "Fraud Response": 0.30,
    "Compliance Support": 0.28,
    "Data Analytics": 0.35
}

# Sidebar inputs
st.sidebar.header("📊 Deal Parameters")
geography = st.sidebar.selectbox("Geography", list(BASE_COSTS.keys()))
fte = st.sidebar.slider("Number of FTEs", 10, 500, 50)
complexity = st.sidebar.selectbox("Complexity Level", list(COMPLEXITY.keys()))
capability = st.sidebar.selectbox("Capability", list(MARGINS.keys()))
years = st.sidebar.slider("Contract Years", 1, 5, 3)

# Calculations
annual_cost = BASE_COSTS[geography] * fte * COMPLEXITY[complexity]
margin_target = MARGINS[capability]
acv = annual_cost / (1 - margin_target)
tcv = acv * years
margin_dollars = acv - annual_cost
margin_pct = (margin_dollars / acv) * 100

# Display metrics
st.subheader("💰 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("ACV", f"${acv:,.0f}")
with col2:
    st.metric("TCV", f"${tcv:,.0f}")
with col3:
    st.metric("Margin $", f"${margin_dollars:,.0f}")
with col4:
    st.metric("Margin %", f"{margin_pct:.1f}%")

# Summary table
st.subheader("📋 Deal Summary")
summary_data = {
    "Metric": ["Annual Cost", "ACV", "TCV", "Margin Target", "Actual Margin %"],
    "Value": [f"${annual_cost:,.0f}", f"${acv:,.0f}", f"${tcv:,.0f}", f"{margin_target*100:.0f}%", f"{margin_pct:.1f}%"]
}
st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

# Multi-year projection
st.subheader("📈 Multi-Year Projection")
projection_rows = []
for year in range(1, years + 1):
    year_acv = acv * (1.03 ** (year - 1))
    year_cost = annual_cost * (1.03 ** (year - 1))
    year_margin = year_acv - year_cost
    projection_rows.append({
        "Year": year,
        "Revenue": f"${year_acv:,.0f}",
        "Cost": f"${year_cost:,.0f}",
        "Margin": f"${year_margin:,.0f}"
    })

st.dataframe(pd.DataFrame(projection_rows), use_container_width=True)

# Footer
st.markdown("---")
st.success("✅ LBG Pricing Calculator Ready!")
st.caption("💡 Adjust parameters in the sidebar to see real-time pricing updates")
