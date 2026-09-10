import streamlit as st
import pandas as pd
import json
from datetime import datetime
import numpy as np
import os

st.set_page_config(page_title="Enterprise Pricing Platform", layout="wide")

st.title("🎯 Dynamic Pricing Platform - Template Edition")
st.markdown("**Master Template | Auto-Populated Defaults | Maximum Flexibility**")
st.markdown("---")

@st.cache_data
def load_master_defaults():
    try:
        import openpyxl
        possible_names = [
            "Pricing_Master_Feb_26_v10.xlsm",
            "Pricing_Master_Feb'26_v10.xlsm",
            "Pricing Master_Feb'26_v10.xlsm",
            "Pricing Master_Feb_26_v10.xlsm",
        ]
        file_path = None
        for name in possible_names:
            if os.path.exists(name):
                file_path = name
                break
        if not file_path:
            return None
        wb = openpyxl.load_workbook(file_path, data_only=True)
        salary_defaults = {}
        sheet_geo_map = {
            "US Salary": "US", "UK Salary": "UK", "SA Salary": "SA",
            "Mexico Salary": "MEX", "Aus Salary": "AUS", "Salary PHP": "PHP",
            "IND Salary": "IND", "ROM Salary": "ROM", "T&T Salary": "TT"
        }
        for sheet_name, geo_code in sheet_geo_map.items():
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                for row in ws.iter_rows(min_row=1, max_row=100, values_only=True):
                    if row and len(row) >= 3:
                        cell0 = str(row[0]).strip() if row[0] else ""
                        cell1 = str(row[1]).strip() if row[1] else ""
                        skill_match = None
                        if "non" in cell0.lower() and "voice" in cell0.lower():
                            skill_match = "Non-voice"
                        elif "voice" in cell0.lower():
                            skill_match = "Voice"
                        elif "back" in cell0.lower() or "office" in cell0.lower():
                            skill_match = "Backoffice"
                        complexity_match = None
                        for level in ["L1", "L2", "L3", "L4", "L5", "L6"]:
                            if level in cell1 or level in cell0:
                                complexity_match = level
                                break
                        if skill_match and complexity_match:
                            for col_idx in range(2, min(len(row), 15)):
                                if row[col_idx]:
                                    try:
                                        val = float(row[col_idx])
                                        if val > 100:
                                            key = f"{skill_match}_{complexity_match}_{geo_code}"
                                            salary_defaults[key] = val
                                            break
                                    except (ValueError, TypeError):
                                        pass
        if len(salary_defaults) > 0:
            return salary_defaults
        return None
    except Exception:
        return None

master_defaults = load_master_defaults()

GEO_SALARIES = {
    "IND": {
        "Voice":      {"L1": 18000, "L2": 22000, "L3": 28000, "L4": 35000, "L5": 42000, "L6": 50000},
        "Non-voice":  {"L1": 16000, "L2": 20000, "L3": 26000, "L4": 32000, "L5": 38000, "L6": 45000},
        "Backoffice": {"L1": 15000, "L2": 19000, "L3": 24000, "L4": 30000, "L5": 36000, "L6": 42000},
    },
    "PHP": {
        "Voice":      {"L1": 20000, "L2": 25000, "L3": 32000, "L4": 40000, "L5": 48000, "L6": 58000},
        "Non-voice":  {"L1": 18000, "L2": 23000, "L3": 30000, "L4": 37000, "L5": 44000, "L6": 52000},
        "Backoffice": {"L1": 17000, "L2": 22000, "L3": 28000, "L4": 35000, "L5": 42000, "L6": 50000},
    },
    "UK": {
        "Voice":      {"L1": 2200, "L2": 2600, "L3": 3200, "L4": 3800, "L5": 4500, "L6": 5200},
        "Non-voice":  {"L1": 2000, "L2": 2400, "L3": 3000, "L4": 3600, "L5": 4200, "L6": 4800},
        "Backoffice": {"L1": 1900, "L2": 2300, "L3": 2800, "L4": 3400, "L5": 4000, "L6": 4600},
    },
    "US": {
        "Voice":      {"L1": 3200, "L2": 3800, "L3": 4500, "L4": 5500, "L5": 6500, "L6": 7500},
        "Non-voice":  {"L1": 3000, "L2": 3600, "L3": 4200, "L4": 5200, "L5": 6000, "L6": 7000},
        "Backoffice": {"L1": 2800, "L2": 3400, "L3": 4000, "L4": 5000, "L5": 5800, "L6": 6800},
    },
    "MEX": {
        "Voice":      {"L1": 14000, "L2": 17000, "L3": 22000, "L4": 28000, "L5": 34000, "L6": 40000},
        "Non-voice":  {"L1": 12000, "L2": 15000, "L3": 20000, "L4": 25000, "L5": 30000, "L6": 36000},
        "Backoffice": {"L1": 11000, "L2": 14000, "L3": 18000, "L4": 23000, "L5": 28000, "L6": 34000},
    },
    "AUS": {
        "Voice":      {"L1": 4200, "L2": 5000, "L3": 6000, "L4": 7200, "L5": 8500, "L6": 10000},
        "Non-voice":  {"L1": 3800, "L2": 4600, "L3": 5500, "L4": 6800, "L5": 8000, "L6": 9200},
        "Backoffice": {"L1": 3600, "L2": 4400, "L3": 5200, "L4": 6500, "L5": 7600, "L6": 8800},
    },
    "SA": {
        "Voice":      {"L1": 12000, "L2": 15000, "L3": 19000, "L4": 24000, "L5": 29000, "L6": 35000},
        "Non-voice":  {"L1": 10000, "L2": 13000, "L3": 17000, "L4": 22000, "L5": 27000, "L6": 32000},
        "Backoffice": {"L1": 9000, "L2": 12000, "L3": 16000, "L4": 20000, "L5": 25000, "L6": 30000},
    },
    "ROM": {
        "Voice":      {"L1": 3500, "L2": 4200, "L3": 5200, "L4": 6500, "L5": 7800, "L6": 9000},
        "Non-voice":  {"L1": 3200, "L2": 3900, "L3": 4800, "L4": 6000, "L5": 7200, "L6": 8400},
        "Backoffice": {"L1": 3000, "L2": 3700, "L3": 4500, "L4": 5700, "L5": 6800, "L6": 8000},
    },
    "TT": {
        "Voice":      {"L1": 8000, "L2": 10000, "L3": 13000, "L4": 16000, "L5": 19000, "L6": 23000},
        "Non-voice":  {"L1": 7000, "L2": 9000, "L3": 12000, "L4": 15000, "L5": 18000, "L6": 21000},
        "Backoffice": {"L1": 6500, "L2": 8500, "L3": 11000, "L4": 14000, "L5": 17000, "L6": 20000},
    },
}

