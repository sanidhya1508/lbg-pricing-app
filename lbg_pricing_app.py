import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="LBG Pricing", layout="wide")

st.title("🎯 LBG Pricing Calculator - Enterprise Edition")
st.markdown("**TIER 1 + TIER 2 + TIER 3 Features Enabled**")
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

# TIER 3: Pricing Tiers
PRICING_TIERS = {
    "Bronze": {"margin": 0.20, "sla": "Standard", "support": "Business hours"},
    "Silver": {"margin": 0.28, "sla": "Enhanced", "support": "24/5"},
    "Gold": {"margin": 0.35, "sla": "Premium", "support": "24/7"}
}

# TIER 3: Currency Conversion
CURRENCIES = {
    "USD": 1.0,
    "GBP": 1.0,
    "INR": 82.5,
    "PHP": 55.0
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "GBP": "£",
    "INR": "₹",
    "PHP": "₱"
}

# ==================== SESSION STATE (TIER 3: Comparison) ====================
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Calculator", "🔄 Comparison (TIER 3)", "💎 Pricing Tiers (TIER 3)", "🌍 Multi-Currency (TIER 3)"])

# ==================== TAB 1: MAIN CALCULATOR ====================
with tab1:
    st.header("📊 Main Pricing Calculator")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Deal Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            geography = st.selectbox("Geography", list(BASE_COSTS.keys()), key="calc_geo")
            fte = st.slider("Number of FTEs", 10, 500, 50, key="calc_fte")
            complexity = st.selectbox("Complexity Level", list(COMPLEXITY.keys()), key="calc_comp")
            capability = st.selectbox("Capability", list(MARGINS.keys()), key="calc_cap")
        
        with col2:
            years = st.slider("Contract Years", 1, 5, 3, key="calc_years")
            delivery_model = st.selectbox("Delivery Model", list(DELIVERY_MODELS.keys()), key="calc_deliv")
            discount_markup = st.slider("Discount/Markup (%)", -50, 50, 0, step=5, key="calc_disc")
            channel = st.selectbox("Primary Channel", list(CHANNELS.keys()), key="calc_chan")
        
        st.markdown("---")
        st.subheader("Advanced Options")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ramp-Up Schedule:**")
            ramp_month1 = st.slider("Month 1-3 Utilization (%)", 25, 100, 50, step=5, key="ramp1")
            ramp_month4 = st.slider("Month 4-6 Utilization (%)", 50, 100, 75, step=5, key="ramp2")
            ramp_month7 = st.slider("Month 7+ Utilization (%)", 75, 100, 100, step=5, key="ramp3")
        
        with col2:
            st.write("**Risk Factors:**")
            attrition = st.selectbox("Annual Attrition Rate", list(ATTRITION_RATES.keys()), key="attrition")
            currency = st.selectbox("Currency", list(CURRENCIES.keys()), key="currency")
    
    with col_right:
        st.write("**Scenario Name (for saving):**")
        scenario_name = st.text_input("Give this scenario a name", value="Scenario 1", key="scenario_name")
        if st.button("💾 Save Scenario", key="save_scenario"):
            st.session_state.scenarios[scenario_name] = {
                "geography": geography,
                "fte": fte,
                "complexity": complexity,
                "capability": capability,
                "years": years,
                "delivery_model": delivery_model,
                "discount_markup": discount_markup,
                "channel": channel,
                "ramp_month1": ramp_month1,
                "ramp_month4": ramp_month4,
                "ramp_month7": ramp_month7,
                "attrition": attrition,
                "currency": currency
            }
            st.success(f"✅ Saved: {scenario_name}")
    
    # ==================== CALCULATIONS ====================
    base_annual_cost = BASE_COSTS[geography] * fte * COMPLEXITY[complexity] * DELIVERY_MODELS[delivery_model] * CHANNELS[channel]
    discount_factor = 1 + (discount_markup / 100)
    annual_cost_adjusted = base_annual_cost * discount_factor
    attrition_rate = ATTRITION_RATES[attrition]
    additional_attrition_cost = annual_cost_adjusted * attrition_rate
    annual_cost_with_attrition = annual_cost_adjusted + additional_attrition_cost
    margin_target = MARGINS[capability]
    acv = annual_cost_with_attrition / (1 - margin_target)
    tcv = acv * years
    margin_dollars = acv - annual_cost_with_attrition
    margin_pct = (margin_dollars / acv) * 100
    
    # Cost breakdown
    salary_pct, overhead_pct, training_pct = 0.65, 0.25, 0.10
    salary_cost = annual_cost_adjusted * salary_pct
    overhead_cost = annual_cost_adjusted * overhead_pct
    training_cost = annual_cost_adjusted * training_pct
    
    # Performance metrics
    cost_per_fte = annual_cost_with_attrition / fte
    revenue_per_fte = acv / fte
    margin_per_fte = margin_dollars / fte
    
    # Apply currency conversion
    currency_factor = CURRENCIES[currency]
    acv_converted = acv * currency_factor
    tcv_converted = tcv * currency_factor
    margin_converted = margin_dollars * currency_factor
    
    currency_symbol = CURRENCY_SYMBOLS[currency]
    
    # ==================== DISPLAY METRICS ====================
    st.markdown("---")
    st.subheader("💰 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ACV", f"{currency_symbol}{acv_converted:,.0f}")
    with col2:
        st.metric("TCV", f"{currency_symbol}{tcv_converted:,.0f}")
    with col3:
        st.metric("Margin $", f"{currency_symbol}{margin_converted:,.0f}")
    with col4:
        st.metric("Margin %", f"{margin_pct:.1f}%")
    
    st.markdown("---")
    
    # Cost breakdown
    st.subheader("📊 Cost Breakdown (TIER 1)")
    col1, col2 = st.columns(2)
    
    with col1:
        breakdown_data = {
            "Component": ["Salary", "Overhead", "Training"],
            "Amount": [f"{currency_symbol}{salary_cost*currency_factor:,.0f}", 
                      f"{currency_symbol}{overhead_cost*currency_factor:,.0f}", 
                      f"{currency_symbol}{training_cost*currency_factor:,.0f}"],
            "% of Total": [f"{salary_pct*100:.0f}%", f"{overhead_pct*100:.0f}%", f"{training_pct*100:.0f}%"]
        }
        st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
    
    with col2:
        st.metric("Base Annual Cost", f"{currency_symbol}{base_annual_cost*currency_factor:,.0f}", 
                 delta=f"{discount_markup:+.0f}% applied")
        st.metric("Attrition Cost", f"{currency_symbol}{additional_attrition_cost*currency_factor:,.0f}", 
                 delta=f"{attrition}")
        st.metric("Final Annual Cost", f"{currency_symbol}{annual_cost_with_attrition*currency_factor:,.0f}")
    
    st.markdown("---")
    
    # Performance metrics
    st.subheader("📈 Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cost per FTE", f"{currency_symbol}{cost_per_fte*currency_factor:,.0f}")
    with col2:
        st.metric("Revenue per FTE", f"{currency_symbol}{revenue_per_fte*currency_factor:,.0f}")
    with col3:
        st.metric("Margin per FTE", f"{currency_symbol}{margin_per_fte*currency_factor:,.0f}")
    
    st.markdown("---")
    
    # Deal summary
    st.subheader("📋 Deal Summary")
    summary_data = {
        "Metric": [
            "Geography", "Delivery Model", "Channel", "FTEs", "Complexity", "Capability",
            "Base Annual Cost", "Discount/Markup", "Attrition Rate", "Annual Cost (Final)",
            "ACV", "TCV", "Margin Target", "Actual Margin %", "Currency"
        ],
        "Value": [
            geography, delivery_model, channel, str(fte), complexity, capability,
            f"{currency_symbol}{base_annual_cost*currency_factor:,.0f}",
            f"{discount_markup:+.0f}%",
            attrition,
            f"{currency_symbol}{annual_cost_with_attrition*currency_factor:,.0f}",
            f"{currency_symbol}{acv_converted:,.0f}",
            f"{currency_symbol}{tcv_converted:,.0f}",
            f"{margin_target*100:.0f}%",
            f"{margin_pct:.1f}%",
            currency
        ]
    }
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
    
    st.markdown("---")
    
    # Ramp-up
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
    
    # Sensitivity
    st.subheader("🎯 Sensitivity Analysis (TIER 2)")
    st.write("Impact on ACV if key factors change:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fte_scenarios = [fte * 0.8, fte, fte * 1.2]
        fte_acv = []
        for scenario_fte in fte_scenarios:
            scenario_cost = BASE_COSTS[geography] * scenario_fte * COMPLEXITY[complexity] * DELIVERY_MODELS[delivery_model]
            scenario_acv = scenario_cost / (1 - margin_target)
            fte_acv.append(scenario_acv)
        
        sensitivity_fte = {
            "FTE Scenario": [f"{int(fte * 0.8)}", f"{int(fte)}", f"{int(fte * 1.2)}"],
            "ACV": [f"{currency_symbol}{x*currency_factor:,.0f}" for x in fte_acv],
            "Change": [f"{((fte_acv[i] / acv) - 1) * 100:+.1f}%" for i in range(3)]
        }
        st.write("**FTE Impact:**")
        st.dataframe(pd.DataFrame(sensitivity_fte), use_container_width=True)
    
    with col2:
        complexity_scenarios = ["Low", "Medium", "High", "Very High"]
        complexity_acv = []
        for comp_scenario in complexity_scenarios:
            scenario_cost = BASE_COSTS[geography] * fte * COMPLEXITY[comp_scenario] * DELIVERY_MODELS[delivery_model]
            scenario_acv = scenario_cost / (1 - margin_target)
            complexity_acv.append(scenario_acv)
        
        sensitivity_complexity = {
            "Complexity": complexity_scenarios,
            "ACV": [f"{currency_symbol}{x*currency_factor:,.0f}" for x in complexity_acv],
            "Change": [f"{((complexity_acv[i] / acv) - 1) * 100:+.1f}%" for i in range(4)]
        }
        st.write("**Complexity Impact:**")
        st.dataframe(pd.DataFrame(sensitivity_complexity), use_container_width=True)
    
    st.markdown("---")
    
    # Multi-year projection
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
            "Revenue": f"{currency_symbol}{year_acv*currency_factor:,.0f}",
            "Cost": f"{currency_symbol}{year_cost*currency_factor:,.0f}",
            "Margin": f"{currency_symbol}{year_margin*currency_factor:,.0f}",
            "Cumulative Revenue": f"{currency_symbol}{cumulative_revenue*currency_factor:,.0f}",
            "Cumulative Margin": f"{currency_symbol}{(cumulative_revenue - cumulative_cost)*currency_factor:,.0f}"
        })
    
    st.dataframe(pd.DataFrame(projection_rows), use_container_width=True)
    
    st.markdown("---")
    
    # Export
    st.subheader("💾 Export & Share (TIER 1)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        export_data = {
            "Parameter": [
                "Geography", "Delivery Model", "Channel", "FTEs", "Complexity", "Capability",
                "Base Annual Cost", "Discount/Markup", "Attrition Rate", "Final Annual Cost",
                "ACV", "TCV", "Margin %", "Cost per FTE", "Revenue per FTE", "Currency"
            ],
            "Value": [
                geography, delivery_model, channel, fte, complexity, capability,
                f"{base_annual_cost*currency_factor:.2f}", f"{discount_markup}%", attrition, 
                f"{annual_cost_with_attrition*currency_factor:.2f}",
                f"{acv_converted:.2f}", f"{tcv_converted:.2f}", f"{margin_pct:.2f}", 
                f"{cost_per_fte*currency_factor:.2f}", f"{revenue_per_fte*currency_factor:.2f}", currency
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
        json_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "geography": geography,
                "delivery_model": delivery_model,
                "currency": currency
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
                "base_annual_cost": float(base_annual_cost * currency_factor),
                "annual_cost": float(annual_cost_with_attrition * currency_factor),
                "acv": float(acv_converted),
                "tcv": float(tcv_converted),
                "margin_dollars": float(margin_converted),
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
        st.info("✅ **Data Ready**\n\nDownload scenarios for sharing")


# ==================== TAB 2: COMPARISON MODE (TIER 3) ====================
with tab2:
    st.header("🔄 Scenario Comparison (TIER 3)")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved yet. Create and save scenarios in the Calculator tab first!")
    else:
        st.write(f"**Saved Scenarios:** {len(st.session_state.scenarios)}")
        
        scenarios_to_compare = st.multiselect(
            "Select 2-4 scenarios to compare:",
            options=list(st.session_state.scenarios.keys()),
            max_selections=4
        )
        
        if scenarios_to_compare:
            comparison_results = []
            
            for scenario_name in scenarios_to_compare:
                params = st.session_state.scenarios[scenario_name]
                
                # Calculate for each scenario
                base_cost = BASE_COSTS[params["geography"]] * params["fte"] * COMPLEXITY[params["complexity"]] * DELIVERY_MODELS[params["delivery_model"]] * CHANNELS[params["channel"]]
                adjusted_cost = base_cost * (1 + params["discount_markup"] / 100)
                attrition_cost = adjusted_cost * ATTRITION_RATES[params["attrition"]]
                final_cost = adjusted_cost + attrition_cost
                margin = MARGINS[params["capability"]]
                acv_scenario = final_cost / (1 - margin)
                tcv_scenario = acv_scenario * params["years"]
                margin_dollars_scenario = acv_scenario - final_cost
                margin_pct_scenario = (margin_dollars_scenario / acv_scenario) * 100
                
                currency_factor = CURRENCIES[params["currency"]]
                currency_sym = CURRENCY_SYMBOLS[params["currency"]]
                
                comparison_results.append({
                    "Scenario": scenario_name,
                    "Geography": params["geography"],
                    "FTEs": params["fte"],
                    "Complexity": params["complexity"],
                    "Annual Cost": f"{currency_sym}{final_cost*currency_factor:,.0f}",
                    "ACV": f"{currency_sym}{acv_scenario*currency_factor:,.0f}",
                    "TCV": f"{currency_sym}{tcv_scenario*currency_factor:,.0f}",
                    "Margin %": f"{margin_pct_scenario:.1f}%"
                })
            
            st.subheader("📊 Side-by-Side Comparison")
            st.dataframe(pd.DataFrame(comparison_results), use_container_width=True)
            
            # Find best option
            if len(comparison_results) > 1:
                st.subheader("🏆 Recommendation")
                best_margin = max([float(r["Margin %"].rstrip("%")) for r in comparison_results])
                best_scenario = [r["Scenario"] for r in comparison_results if float(r["Margin %"].rstrip("%")) == best_margin][0]
                st.success(f"**Highest Margin:** {best_scenario} ({best_margin:.1f}%)")


# ==================== TAB 3: PRICING TIERS (TIER 3) ====================
with tab3:
    st.header("💎 Pricing Tiers (TIER 3)")
    
    st.write("Compare our three service tiers:")
    
    col1, col2, col3 = st.columns(3)
    
    tier_geographies = st.selectbox("Compare tiers for:", list(BASE_COSTS.keys()), key="tier_geo")
    tier_fte = st.slider("Number of FTEs:", 10, 500, 50, key="tier_fte")
    tier_complexity = st.selectbox("Complexity:", list(COMPLEXITY.keys()), key="tier_comp")
    tier_years = st.slider("Contract Years:", 1, 5, 3, key="tier_years")
    
    tier_results = []
    
    for tier_name, tier_info in PRICING_TIERS.items():
        base = BASE_COSTS[tier_geographies] * tier_fte * COMPLEXITY[tier_complexity]
        margin = tier_info["margin"]
        acv_tier = base / (1 - margin)
        tcv_tier = acv_tier * tier_years
        margin_dollars_tier = acv_tier - base
        
        tier_results.append({
            "Tier": tier_name,
            "SLA": tier_info["sla"],
            "Support": tier_info["support"],
            "Margin Target": f"{margin*100:.0f}%",
            "Annual Cost": f"${base:,.0f}",
            "ACV": f"${acv_tier:,.0f}",
            "TCV": f"${tcv_tier:,.0f}",
            "Margin $": f"${margin_dollars_tier:,.0f}"
        })
    
    st.subheader("📊 Pricing Tier Comparison")
    st.dataframe(pd.DataFrame(tier_results), use_container_width=True)
    
    st.info("💡 **Recommendation:** Choose Bronze for price-sensitive, Gold for premium customers")


# ==================== TAB 4: MULTI-CURRENCY (TIER 3) ====================
with tab4:
    st.header("🌍 Multi-Currency Support (TIER 3)")
    
    st.write("View pricing in different currencies with real-time conversion.")
    
    multi_geo = st.selectbox("Geography:", list(BASE_COSTS.keys()), key="multi_geo")
    multi_fte = st.slider("FTEs:", 10, 500, 50, key="multi_fte")
    multi_comp = st.selectbox("Complexity:", list(COMPLEXITY.keys()), key="multi_comp")
    multi_cap = st.selectbox("Capability:", list(MARGINS.keys()), key="multi_cap")
    
    base = BASE_COSTS[multi_geo] * multi_fte * COMPLEXITY[multi_comp]
    margin = MARGINS[multi_cap]
    acv_base = base / (1 - margin)
    
    currency_results = []
    
    for curr, factor in CURRENCIES.items():
        symbol = CURRENCY_SYMBOLS[curr]
        currency_results.append({
            "Currency": curr,
            "Symbol": symbol,
            "Annual Cost": f"{symbol}{base*factor:,.0f}",
            "ACV": f"{symbol}{acv_base*factor:,.0f}",
            "Conversion Factor": f"{factor}x"
        })
    
    st.subheader("💱 Currency Conversion Table")
    st.dataframe(pd.DataFrame(currency_results), use_container_width=True)
    
    st.info("📌 **Conversion Rates:** Based on current market rates (USD base)")


# ==================== FOOTER ====================
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.success("✅ **LBG Pricing Calculator - Enterprise Edition**")
with col2:
    st.caption("🚀 TIER 1 + TIER 2 + TIER 3 Features | Multi-Currency | Comparison Mode | Pricing Tiers")
