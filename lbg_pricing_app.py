import streamlit as st
import pandas as pd
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Enterprise Pricing Platform", layout="wide")

st.title("🎯 Dynamic Pricing Platform - Template Edition")
st.markdown("**Master Template | Any Project Type | Maximum Flexibility**")
st.markdown("---")

# ==================== PREDEFINED DATA ====================
# Based on master file structure

GEOGRAPHIES = {
    "IND": {"name": "India (Mumbai, Bangalore)", "currency": "INR", "base_salary": 15000},
    "PHP": {"name": "Philippines", "currency": "PHP", "base_salary": 18000},
    "UK": {"name": "United Kingdom", "currency": "GBP", "base_salary": 32000},
    "US": {"name": "United States", "currency": "USD", "base_salary": 45000},
    "MEX": {"name": "Mexico", "currency": "MXN", "base_salary": 22000},
    "AUS": {"name": "Australia", "currency": "AUD", "base_salary": 58000},
    "SA": {"name": "South Africa", "currency": "ZAR", "base_salary": 18000},
    "ROM": {"name": "Romania", "currency": "EUR", "base_salary": 28000},
    "TT": {"name": "Trinidad & Tobago", "currency": "TTD", "base_salary": 20000}
}

SKILL_TYPES = {
    "Voice": {"description": "Voice/Phone Support", "color": "🎧", "icon": "☎️"},
    "Non-Voice": {"description": "Chat/Email/Digital", "color": "💬", "icon": "💻"},
    "Backoffice": {"description": "Back Office/Processing", "color": "📋", "icon": "📊"}
}

COMPLEXITY_LEVELS = {
    "L1": {"description": "Level 1 - Basic", "multiplier": 1.0},
    "L2": {"description": "Level 2 - Intermediate", "multiplier": 1.15},
    "L3": {"description": "Level 3 - Advanced", "multiplier": 1.35},
    "L4": {"description": "Level 4 - Expert", "multiplier": 1.60},
    "L5": {"description": "Level 5 - Specialized", "multiplier": 1.85},
    "L6": {"description": "Level 6 - Premium", "multiplier": 2.10}
}

WFO_OPTIONS = {
    "100% WFO": 1.00,
    "80% WFO": 0.80,
    "50% WFO": 0.50,
    "20% WFO": 0.20,
    "100% WFH": 0.00
}

SHRINKAGE_FACTORS = {
    "Low (5%)": 0.05,
    "Normal (10%)": 0.10,
    "High (15%)": 0.15,
    "Very High (20%)": 0.20
}

ATTRITION_RATES = {
    "Low (5%)": 0.05,
    "Medium (10%)": 0.10,
    "High (15%)": 0.15,
    "Critical (25%)": 0.25
}

CURRENCIES = {
    "USD": 1.0,
    "GBP": 1.27,
    "EUR": 0.92,
    "INR": 82.5,
    "PHP": 55.0,
    "AUD": 1.50,
    "ZAR": 18.0,
    "MXN": 17.0,
    "TTD": 6.75
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "INR": "₹",
    "PHP": "₱",
    "AUD": "A$",
    "ZAR": "R",
    "MXN": "Mex$",
    "TTD": "TT$"
}

RISK_CATEGORIES = {
    "Operational Risk": {
        "Attrition": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.20},
        "Quality": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Compliance": {"Low": 0.03, "Medium": 0.07, "High": 0.12, "Critical": 0.18},
        "Technology": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15}
    },
    "Financial Risk": {
        "Currency": {"Low": 0.01, "Medium": 0.03, "High": 0.06, "Critical": 0.10},
        "Volume": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Inflation": {"Low": 0.02, "Medium": 0.04, "High": 0.07, "Critical": 0.12},
        "Margin": {"Low": 0.03, "Medium": 0.06, "High": 0.10, "Critical": 0.15}
    },
    "Client Risk": {
        "Concentration": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Renewal": {"Low": 0.03, "Medium": 0.07, "High": 0.12, "Critical": 0.20},
        "Scope Creep": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "SLA Risk": {"Low": 0.02, "Medium": 0.04, "High": 0.08, "Critical": 0.12}
    },
    "Market Risk": {
        "Volatility": {"Low": 0.02, "Medium": 0.04, "High": 0.08, "Critical": 0.12},
        "Competition": {"Low": 0.03, "Medium": 0.06, "High": 0.10, "Critical": 0.15},
        "Regulatory": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Geopolitical": {"Low": 0.01, "Medium": 0.03, "High": 0.06, "Critical": 0.12}
    }
}