GEOGRAPHIES = {
    "IND": {"name": "India", "currency": "INR", "symbol": "₹"},
    "PHP": {"name": "Philippines", "currency": "PHP", "symbol": "₱"},
    "UK":  {"name": "United Kingdom", "currency": "GBP", "symbol": "£"},
    "US":  {"name": "United States", "currency": "USD", "symbol": "$"},
    "MEX": {"name": "Mexico", "currency": "MXN", "symbol": "Mex$"},
    "AUS": {"name": "Australia", "currency": "AUD", "symbol": "A$"},
    "SA":  {"name": "South Africa", "currency": "ZAR", "symbol": "R"},
    "ROM": {"name": "Romania", "currency": "EUR", "symbol": "€"},
    "TT":  {"name": "Trinidad & Tobago", "currency": "TTD", "symbol": "TT$"},
}

SKILL_TYPES = {
    "Voice": {"description": "Voice/Phone Support"},
    "Non-voice": {"description": "Chat/Email/Digital"},
    "Backoffice": {"description": "Back Office/Processing"}
}

COMPLEXITY_LEVELS = {
    "L1": {"description": "Level 1 - Basic", "multiplier": 1.0},
    "L2": {"description": "Level 2 - Intermediate", "multiplier": 1.15},
    "L3": {"description": "Level 3 - Advanced", "multiplier": 1.35},
    "L4": {"description": "Level 4 - Expert", "multiplier": 1.60},
    "L5": {"description": "Level 5 - Specialized", "multiplier": 1.85},
    "L6": {"description": "Level 6 - Premium", "multiplier": 2.10}
}

WFO_OPTIONS = {"100% WFO": 1.00, "80% WFO": 0.80, "50% WFO": 0.50, "20% WFO": 0.20, "100% WFH": 0.00}
SHRINKAGE_FACTORS = {"Low (5%)": 0.05, "Normal (10%)": 0.10, "High (15%)": 0.15, "Very High (20%)": 0.20}
ATTRITION_RATES = {"Low (5%)": 0.05, "Medium (10%)": 0.10, "High (15%)": 0.15, "Critical (25%)": 0.25}
CURRENCIES = {"USD": 1.0, "GBP": 1.27, "EUR": 0.92, "INR": 82.5, "PHP": 55.0, "AUD": 1.50, "ZAR": 18.0, "MXN": 17.0, "TTD": 6.75}
CURRENCY_SYMBOLS = {"USD": "$", "GBP": "£", "EUR": "€", "INR": "₹", "PHP": "₱", "AUD": "A$", "ZAR": "R", "MXN": "Mex$", "TTD": "TT$"}

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

