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
additional_attrition_cost = annual_cost_adjusted * attrition_rate
annual_cost_with_attrition = annual_cost_adjusted + additional_attrition_cost

# Revenue calculation
margin_target = MARGINS[capability]
acv = annual_cost_with_attrition / (1 - margin_target)
tcv = acv * years
margin_dollars = acv - annual_cost_with_attrition
margin_pct = (margin_dollars / acv) * 100

# Cost breakdown (TIER 1)
salary_pct = 0.65
overhead_pct = 0.25
training_pct = 0.10

salary_cost = annual_cost_adjusted * salary_pct
overhead_cost = annual_cost_adjusted * overhead_pct
training_cost = annual_cost_adjusted * training_pct

# Cost per FTE (Performance metric)
cost_per_fte = annual_cost_with_attrition / fte
revenue_per_fte = acv / fte
margin_per_fte = margin_dollars / fte

# ==================== MAIN DISPLAY ====================

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

st.markdown("---")

# TIER 1: Cost Breakdown
st.subheader("📊 Cost Breakdown (TIER 1)")
col1, col2 = st.columns(2)

with col1:
    breakdown_data = {
        "Component": ["Salary", "Overhead", "Training"],
        "Amount": [f"${salary_cost:,.0f}", f"${overhead_cost:,.0f}", f"${training_cost:,.0f}"],
        "% of Total": [f"{salary_pct*100:.0f}%", f"{overhead_pct*100:.0f}%", f"{training_pct*100:.0f}%"]
    }
    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)

with col2:
    st.metric("Base Annual Cost", f"${base_annual_cost:,.0f}", delta=f"{discount_markup:+.0f}% applied")
    st.metric("Attrition Cost", f"${additional_attrition_cost:,.0f}", delta=f"{attrition}")
    st.metric("Final Annual Cost", f"${annual_cost_with_attrition:,.0f}")

st.markdown("---")

# Performance Metrics
st.subheader("📈 Performance Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cost per FTE", f"${cost_per_fte:,.0f}")
with col2:
    st.metric("Revenue per FTE", f"${revenue_per_fte:,.0f}")
with col3:
    st.metric("Margin per FTE", f"${margin_per_fte:,.0f}")

st.markdown("---")

# Deal Summary
st.subheader("📋 Deal Summary")
summary_data = {
    "Metric": [
        "Geography",
        "Delivery Model",
        "Channel",
        "FTEs",
        "Complexity",
        "Capability",
        "Annual Cost (Base)",
        "Discount/Markup",
        "Attrition Rate",
        "Annual Cost (Final)",
        "ACV",
        "TCV",
        "Margin Target",
        "Actual Margin %"
    ],
    "Value": [
        geography,
        delivery_model,
        channel,
        str(fte),
        complexity,
        capability,
        f"${base_annual_cost:,.0f}",
        f"{discount_markup:+.0f}%",
        attrition,
        f"${annual_cost_with_attrition:,.0f}",
        f"${acv:,.0f}",
        f"${tcv:,.0f}",
        f"{margin_target*100:.0f}%",
        f"{margin_pct:.1f}%"
    ]
}
st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

st.markdown("---")

# TIER 2: Ramp-Up Curve
st.subheader("📅 Ramp-Up Schedule (TIER 2)")
ramp_data = {
    "Period": ["Month 1-3", "Month 4-6", "Month 7+"],
    "Utilization": [f"{ramp_month1}%", f"{ramp_month4}%", f"{ramp_month7}%"],
    "Adjusted FTE": [
        f"{fte * ramp_month1 / 100:.1f}",
        f"{fte * ramp_month4 / 100:.1f}",
        f"{fte * ramp_month7 / 100:.1f}"
    ]
}
st.dataframe(pd.DataFrame(ramp_data), use_container_width=True)

st.markdown("---")

# TIER 2: Sensitivity Analysis
st.subheader("🎯 Sensitivity Analysis (TIER 2)")
st.write("Impact on ACV if key factors change:")

col1, col2 = st.columns(2)