# ==================== SESSION STATE ====================
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

if 'templates' not in st.session_state:
    st.session_state.templates = {}

if 'risk_assessments' not in st.session_state:
    st.session_state.risk_assessments = {}

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Calculator",
    "📚 Templates",
    "🔄 Comparison",
    "⚠️ Risk Assessment",
    "🎯 Decision Dashboard",
    "💹 ROI Analysis",
    "📈 Advanced Analysis",
    "⚙️ Settings"
])

# ==================== TAB 1: CALCULATOR ====================
with tab1:
    st.header("📊 Dynamic Pricing Calculator")
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        skill_type = st.selectbox("🎯 Skill Type", list(SKILL_TYPES.keys()), key="skill_type")
        st.caption(SKILL_TYPES[skill_type]['description'])
    
    with col2:
        complexity = st.selectbox("📊 Complexity Level", list(COMPLEXITY_LEVELS.keys()), key="complexity")
        st.caption(COMPLEXITY_LEVELS[complexity]['description'])
    
    with col3:
        geography = st.selectbox("🌍 Geography", list(GEOGRAPHIES.keys()), key="geography")
        st.caption(GEOGRAPHIES[geography]['name'])
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        base_salary = st.number_input("Base Monthly Salary", value=GEOGRAPHIES[geography]['base_salary'], step=1000, key="salary")
    with col2:
        ftes = st.slider("Number of FTEs/Agents", 10, 2000, 100, step=10, key="ftes")
    with col3:
        wfo_model = st.selectbox("WFO/WFH Model", list(WFO_OPTIONS.keys()), key="wfo")
    with col4:
        years = st.slider("Contract Duration (Years)", 1, 10, 3, key="years")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        currency = st.selectbox("Currency", list(CURRENCIES.keys()), key="currency")
    with col2:
        shrinkage = st.selectbox("Shrinkage Rate", list(SHRINKAGE_FACTORS.keys()), key="shrinkage")
    with col3:
        attrition = st.selectbox("Attrition Rate", list(ATTRITION_RATES.keys()), key="attrition")
    with col4:
        margin_target = st.slider("Target Margin (%)", 15, 50, 30, step=2, key="margin")
    
    st.markdown("---")
    
    st.subheader("💰 Cost Components (%)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        salary_pct = st.slider("Salary", 50, 75, 60, step=1, key="salary_pct")
    with col2:
        benefits_pct = st.slider("Benefits", 5, 20, 12, step=1, key="benefits_pct")
    with col3:
        overhead_pct = st.slider("Overhead", 5, 20, 15, step=1, key="overhead_pct")
    with col4:
        training_pct = st.slider("Training", 3, 15, 5, step=1, key="training_pct")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        onboarding_pct = st.slider("Onboarding", 0, 30, 10, step=2, key="onboarding_pct")
    with col2:
        qa_cost_pct = st.slider("QA/Audit", 0, 15, 5, step=1, key="qa_cost_pct")
    with col3:
        compliance_pct = st.slider("Compliance", 0, 10, 3, step=1, key="compliance_pct")
    with col4:
        tools_pct = st.slider("Tools/Tech", 2, 10, 5, step=1, key="tools_pct")
    
    st.markdown("---")
    
    st.subheader("📅 Ramp-Up Schedule")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Months 1-3**")
        ramp_m1_util = st.slider("Utilization %", 20, 100, 40, step=5, key="ramp_m1")
        ramp_m1_bonus = st.slider("Ramp Cost %", 0, 50, 15, step=5, key="ramp_m1_bonus")
    
    with col2:
        st.write("**Months 4-6**")
        ramp_m4_util = st.slider("Utilization %", 50, 100, 70, step=5, key="ramp_m4")
        ramp_m4_bonus = st.slider("Ramp Cost %", 0, 30, 8, step=5, key="ramp_m4_bonus")
    
    with col3:
        st.write("**Months 7+**")
        ramp_m7_util = st.slider("Utilization %", 75, 100, 100, step=5, key="ramp_m7")
        ramp_m7_bonus = st.slider("Ramp Cost %", 0, 20, 0, step=5, key="ramp_m7_bonus")
    
    st.markdown("---")
    
    st.subheader("🎁 Incentives & Adjustments")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        retention_bonus = st.slider("Retention Bonus %", 0, 30, 5, step=2, key="retention_bonus")
    with col2:
        performance_bonus = st.slider("Performance Bonus %", 0, 25, 3, step=2, key="performance_bonus")
    with col3:
        skill_premium = st.slider("Skill Premium %", 0, 50, 10, step=5, key="skill_premium")
    with col4:
        discount_markup = st.slider("Discount/Markup %", -50, 100, 0, step=5, key="discount_markup")
    
    st.markdown("---")
    
    # ==================== CALCULATIONS ====================
    
    wfo_factor = WFO_OPTIONS[wfo_model]
    complexity_mult = COMPLEXITY_LEVELS[complexity]['multiplier']
    shrinkage_rate = SHRINKAGE_FACTORS[shrinkage]
    attrition_rate = ATTRITION_RATES[attrition]
    currency_factor = CURRENCIES[currency]
    currency_symbol = CURRENCY_SYMBOLS[currency]
    
    # Base cost per FTE (annual)
    total_cost_pct = salary_pct + benefits_pct + overhead_pct + training_pct
    monthly_cost = base_salary * (total_cost_pct / salary_pct) if salary_pct > 0 else 0
    annual_cost_base = monthly_cost * 12
    
    # Apply complexity and WFO
    annual_cost_adjusted = annual_cost_base * complexity_mult * (1 + (1 - wfo_factor) * 0.15)
    
    # Add additional costs
    onboarding_cost = (base_salary * 12) * (onboarding_pct / 100)
    qa_cost = annual_cost_adjusted * (qa_cost_pct / 100)
    compliance_cost = annual_cost_adjusted * (compliance_pct / 100)
    tools_cost = annual_cost_adjusted * (tools_pct / 100)
    
    total_annual_cost_fte = annual_cost_adjusted + onboarding_cost + qa_cost + compliance_cost + tools_cost
    
    # Apply shrinkage and attrition
    shrinkage_cost = total_annual_cost_fte * shrinkage_rate
    attrition_cost_fte = total_annual_cost_fte * attrition_rate
    
    total_annual_cost_per_fte = total_annual_cost_fte + shrinkage_cost + attrition_cost_fte
    
    # Total team cost
    total_team_cost = total_annual_cost_per_fte * ftes
    
    # Ramp-up adjustments (Year 1)
    ramp_cost_m1 = (base_salary * 12 * ramp_m1_bonus / 100) * ftes * 0.25
    ramp_cost_m4 = (base_salary * 12 * ramp_m4_bonus / 100) * ftes * 0.25
    ramp_cost_m7 = (base_salary * 12 * ramp_m7_bonus / 100) * ftes * 0.50
    total_ramp_cost = ramp_cost_m1 + ramp_cost_m4 + ramp_cost_m7
    
    # Incentives (Year 1)
    retention_cost = (base_salary * 12 * retention_bonus / 100) * ftes
    performance_cost = (base_salary * 12 * performance_bonus / 100) * ftes
    skill_cost = (base_salary * 12 * skill_premium / 100) * ftes
    
    total_y1_cost = total_team_cost + total_ramp_cost + retention_cost + performance_cost + skill_cost
    
    # Apply discount/markup
    discount_factor = 1 + (discount_markup / 100)
    final_y1_cost = total_y1_cost * discount_factor
    
    # Revenue calculation
    margin_decimal = margin_target / 100
    acv = final_y1_cost / (1 - margin_decimal)
    tcv = acv * years
    margin_dollars = acv - final_y1_cost
    margin_pct_calc = (margin_dollars / acv) * 100
    
    # Convert to selected currency
    acv_local = acv * currency_factor
    tcv_local = tcv * currency_factor
    margin_local = margin_dollars * currency_factor
    
    # ==================== DISPLAY ====================
    
    st.markdown("---")
    st.subheader("💰 KEY METRICS")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Annual Cost/FTE", f"{currency_symbol}{total_annual_cost_per_fte*currency_factor:,.0f}")
    with col2:
        st.metric("Team Annual Cost", f"{currency_symbol}{total_team_cost*currency_factor:,.0f}")
    with col3:
        st.metric("ACV", f"{currency_symbol}{acv_local:,.0f}")
    with col4:
        st.metric("TCV", f"{currency_symbol}{tcv_local:,.0f}")
    with col5:
        st.metric("Margin %", f"{margin_pct_calc:.1f}%")
    
    st.markdown("---")
    
    st.subheader("📊 Cost Breakdown")
    
    cost_breakdown = pd.DataFrame({
        "Component": ["Salary", "Benefits", "Overhead", "Training", "QA/Audit", "Compliance", "Tools/Tech", "Onboarding (Y1)", "Shrinkage", "Attrition", "TOTAL/FTE"],
        "Annual Cost/FTE": [
            f"{currency_symbol}{(annual_cost_adjusted * salary_pct / total_cost_pct)*currency_factor:,.0f}",
            f"{currency_symbol}{(annual_cost_adjusted * benefits_pct / total_cost_pct)*currency_factor:,.0f}",
            f"{currency_symbol}{(annual_cost_adjusted * overhead_pct / total_cost_pct)*currency_factor:,.0f}",
            f"{currency_symbol}{(annual_cost_adjusted * training_pct / total_cost_pct)*currency_factor:,.0f}",
            f"{currency_symbol}{qa_cost*currency_factor:,.0f}",
            f"{currency_symbol}{compliance_cost*currency_factor:,.0f}",
            f"{currency_symbol}{tools_cost*currency_factor:,.0f}",
            f"{currency_symbol}{(onboarding_cost/ftes)*currency_factor:,.0f}",
            f"{currency_symbol}{shrinkage_cost*currency_factor:,.0f}",
            f"{currency_symbol}{attrition_cost_fte*currency_factor:,.0f}",
            f"{currency_symbol}{total_annual_cost_per_fte*currency_factor:,.0f}"
        ]
    })
    
    st.dataframe(cost_breakdown, use_container_width=True)
    
    st.markdown("---")
    
    # Scenario name and save
    scenario_name = st.text_input("Scenario Name", value=f"{skill_type}_{complexity}_{geography}_{datetime.now().strftime('%Y%m%d')}", key="scenario_name")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Scenario"):
            st.session_state.scenarios[scenario_name] = {
                "skill_type": skill_type,
                "complexity": complexity,
                "geography": geography,
                "base_salary": base_salary,
                "ftes": ftes,
                "wfo_model": wfo_model,
                "years": years,
                "currency": currency,
                "shrinkage": shrinkage,
                "attrition": attrition,
                "margin_target": margin_target,
                "acv": acv_local,
                "tcv": tcv_local,
                "margin_pct": margin_pct_calc,
                "annual_cost": total_team_cost * currency_factor,
                "timestamp": datetime.now().isoformat()
            }
            st.success(f"✅ Saved: {scenario_name}")
    
    with col2:
        if st.button("📥 Save as Template"):
            st.session_state.templates[scenario_name] = {
                "skill_type": skill_type,
                "complexity": complexity,
                "geography": geography,
                "wfo_model": wfo_model,
                "currency": currency,
                "margin_target": margin_target,
                "salary_pct": salary_pct,
                "benefits_pct": benefits_pct,
                "overhead_pct": overhead_pct,
                "training_pct": training_pct
            }
            st.success(f"✅ Template Saved: {scenario_name}")
    
    with col3:
        st.metric(f"Scenarios: {len(st.session_state.scenarios)}", "✅")


# ==================== TAB 2: TEMPLATES ====================
with tab2:
    st.header("📚 Pricing Templates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Saved Templates")
        if len(st.session_state.templates) > 0:
            for template_name, template in st.session_state.templates.items():
                st.write(f"**{template_name}**")
                st.caption(f"{template['skill_type']} | {template['complexity']} | {template['geography']}")
        else:
            st.info("No templates saved yet")
    
    with col2:
        st.subheader("Quick Start Templates")
        quick_templates = {
            "Voice L1 (India)": {"skill_type": "Voice", "complexity": "L1", "geography": "IND", "margin_target": 30},
            "Backoffice L2 (Philippines)": {"skill_type": "Backoffice", "complexity": "L2", "geography": "PHP", "margin_target": 35},
            "Non-Voice L3 (US)": {"skill_type": "Non-Voice", "complexity": "L3", "geography": "US", "margin_target": 28}
        }
        
        for template_name, template in quick_templates.items():
            st.write(f"**{template_name}**")


# ==================== TAB 3: COMPARISON ====================
with tab3:
    st.header("🔄 Scenario Comparison")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved. Create some in the Calculator tab first!")
    else:
        scenarios_list = list(st.session_state.scenarios.keys())
        selected_scenarios = st.multiselect("Select scenarios to compare", scenarios_list, max_selections=6)
        
        if selected_scenarios:
            comparison_data = []
            for scenario_name in selected_scenarios:
                s = st.session_state.scenarios[scenario_name]
                comparison_data.append({
                    "Scenario": scenario_name,
                    "Skill Type": s["skill_type"],
                    "Complexity": s["complexity"],
                    "Geography": s["geography"],
                    "FTEs": s["ftes"],
                    "Annual Cost": f"{s['currency']}{s['annual_cost']:,.0f}",
                    "ACV": f"{s['currency']}{s['acv']:,.0f}",
                    "TCV": f"{s['currency']}{s['tcv']:,.0f}",
                    "Margin %": f"{s['margin_pct']:.1f}%"
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)


# ==================== TAB 4: RISK ASSESSMENT ====================
with tab4:
    st.header("⚠️ Risk Assessment")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ Create scenarios first!")
    else:
        risk_scenario = st.selectbox("Select Scenario", list(st.session_state.scenarios.keys()), key="risk_scenario")
        
        st.markdown("---")
        st.subheader("Risk Scoring")
        
        with st.expander("🏭 OPERATIONAL RISK", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                op_attrition = st.selectbox("Attrition Risk", ["Low", "Medium", "High", "Critical"], key="op_attrition")
                op_quality = st.selectbox("Quality Risk", ["Low", "Medium", "High", "Critical"], key="op_quality")
            with col2:
                op_compliance = st.selectbox("Compliance Risk", ["Low", "Medium", "High", "Critical"], key="op_compliance")
                op_tech = st.selectbox("Technology Risk", ["Low", "Medium", "High", "Critical"], key="op_tech")
            
            op_score = (
                RISK_CATEGORIES["Operational Risk"]["Attrition"][op_attrition] +
                RISK_CATEGORIES["Operational Risk"]["Quality"][op_quality] +
                RISK_CATEGORIES["Operational Risk"]["Compliance"][op_compliance] +
                RISK_CATEGORIES["Operational Risk"]["Technology"][op_tech]
            ) / 4
            
            st.metric("Operational Risk Score", f"{op_score:.2%}")
        
        with st.expander("💰 FINANCIAL RISK"):
            col1, col2 = st.columns(2)
            with col1:
                fin_currency = st.selectbox("Currency Risk", ["Low", "Medium", "High", "Critical"], key="fin_currency")
                fin_volume = st.selectbox("Volume Risk", ["Low", "Medium", "High", "Critical"], key="fin_volume")
            with col2:
                fin_inflation = st.selectbox("Cost Inflation Risk", ["Low", "Medium", "High", "Critical"], key="fin_inflation")
                fin_margin = st.selectbox("Margin Compression Risk", ["Low", "Medium", "High", "Critical"], key="fin_margin")
            
            fin_score = (
                RISK_CATEGORIES["Financial Risk"]["Currency"][fin_currency] +
                RISK_CATEGORIES["Financial Risk"]["Volume"][fin_volume] +
                RISK_CATEGORIES["Financial Risk"]["Inflation"][fin_inflation] +
                RISK_CATEGORIES["Financial Risk"]["Margin"][fin_margin]
            ) / 4
            
            st.metric("Financial Risk Score", f"{fin_score:.2%}")
        
        with st.expander("🤝 CLIENT RISK"):
            col1, col2 = st.columns(2)
            with col1:
                client_concentration = st.selectbox("Client Concentration", ["Low", "Medium", "High", "Critical"], key="client_concentration")
                client_renewal = st.selectbox("Contract Renewal Risk", ["Low", "Medium", "High", "Critical"], key="client_renewal")
            with col2:
                client_scope = st.selectbox("Scope Creep Risk", ["Low", "Medium", "High", "Critical"], key="client_scope")
                client_sla = st.selectbox("SLA Non-Performance", ["Low", "Medium", "High", "Critical"], key="client_sla")
            
            client_score = (
                RISK_CATEGORIES["Client Risk"]["Concentration"][client_concentration] +
                RISK_CATEGORIES["Client Risk"]["Renewal"][client_renewal] +
                RISK_CATEGORIES["Client Risk"]["Scope Creep"][client_scope] +
                RISK_CATEGORIES["Client Risk"]["SLA Risk"][client_sla]
            ) / 4
            
            st.metric("Client Risk Score", f"{client_score:.2%}")
        
        with st.expander("📈 MARKET RISK"):
            col1, col2 = st.columns(2)
            with col1:
                market_volatility = st.selectbox("Market Volatility", ["Low", "Medium", "High", "Critical"], key="market_volatility")
                market_competition = st.selectbox("Competition Risk", ["Low", "Medium", "High", "Critical"], key="market_competition")
            with col2:
                market_regulatory = st.selectbox("Regulatory Risk", ["Low", "Medium", "High", "Critical"], key="market_regulatory")
                market_geopolitical = st.selectbox("Geopolitical Risk", ["Low", "Medium", "High", "Critical"], key="market_geopolitical")
            
            market_score = (
                RISK_CATEGORIES["Market Risk"]["Volatility"][market_volatility] +
                RISK_CATEGORIES["Market Risk"]["Competition"][market_competition] +
                RISK_CATEGORIES["Market Risk"]["Regulatory"][market_regulatory] +
                RISK_CATEGORIES["Market Risk"]["Geopolitical"][market_geopolitical]
            ) / 4
            
            st.metric("Market Risk Score", f"{market_score:.2%}")
        
        st.markdown("---")
        
        overall_risk = (op_score + fin_score + client_score + market_score) / 4
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("OVERALL RISK SCORE", f"{overall_risk:.2%}")
        
        with col2:
            if overall_risk < 0.05:
                st.success("🟢 LOW RISK")
            elif overall_risk < 0.10:
                st.info("🟡 MODERATE RISK")
            else:
                st.error("🔴 HIGH RISK")
        
        with col3:
            scenario = st.session_state.scenarios[risk_scenario]
            risk_adjusted_margin = scenario['margin_pct'] - (overall_risk * 100)
            st.metric("Risk-Adjusted Margin", f"{risk_adjusted_margin:.1f}%")


# ==================== TAB 5: DECISION DASHBOARD ====================
with tab5:
    st.header("🎯 Decision Support Dashboard")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ Create scenarios first!")
    else:
        decision_scenario = st.selectbox("Select Scenario", list(st.session_state.scenarios.keys()), key="decision_scenario")
        scenario = st.session_state.scenarios[decision_scenario]
        
        st.subheader("Deal Scoring Matrix")
        
        col1, col2 = st.columns(2)
        with col1:
            margin_score = st.slider("Margin Attractiveness", 1, 10, 7, key="margin_score")
            growth_score = st.slider("Growth Potential", 1, 10, 6, key="growth_score")
            client_quality = st.slider("Client Quality", 1, 10, 7, key="client_quality")
            stability_score = st.slider("Market Stability", 1, 10, 6, key="stability_score")
        
        with col2:
            risk_score = st.slider("Risk Level (1=High, 10=Low)", 1, 10, 5, key="risk_score")
            execution = st.slider("Execution Capability", 1, 10, 7, key="execution")
            scalability = st.slider("Scalability", 1, 10, 6, key="scalability")
            strategic_fit = st.slider("Strategic Alignment", 1, 10, 7, key="strategic_fit")
        
        weights = {"Margin": 0.20, "Growth": 0.15, "Client": 0.15, "Stability": 0.10, "Risk": 0.15, "Execution": 0.10, "Scalability": 0.10, "Strategic": 0.05}
        
        weighted_score = (
            margin_score * weights["Margin"] + growth_score * weights["Growth"] +
            client_quality * weights["Client"] + stability_score * weights["Stability"] +
            risk_score * weights["Risk"] + execution * weights["Execution"] +
            scalability * weights["Scalability"] + strategic_fit * weights["Strategic"]
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Decision Score", f"{weighted_score:.1f}/10")
        with col2:
            if weighted_score >= 8:
                st.success("🟢 STRONG BUY")
            elif weighted_score >= 6.5:
                st.info("🟡 BUY")
            else:
                st.error("🔴 PASS/RECONSIDER")
        with col3:
            st.metric("Target Margin", f"{scenario['margin_pct']:.1f}%")


# ==================== TAB 6: ROI ANALYSIS ====================
with tab6:
    st.header("💹 ROI & Break-Even Analysis")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ Create scenarios first!")
    else:
        roi_scenario = st.selectbox("Select Scenario", list(st.session_state.scenarios.keys()), key="roi_scenario")
        scenario = st.session_state.scenarios[roi_scenario]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            investment = st.number_input("Initial Investment", value=100000, step=10000, key="initial_investment")
        with col2:
            discount_rate = st.slider("Discount Rate (%)", 0, 20, 10, key="discount_rate")
        with col3:
            analysis_period = st.slider("Analysis Period (Years)", 1, 10, 5, key="analysis_period")
        
        annual_profit = scenario['acv'] - scenario['annual_cost']
        breakeven_months = (investment / annual_profit * 12) if annual_profit > 0 else float('inf')
        total_profit = annual_profit * analysis_period - investment
        roi_pct = (total_profit / investment * 100) if investment > 0 else 0
        
        npv = -investment
        for year in range(1, int(analysis_period) + 1):
            npv += annual_profit / ((1 + discount_rate / 100) ** year)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Annual Profit", f"${annual_profit:,.0f}")
        with col2:
            st.metric("Break-Even (Months)", f"{breakeven_months:.1f}" if breakeven_months != float('inf') else "N/A")
        with col3:
            st.metric(f"ROI ({analysis_period:.0f}yr)", f"{roi_pct:.1f}%")
        with col4:
            st.metric(f"NPV ({discount_rate}%)", f"${npv:,.0f}")


# ==================== TAB 7: ADVANCED ANALYSIS ====================
with tab7:
    st.header("📈 Advanced Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sensitivity Analysis")
        if len(st.session_state.scenarios) > 0:
            sensitivity_scenario = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="sensitivity_scenario")
            scenario = st.session_state.scenarios[sensitivity_scenario]
            
            parameter = st.selectbox("Parameter to Vary", ["FTEs", "Salary", "Margin"], key="sensitivity_param")
            
            if parameter == "FTEs":
                variations = [scenario['ftes'] * 0.8, scenario['ftes'], scenario['ftes'] * 1.2]
                results = []
                for var in variations:
                    results.append({"Value": f"{int(var)}", "Change": f"{(var/scenario['ftes']-1)*100:+.0f}%", "Est. ACV": f"{scenario['acv'] * var / scenario['ftes']:,.0f}"})
                st.dataframe(pd.DataFrame(results), use_container_width=True)
    
    with col2:
        st.subheader("Portfolio Analysis")
        if len(st.session_state.scenarios) > 1:
            total_acv = sum([s['acv'] for s in st.session_state.scenarios.values()])
            avg_margin = np.mean([s['margin_pct'] for s in st.session_state.scenarios.values()])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Portfolio ACV", f"${total_acv:,.0f}")
            with col2:
                st.metric("Average Margin", f"{avg_margin:.1f}%")


# ==================== TAB 8: SETTINGS ====================
with tab8:
    st.header("⚙️ Settings & Configuration")
    
    st.subheader("📁 File Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Scenarios (JSON)"):
            export_data = json.dumps(st.session_state.scenarios, indent=2, default=str)
            st.download_button("Download Scenarios", export_data, "scenarios_export.json", "application/json")
    
    with col2:
        if st.button("📥 Export All Templates (JSON)"):
            export_data = json.dumps(st.session_state.templates, indent=2, default=str)
            st.download_button("Download Templates", export_data, "templates_export.json", "application/json")
    
    st.markdown("---")
    
    st.subheader("🔧 System Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Saved Scenarios", len(st.session_state.scenarios))
    with col2:
        st.metric("Saved Templates", len(st.session_state.templates))
    with col3:
        st.metric("Risk Assessments", len(st.session_state.risk_assessments))


# ==================== FOOTER ====================
st.markdown("---")
st.success("✅ **Dynamic Pricing Platform - Template Edition**")
st.caption("🎯 Template-Based | 9 Geographies | 3 Skill Types | 6 Complexity Levels | Advanced Analytics")
st.caption(f"📊 Active Scenarios: {len(st.session_state.scenarios)} | Templates: {len(st.session_state.templates)}")