def get_salary(skill_type, complexity, geography):
    if master_defaults:
        key = f"{skill_type}_{complexity}_{geography}"
        if key in master_defaults:
            return int(master_defaults[key])
    if geography in GEO_SALARIES and skill_type in GEO_SALARIES[geography] and complexity in GEO_SALARIES[geography][skill_type]:
        return GEO_SALARIES[geography][skill_type][complexity]
    return 15000

if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}
if 'templates' not in st.session_state:
    st.session_state.templates = {}
if 'prev_selection' not in st.session_state:
    st.session_state.prev_selection = ""
if 'dynamic_salary' not in st.session_state:
    st.session_state.dynamic_salary = 18000

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Calculator", "📚 Templates", "🔄 Comparison", "⚠️ Risk Assessment",
    "🎯 Decision Dashboard", "💹 ROI Analysis", "📈 Advanced Analysis", "⚙️ Settings"
])

with tab1:
    st.header("📊 Dynamic Pricing Calculator")
    if master_defaults:
        st.success(f"✅ Master file loaded — {len(master_defaults)} salary entries from geography sheets")
    else:
        st.info("ℹ️ Using built-in salary defaults per Geography × Skill × Level")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        skill_type = st.selectbox("🎯 Skill Type", list(SKILL_TYPES.keys()), key="skill_type")
        st.caption(SKILL_TYPES[skill_type]['description'])
    with col2:
        complexity = st.selectbox("📊 Complexity Level", list(COMPLEXITY_LEVELS.keys()), key="complexity")
        st.caption(COMPLEXITY_LEVELS[complexity]['description'])
    with col3:
        geography = st.selectbox("🌍 Geography", list(GEOGRAPHIES.keys()), key="geography",
                                  format_func=lambda x: f"{x} — {GEOGRAPHIES[x]['name']}")

    current_selection = f"{skill_type}_{complexity}_{geography}"
    default_salary = get_salary(skill_type, complexity, geography)
    geo_currency = GEOGRAPHIES[geography]['currency']
    geo_symbol = GEOGRAPHIES[geography]['symbol']

    if current_selection != st.session_state.prev_selection:
        st.session_state.prev_selection = current_selection
        st.session_state.dynamic_salary = default_salary

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        base_salary = st.number_input(
            f"💰 Base Monthly Salary ({geo_symbol})",
            value=st.session_state.dynamic_salary,
            step=1000, min_value=100,
            key=f"salary_{current_selection}"
        )
        source = "📂 Master file" if master_defaults and f"{skill_type}_{complexity}_{geography}" in master_defaults else "📋 Built-in default"
        st.caption(f"{source} | {geo_currency}")
    with col2:
        ftes = st.number_input("👥 Number of FTEs", value=100, step=10, min_value=1, max_value=5000, key="ftes")
    with col3:
        wfo_model = st.selectbox("🏢 WFO/WFH Model", list(WFO_OPTIONS.keys()), key="wfo")
    with col4:
        years = st.slider("📅 Contract (Years)", 1, 10, 3, key="years")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        currency_list = list(CURRENCIES.keys())
        default_idx = currency_list.index(geo_currency) if geo_currency in currency_list else 0
        currency = st.selectbox("💱 Display Currency", currency_list, index=default_idx, key="currency")
    with col2:
        shrinkage = st.selectbox("📉 Shrinkage", list(SHRINKAGE_FACTORS.keys()), key="shrinkage")
    with col3:
        attrition = st.selectbox("🔄 Attrition", list(ATTRITION_RATES.keys()), key="attrition")
    with col4:
        margin_target = st.slider("🎯 Target Margin %", 15, 50, 30, step=2, key="margin")

    st.markdown("---")

    st.subheader("💰 Cost Components (%)")
    col1, col2, col3, col4 = st.columns(4)
    with col1: salary_pct = st.slider("Salary", 50, 75, 60, key="salary_pct")
    with col2: benefits_pct = st.slider("Benefits", 5, 20, 12, key="benefits_pct")
    with col3: overhead_pct = st.slider("Overhead", 5, 20, 15, key="overhead_pct")
    with col4: training_pct = st.slider("Training", 3, 15, 5, key="training_pct")

    col1, col2, col3, col4 = st.columns(4)
    with col1: onboarding_pct = st.slider("Onboarding", 0, 30, 10, step=2, key="onboarding_pct")
    with col2: qa_cost_pct = st.slider("QA/Audit", 0, 15, 5, key="qa_cost_pct")
    with col3: compliance_pct = st.slider("Compliance", 0, 10, 3, key="compliance_pct")
    with col4: tools_pct = st.slider("Tools/Tech", 2, 10, 5, key="tools_pct")

    st.markdown("---")

    st.subheader("📅 Ramp-Up Schedule")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Months 1-3**")
        ramp_m1_bonus = st.slider("Ramp Cost %", 0, 50, 15, step=5, key="ramp_m1_bonus")
    with col2:
        st.write("**Months 4-6**")
        ramp_m4_bonus = st.slider("Ramp Cost %", 0, 30, 8, step=5, key="ramp_m4_bonus")
    with col3:
        st.write("**Months 7+**")
        ramp_m7_bonus = st.slider("Ramp Cost %", 0, 20, 0, step=5, key="ramp_m7_bonus")

    st.markdown("---")

    st.subheader("🎁 Incentives & Adjustments")
    col1, col2, col3, col4 = st.columns(4)
    with col1: retention_bonus = st.slider("Retention Bonus %", 0, 30, 5, step=2, key="retention_bonus")
    with col2: performance_bonus = st.slider("Performance Bonus %", 0, 25, 3, step=2, key="performance_bonus")
    with col3: skill_premium = st.slider("Skill Premium %", 0, 50, 10, step=5, key="skill_premium")
    with col4: discount_markup = st.slider("Discount/Markup %", -50, 100, 0, step=5, key="discount_markup")

    st.markdown("---")

    wfo_factor = WFO_OPTIONS[wfo_model]
    complexity_mult = COMPLEXITY_LEVELS[complexity]['multiplier']
    shrinkage_rate = SHRINKAGE_FACTORS[shrinkage]
    attrition_rate = ATTRITION_RATES[attrition]
    currency_factor = CURRENCIES[currency]
    currency_symbol = CURRENCY_SYMBOLS[currency]

    total_cost_pct = salary_pct + benefits_pct + overhead_pct + training_pct
    monthly_cost = base_salary * (total_cost_pct / salary_pct) if salary_pct > 0 else 0
    annual_cost_base = monthly_cost * 12
    annual_cost_adjusted = annual_cost_base * complexity_mult * (1 + (1 - wfo_factor) * 0.15)

    onboarding_cost = (base_salary * 12) * (onboarding_pct / 100)
    qa_cost = annual_cost_adjusted * (qa_cost_pct / 100)
    compliance_cost = annual_cost_adjusted * (compliance_pct / 100)
    tools_cost = annual_cost_adjusted * (tools_pct / 100)

    total_annual_cost_fte = annual_cost_adjusted + onboarding_cost + qa_cost + compliance_cost + tools_cost
    shrinkage_cost = total_annual_cost_fte * shrinkage_rate
    attrition_cost_fte = total_annual_cost_fte * attrition_rate
    total_annual_cost_per_fte = total_annual_cost_fte + shrinkage_cost + attrition_cost_fte

    total_team_cost = total_annual_cost_per_fte * ftes

    ramp_cost = (base_salary * 12 * ramp_m1_bonus / 100) * ftes * 0.25 + \
                (base_salary * 12 * ramp_m4_bonus / 100) * ftes * 0.25 + \
                (base_salary * 12 * ramp_m7_bonus / 100) * ftes * 0.50

    retention_cost = (base_salary * 12 * retention_bonus / 100) * ftes
    performance_cost = (base_salary * 12 * performance_bonus / 100) * ftes
    skill_cost = (base_salary * 12 * skill_premium / 100) * ftes

    total_y1_cost = total_team_cost + ramp_cost + retention_cost + performance_cost + skill_cost
    final_y1_cost = total_y1_cost * (1 + discount_markup / 100)

    margin_decimal = margin_target / 100
    acv = final_y1_cost / (1 - margin_decimal) if margin_decimal < 1 else 0
    tcv = acv * years
    margin_dollars = acv - final_y1_cost
    margin_pct_calc = (margin_dollars / acv * 100) if acv > 0 else 0

    geo_to_usd = 1.0 / CURRENCIES.get(geo_currency, 1.0)
    conv = geo_to_usd * currency_factor

    st.subheader("💰 KEY METRICS")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Cost/FTE/Year", f"{currency_symbol}{total_annual_cost_per_fte*conv:,.0f}")
    with col2: st.metric("Team Cost/Year", f"{currency_symbol}{total_team_cost*conv:,.0f}")
    with col3: st.metric("ACV", f"{currency_symbol}{acv*conv:,.0f}")
    with col4: st.metric("TCV", f"{currency_symbol}{tcv*conv:,.0f}")
    with col5: st.metric("Margin", f"{margin_pct_calc:.1f}%")

    st.markdown("---")
    st.info(f"📌 **{skill_type} | {complexity} | {GEOGRAPHIES[geography]['name']}** → Base: {geo_symbol}{base_salary:,}/mo")

    st.subheader("📊 Cost Breakdown (per FTE)")
    cost_data = pd.DataFrame({
        "Component": ["Salary", "Benefits", "Overhead", "Training", "QA/Audit", "Compliance",
                       "Tools/Tech", "Onboarding", "Shrinkage", "Attrition", "**TOTAL**"],
        f"Local ({geo_symbol})": [
            f"{geo_symbol}{annual_cost_adjusted*salary_pct/total_cost_pct:,.0f}",
            f"{geo_symbol}{annual_cost_adjusted*benefits_pct/total_cost_pct:,.0f}",
            f"{geo_symbol}{annual_cost_adjusted*overhead_pct/total_cost_pct:,.0f}",
            f"{geo_symbol}{annual_cost_adjusted*training_pct/total_cost_pct:,.0f}",
            f"{geo_symbol}{qa_cost:,.0f}", f"{geo_symbol}{compliance_cost:,.0f}",
            f"{geo_symbol}{tools_cost:,.0f}", f"{geo_symbol}{onboarding_cost:,.0f}",
            f"{geo_symbol}{shrinkage_cost:,.0f}", f"{geo_symbol}{attrition_cost_fte:,.0f}",
            f"{geo_symbol}{total_annual_cost_per_fte:,.0f}"
        ],
        f"Display ({currency_symbol})": [
            f"{currency_symbol}{annual_cost_adjusted*salary_pct/total_cost_pct*conv:,.0f}",
            f"{currency_symbol}{annual_cost_adjusted*benefits_pct/total_cost_pct*conv:,.0f}",
            f"{currency_symbol}{annual_cost_adjusted*overhead_pct/total_cost_pct*conv:,.0f}",
            f"{currency_symbol}{annual_cost_adjusted*training_pct/total_cost_pct*conv:,.0f}",
            f"{currency_symbol}{qa_cost*conv:,.0f}", f"{currency_symbol}{compliance_cost*conv:,.0f}",
            f"{currency_symbol}{tools_cost*conv:,.0f}", f"{currency_symbol}{onboarding_cost*conv:,.0f}",
            f"{currency_symbol}{shrinkage_cost*conv:,.0f}", f"{currency_symbol}{attrition_cost_fte*conv:,.0f}",
            f"{currency_symbol}{total_annual_cost_per_fte*conv:,.0f}"
        ]
    })
    st.dataframe(cost_data, use_container_width=True, hide_index=True)

    st.markdown("---")

    scenario_name = st.text_input("Scenario Name", value=f"{skill_type}_{complexity}_{geography}_{datetime.now().strftime('%Y%m%d')}", key="scenario_name")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Scenario"):
            st.session_state.scenarios[scenario_name] = {
                "skill_type": skill_type, "complexity": complexity, "geography": geography,
                "base_salary": base_salary, "ftes": ftes, "wfo_model": wfo_model,
                "years": years, "currency": currency, "shrinkage": shrinkage, "attrition": attrition,
                "margin_target": margin_target, "acv": acv*conv, "tcv": tcv*conv,
                "margin_pct": margin_pct_calc, "annual_cost": total_team_cost*conv,
                "timestamp": datetime.now().isoformat()
            }
            st.success(f"✅ Saved: {scenario_name}")
    with col2:
        if st.button("📥 Save as Template"):
            st.session_state.templates[scenario_name] = {
                "skill_type": skill_type, "complexity": complexity, "geography": geography,
                "wfo_model": wfo_model, "currency": currency, "margin_target": margin_target
            }
            st.success(f"✅ Template Saved")
    with col3:
        st.metric("Scenarios", len(st.session_state.scenarios))
    # ==================== EXCEL DOWNLOAD ====================
    st.markdown("---")
    st.subheader("📥 Download Pricing Sheet (Excel)")

    def generate_excel():
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            # Sheet 1: Input Parameters
            inputs = pd.DataFrame({
                "Parameter": [
                    "Skill Type", "Complexity Level", "Geography", "Geography Name",
                    "Base Monthly Salary", "Salary Currency", "Number of FTEs",
                    "WFO/WFH Model", "Contract Duration (Years)", "Display Currency",
                    "Shrinkage Rate", "Attrition Rate", "Target Margin %",
                    "", "--- Cost Components (%) ---", "",
                    "Salary %", "Benefits %", "Overhead %", "Training %",
                    "Onboarding %", "QA/Audit %", "Compliance %", "Tools/Tech %",
                    "", "--- Ramp-Up Schedule ---", "",
                    "Months 1-3 Ramp Cost %", "Months 4-6 Ramp Cost %", "Months 7+ Ramp Cost %",
                    "", "--- Incentives & Adjustments ---", "",
                    "Retention Bonus %", "Performance Bonus %", "Skill Premium %", "Discount/Markup %"
                ],
                "Value": [
                    skill_type, complexity, geography, GEOGRAPHIES[geography]['name'],
                    base_salary, geo_currency, ftes,
                    wfo_model, years, currency,
                    shrinkage, attrition, margin_target,
                    "", "", "",
                    salary_pct, benefits_pct, overhead_pct, training_pct,
                    onboarding_pct, qa_cost_pct, compliance_pct, tools_pct,
                    "", "", "",
                    ramp_m1_bonus, ramp_m4_bonus, ramp_m7_bonus,
                    "", "", "",
                    retention_bonus, performance_bonus, skill_premium, discount_markup
                ]
            })
            inputs.to_excel(writer, sheet_name="Input Parameters", index=False)

            # Sheet 2: Key Metrics
            metrics = pd.DataFrame({
                "Metric": [
                    "Annual Cost per FTE (Local)", "Annual Cost per FTE (Display)",
                    "Total Team Cost/Year (Local)", "Total Team Cost/Year (Display)",
                    "ACV (Display Currency)", "TCV (Display Currency)",
                    "Margin %", "Margin Amount (Display)",
                    "", "--- Year 1 Costs ---", "",
                    "Total Team Cost", "Ramp-Up Cost", "Retention Cost",
                    "Performance Cost", "Skill Premium Cost",
                    "Total Y1 Cost (before markup)", "Final Y1 Cost (after markup)",
                ],
                "Value": [
                    f"{geo_symbol}{total_annual_cost_per_fte:,.0f}",
                    f"{currency_symbol}{total_annual_cost_per_fte*conv:,.0f}",
                    f"{geo_symbol}{total_team_cost:,.0f}",
                    f"{currency_symbol}{total_team_cost*conv:,.0f}",
                    f"{currency_symbol}{acv*conv:,.0f}",
                    f"{currency_symbol}{tcv*conv:,.0f}",
                    f"{margin_pct_calc:.1f}%",
                    f"{currency_symbol}{margin_dollars*conv:,.0f}",
                    "", "", "",
                    f"{geo_symbol}{total_team_cost:,.0f}",
                    f"{geo_symbol}{ramp_cost:,.0f}",
                    f"{geo_symbol}{retention_cost:,.0f}",
                    f"{geo_symbol}{performance_cost:,.0f}",
                    f"{geo_symbol}{skill_cost:,.0f}",
                    f"{geo_symbol}{total_y1_cost:,.0f}",
                    f"{geo_symbol}{final_y1_cost:,.0f}",
                ],
                "Numeric": [
                    total_annual_cost_per_fte, total_annual_cost_per_fte*conv,
                    total_team_cost, total_team_cost*conv,
                    acv*conv, tcv*conv,
                    margin_pct_calc, margin_dollars*conv,
                    "", "", "",
                    total_team_cost, ramp_cost, retention_cost,
                    performance_cost, skill_cost,
                    total_y1_cost, final_y1_cost,
                ]
            })
            metrics.to_excel(writer, sheet_name="Key Metrics", index=False)

            # Sheet 3: Cost Breakdown per FTE
            breakdown = pd.DataFrame({
                "Component": ["Salary", "Benefits", "Overhead", "Training",
                              "QA/Audit", "Compliance", "Tools/Tech", "Onboarding",
                              "Shrinkage", "Attrition", "TOTAL per FTE"],
                f"Annual Local ({geo_symbol})": [
                    round(annual_cost_adjusted*salary_pct/total_cost_pct),
                    round(annual_cost_adjusted*benefits_pct/total_cost_pct),
                    round(annual_cost_adjusted*overhead_pct/total_cost_pct),
                    round(annual_cost_adjusted*training_pct/total_cost_pct),
                    round(qa_cost), round(compliance_cost),
                    round(tools_cost), round(onboarding_cost),
                    round(shrinkage_cost), round(attrition_cost_fte),
                    round(total_annual_cost_per_fte)
                ],
                f"Annual Display ({currency_symbol})": [
                    round(annual_cost_adjusted*salary_pct/total_cost_pct*conv),
                    round(annual_cost_adjusted*benefits_pct/total_cost_pct*conv),
                    round(annual_cost_adjusted*overhead_pct/total_cost_pct*conv),
                    round(annual_cost_adjusted*training_pct/total_cost_pct*conv),
                    round(qa_cost*conv), round(compliance_cost*conv),
                    round(tools_cost*conv), round(onboarding_cost*conv),
                    round(shrinkage_cost*conv), round(attrition_cost_fte*conv),
                    round(total_annual_cost_per_fte*conv)
                ],
                "% of Total": [
                    f"{salary_pct/total_cost_pct*100:.1f}%",
                    f"{benefits_pct/total_cost_pct*100:.1f}%",
                    f"{overhead_pct/total_cost_pct*100:.1f}%",
                    f"{training_pct/total_cost_pct*100:.1f}%",
                    f"{qa_cost_pct:.1f}%", f"{compliance_pct:.1f}%",
                    f"{tools_pct:.1f}%", f"{onboarding_pct:.1f}%",
                    f"{shrinkage_rate*100:.1f}%", f"{attrition_rate*100:.1f}%",
                    "100%"
                ]
            })
            breakdown.to_excel(writer, sheet_name="Cost Breakdown", index=False)

            # Sheet 4: Multi-Year Projection
            yearly_rows = []
            for yr in range(1, years + 1):
                if yr == 1:
                    yr_cost_total = final_y1_cost
                else:
                    yr_cost_total = total_team_cost * (1 + discount_markup / 100)
                yr_acv = yr_cost_total / (1 - margin_decimal) if margin_decimal < 1 else 0
                yr_margin = yr_acv - yr_cost_total
                yearly_rows.append({
                    "Year": yr,
                    f"Cost ({geo_symbol})": round(yr_cost_total),
                    f"Revenue/ACV ({geo_symbol})": round(yr_acv),
                    f"Margin ({geo_symbol})": round(yr_margin),
                    "Margin %": f"{(yr_margin/yr_acv*100) if yr_acv > 0 else 0:.1f}%",
                    f"Cost ({currency_symbol})": round(yr_cost_total * conv),
                    f"Revenue ({currency_symbol})": round(yr_acv * conv),
                })
            yearly_df = pd.DataFrame(yearly_rows)
            yearly_df.to_excel(writer, sheet_name="Multi-Year Projection", index=False)

            # Sheet 5: Salary Reference for selected geography
            if geography in GEO_SALARIES:
                sal_rows = []
                for sk in ["Voice", "Non-voice", "Backoffice"]:
                    for lv in ["L1", "L2", "L3", "L4", "L5", "L6"]:
                        master_val = None
                        if master_defaults:
                            mkey = f"{sk}_{lv}_{geography}"
                            if mkey in master_defaults:
                                master_val = master_defaults[mkey]
                        builtin_val = GEO_SALARIES.get(geography, {}).get(sk, {}).get(lv, "N/A")
                        sal_rows.append({
                            "Skill Type": sk, "Level": lv, "Geography": geography,
                            f"Built-in Salary ({geo_symbol}/mo)": builtin_val,
                            f"Master File ({geo_symbol}/mo)": master_val if master_val else "N/A",
                            "Source Used": "Master File" if master_val else "Built-in"
                        })
                sal_df = pd.DataFrame(sal_rows)
                sal_df.to_excel(writer, sheet_name="Salary Reference", index=False)

            # Auto-fit column widths
            for sheet_name in writer.sheets:
                ws = writer.sheets[sheet_name]
                for col_cells in ws.columns:
                    max_len = max(len(str(cell.value or "")) for cell in col_cells)
                    col_letter = col_cells[0].column_letter
                    ws.column_dimensions[col_letter].width = min(max_len + 3, 40)

        output.seek(0)
        return output

    file_name = f"Pricing_{skill_type}_{complexity}_{geography}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    excel_data = generate_excel()
    st.download_button(
        label="📥 Download Full Pricing Sheet (Excel)",
        data=excel_data,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.caption(f"5 sheets: Input Parameters | Key Metrics | Cost Breakdown | {years}-Year Projection | Salary Reference")
with tab2:
    st.header("📚 Pricing Templates")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Saved Templates")
        if st.session_state.templates:
            for tn, t in st.session_state.templates.items():
                st.write(f"**{tn}** — {t['skill_type']} | {t['complexity']} | {t['geography']}")
        else:
            st.info("No templates saved yet")
    with col2:
        st.subheader("Quick Start")
        for t in ["Voice L1 (India)", "Backoffice L2 (Phil)", "Non-voice L3 (US)"]:
            st.write(f"**{t}**")

with tab3:
    st.header("🔄 Scenario Comparison")
    if not st.session_state.scenarios:
        st.warning("⚠️ Save scenarios first!")
    else:
        sel = st.multiselect("Compare", list(st.session_state.scenarios.keys()), max_selections=6)
        if sel:
            rows = [{"Scenario": n, "Skill": s["skill_type"], "Level": s["complexity"],
                     "Geo": s["geography"], "FTEs": s["ftes"], "ACV": f"${s['acv']:,.0f}",
                     "TCV": f"${s['tcv']:,.0f}", "Margin": f"{s['margin_pct']:.1f}%"}
                    for n, s in st.session_state.scenarios.items() if n in sel]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tab4:
    st.header("⚠️ Risk Assessment")
    if not st.session_state.scenarios:
        st.warning("⚠️ Create scenarios first!")
    else:
        rsc = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="rsc")
        scores = []
        for cat_name, factors in RISK_CATEGORIES.items():
            with st.expander(cat_name, expanded=(cat_name=="Operational Risk")):
                c1,c2 = st.columns(2)
                cat_scores = []
                for i, (fname, fvals) in enumerate(factors.items()):
                    col = c1 if i % 2 == 0 else c2
                    with col:
                        val = st.selectbox(fname, ["Low","Medium","High","Critical"], key=f"r_{cat_name}_{fname}")
                        cat_scores.append(fvals[val])
                avg = np.mean(cat_scores)
                scores.append(avg)
                st.metric(f"{cat_name} Score", f"{avg:.2%}")
        st.markdown("---")
        overall = np.mean(scores)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("OVERALL RISK", f"{overall:.2%}")
        with c2:
            if overall < 0.05: st.success("🟢 LOW")
            elif overall < 0.10: st.info("🟡 MODERATE")
            else: st.error("🔴 HIGH")
        with c3:
            s = st.session_state.scenarios[rsc]
            st.metric("Risk-Adj Margin", f"{s['margin_pct']-overall*100:.1f}%")