with col1:
    # FTE sensitivity
    fte_scenarios = [fte * 0.8, fte, fte * 1.2]
    fte_acv = []
    for scenario_fte in fte_scenarios:
        scenario_cost = BASE_COSTS[geography] * scenario_fte * COMPLEXITY[complexity] * DELIVERY_MODELS[delivery_model]
        scenario_acv = scenario_cost / (1 - margin_target)
        fte_acv.append(scenario_acv)
    
    sensitivity_fte = {
        "FTE Scenario": [f"{int(fte * 0.8)}", f"{int(fte)}", f"{int(fte * 1.2)}"],
        "ACV": [f"${x:,.0f}" for x in fte_acv],
        "Change": [f"{((fte_acv[i] / acv) - 1) * 100:+.1f}%" for i in range(3)]
    }
    st.write("**FTE Impact:**")
    st.dataframe(pd.DataFrame(sensitivity_fte), use_container_width=True)

with col2:
    # Complexity sensitivity
    complexity_scenarios = ["Low", "Medium", "High", "Very High"]
    complexity_acv = []
    for comp_scenario in complexity_scenarios:
        scenario_cost = BASE_COSTS[geography] * fte * COMPLEXITY[comp_scenario] * DELIVERY_MODELS[delivery_model]
        scenario_acv = scenario_cost / (1 - margin_target)
        complexity_acv.append(scenario_acv)
    
    sensitivity_complexity = {
        "Complexity": complexity_scenarios,
        "ACV": [f"${x:,.0f}" for x in complexity_acv],
        "Change": [f"{((complexity_acv[i] / acv) - 1) * 100:+.1f}%" for i in range(4)]
    }
    st.write("**Complexity Impact:**")
    st.dataframe(pd.DataFrame(sensitivity_complexity), use_container_width=True)

st.markdown("---")

# Multi-Year Projection
st.subheader("📈 Multi-Year Projection")
projection_rows = []
cumulative_cost = 0
cumulative_revenue = 0

for year in range(1, years + 1):
    year_acv = acv * (1.03 ** (year - 1))
    year_cost = annual_cost_with_attrition * (1.03 ** (year - 1))
    year_margin = year_acv - year_cost
    
    cumulative_cost += year_cost
    cumulative_revenue += year_acv
    
    projection_rows.append({
        "Year": year,
        "Revenue": f"${year_acv:,.0f}",
        "Cost": f"${year_cost:,.0f}",
        "Margin": f"${year_margin:,.0f}",
        "Cumulative Revenue": f"${cumulative_revenue:,.0f}",
        "Cumulative Margin": f"${cumulative_revenue - cumulative_cost:,.0f}"
    })

st.dataframe(pd.DataFrame(projection_rows), use_container_width=True)

st.markdown("---")

# TIER 1: Export Options
st.subheader("💾 Export & Share (TIER 1)")

col1, col2, col3 = st.columns(3)

with col1:
    # CSV Export
    export_data = {
        "Parameter": [
            "Geography", "Delivery Model", "Channel", "FTEs", "Complexity", "Capability",
            "Base Annual Cost", "Discount/Markup", "Attrition Rate", "Final Annual Cost",
            "ACV", "TCV", "Margin %", "Cost per FTE", "Revenue per FTE"
        ],
        "Value": [
            geography, delivery_model, channel, fte, complexity, capability,
            f"{base_annual_cost:.2f}", f"{discount_markup}%", attrition, f"{annual_cost_with_attrition:.2f}",
            f"{acv:.2f}", f"{tcv:.2f}", f"{margin_pct:.2f}", f"{cost_per_fte:.2f}", f"{revenue_per_fte:.2f}"
        ]
    }
    
    csv_data = pd.DataFrame(export_data).to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"lbg_pricing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # JSON Export
    json_data = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "geography": geography,
            "delivery_model": delivery_model,
            "channel": channel
        },
        "inputs": {
            "fte": fte,
            "complexity": complexity,
            "capability": capability,
            "years": years,
            "discount_markup": discount_markup,
            "attrition": attrition
        },
        "outputs": {
            "base_annual_cost": float(base_annual_cost),
            "annual_cost": float(annual_cost_with_attrition),
            "acv": float(acv),
            "tcv": float(tcv),
            "margin_dollars": float(margin_dollars),
            "margin_pct": float(margin_pct)
        }
    }
    
    json_export = json.dumps(json_data, indent=2)
    st.download_button(
        label="📥 Download JSON",
        data=json_export,
        file_name=f"lbg_pricing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

with col3:
    st.info("✅ **Data Ready to Export**\n\nDownload and share pricing scenarios with stakeholders")

st.markdown("---")

st.success("✅ LBG Pricing Calculator - Advanced Ready!")
st.caption("🚀 All TIER 1 & TIER 2 features enabled | Real-time calculations | Export ready")