with tab5:
    st.header("🎯 Decision Dashboard")
    if not st.session_state.scenarios:
        st.warning("⚠️ Create scenarios first!")
    else:
        dsc = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="dsc")
        s = st.session_state.scenarios[dsc]
        c1,c2 = st.columns(2)
        with c1:
            ms=st.slider("Margin",1,10,7,key="d1"); gs=st.slider("Growth",1,10,6,key="d2")
            cq=st.slider("Client Quality",1,10,7,key="d3"); ss2=st.slider("Stability",1,10,6,key="d4")
        with c2:
            rs2=st.slider("Risk(1=Hi,10=Lo)",1,10,5,key="d5"); ex=st.slider("Execution",1,10,7,key="d6")
            sc2=st.slider("Scalability",1,10,6,key="d7"); sf=st.slider("Strategic",1,10,7,key="d8")
        ws=ms*.20+gs*.15+cq*.15+ss2*.10+rs2*.15+ex*.10+sc2*.10+sf*.05
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Score",f"{ws:.1f}/10")
        with c2:
            if ws>=8: st.success("🟢 STRONG BUY")
            elif ws>=6.5: st.info("🟡 BUY")
            else: st.error("🔴 PASS")
        with c3: st.metric("Margin",f"{s['margin_pct']:.1f}%")

with tab6:
    st.header("💹 ROI Analysis")
    if not st.session_state.scenarios:
        st.warning("⚠️ Create scenarios first!")
    else:
        rsc2 = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="rsc2")
        s = st.session_state.scenarios[rsc2]
        c1,c2,c3 = st.columns(3)
        with c1: inv=st.number_input("Investment",value=100000,step=10000,key="inv")
        with c2: dr=st.slider("Discount %",0,20,10,key="dr")
        with c3: ap=st.slider("Period (Yrs)",1,10,5,key="ap")
        p=s['acv']-s['annual_cost']
        be=(inv/p*12) if p>0 else float('inf')
        roi=((p*ap-inv)/inv*100) if inv>0 else 0
        npv=-inv+sum(p/((1+dr/100)**y) for y in range(1,ap+1))
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("Profit/Yr",f"${p:,.0f}")
        with c2: st.metric("Break-Even",f"{be:.1f}mo" if be!=float('inf') else "N/A")
        with c3: st.metric("ROI",f"{roi:.1f}%")
        with c4: st.metric("NPV",f"${npv:,.0f}")

with tab7:
    st.header("📈 Advanced Analysis")
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Sensitivity")
        if st.session_state.scenarios:
            ssc=st.selectbox("Scenario",list(st.session_state.scenarios.keys()),key="ssc")
            s=st.session_state.scenarios[ssc]
            rows=[{"FTEs":int(s['ftes']*m),"Change":f"{(m-1)*100:+.0f}%","ACV":f"${s['acv']*m:,.0f}"}
                  for m in [0.8,0.9,1.0,1.1,1.2]]
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    with c2:
        st.subheader("Portfolio")
        if len(st.session_state.scenarios)>1:
            st.metric("Total ACV",f"${sum(s['acv'] for s in st.session_state.scenarios.values()):,.0f}")
            st.metric("Avg Margin",f"{np.mean([s['margin_pct'] for s in st.session_state.scenarios.values()]):.1f}%")

with tab8:
    st.header("⚙️ Settings")
    c1,c2=st.columns(2)
    with c1:
        if st.button("📥 Export Scenarios"):
            st.download_button("Download",json.dumps(st.session_state.scenarios,indent=2,default=str),"scenarios.json")
    with c2:
        if st.button("📥 Export Templates"):
            st.download_button("Download",json.dumps(st.session_state.templates,indent=2,default=str),"templates.json")
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Scenarios",len(st.session_state.scenarios))
    with c2: st.metric("Templates",len(st.session_state.templates))
    with c3: st.metric("Master File","✅" if master_defaults else "📋 Built-in")
    if master_defaults:
        with st.expander("🔍 Loaded Salary Entries"):
            for k,v in sorted(master_defaults.items()):
                st.caption(f"{k}: {v:,.0f}")

st.markdown("---")
st.success("✅ **Dynamic Pricing Platform — Linked Defaults**")
st.caption("🎯 Salary auto-updates with Skill × Level × Geography | Editable FTE | 9 Geos | 6 Levels")
