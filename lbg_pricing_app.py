import streamlit as st
import pandas as pd
import json
import openpyxl
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Enterprise Pricing Platform", layout="wide")

st.title("🎯 Dynamic Pricing Platform - Template Edition")
st.markdown("**Master Template | Any Project Type | Maximum Flexibility**")
st.markdown("---")

# ==================== LOAD MASTER FILE ====================

MASTER_FILE = "Pricing_Master_Feb_26_v10.xlsm"

@st.cache_data
def load_master_data():
    """Load all data from master pricing file"""
    try:
        wb = openpyxl.load_workbook(MASTER_FILE, data_only=False)
        
        # Extract geography from salary sheets
        geographies = {}
        salary_sheets = ['US Salary', 'UK Salary', 'SA Salary', 'Mexico Salary', 'Aus Salary', 'Salary PHP', 'IND Salary', 'ROM Salary', 'T&T Salary']
        
        for sheet_name in salary_sheets:
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                geo_name = sheet_name.replace(' Salary', '')
                geographies[geo_name] = {'sheet': sheet_name, 'data': {}}
        
        # Extract threshold guidance (SLA & margins)
        thresholds = {}
        if 'Threshold Guidance' in wb.sheetnames:
            ws = wb['Threshold Guidance']
            for row in ws.iter_rows(min_row=3, max_row=15, values_only=True):
                if row[1]:  # Skill type
                    key = f"{row[1]}_{row[2]}"  # Skill_Complexity
                    thresholds[key] = row[3:] if row[3:] else [0.30]  # Threshold values
        
        # Extract rate chart
        rate_chart = {}
        if 'Rate Chart' in wb.sheetnames:
            ws = wb['Rate Chart']
            for row in ws.iter_rows(min_row=3, max_row=15, values_only=True):
                if row[0]:
                    key = f"{row[0]}_{row[1]}"  # Skill_Complexity
                    rate_chart[key] = {
                        'location': row[3],
                        'wfo': row[4],
                        'salary': row[5],
                        'ftes': row[6],
                        'rate_per_hr': row[7],
                        'training_rate': row[8],
                        'revenue_3yr': row[9]
                    }
        
        return {
            'geographies': list(geographies.keys()),
            'thresholds': thresholds,
            'rate_chart': rate_chart,
            'workbook': wb
        }
    except Exception as e:
        st.error(f"Error loading master file: {e}")
        return None

master_data = load_master_data()

if master_data is None:
    st.error("Cannot load master pricing file. Please ensure 'Pricing_Master_Feb_26_v10.xlsm' is in the same directory.")
    st.stop()

# ==================== DATA DEFINITIONS ====================

SKILL_TYPES = {
    "Voice": {"description": "Voice/Phone Support", "color": "🎧"},
    "Non-Voice": {"description": "Chat/Email/Digital", "color": "💬"},
    "Backoffice": {"description": "Back Office/Processing", "color": "📋"}
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
    "MXN": 17.0
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "INR": "₹",
    "PHP": "₱",
    "AUD": "A$",
    "MXN": "Mex$"
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Calculator",
    "📚 Templates",
    "🔄 Comparison",
    "⚠️ Risk Assessment",
    "🎯 Decision Dashboard",
    "💹 ROI Analysis",
    "💎 Pricing Optimization",
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
        geography = st.selectbox("🌍 Geography", master_data['geographies'], key="geography")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        base_salary = st.number_input("Base Monthly Salary (Local Currency)", value=25000, step=1000, key="salary")
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
    
    st.subheader("💰 Cost Components")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        salary_pct = st.slider("Salary %", 50, 75, 60, step=1, key="salary_pct")
    with col2:
        benefits_pct = st.slider("Benefits %", 5, 20, 12, step=1, key="benefits_pct")
    with col3:
        overhead_pct = st.slider("Overhead %", 5, 20, 15, step=1, key="overhead_pct")
    with col4:
        training_pct = st.slider("Training %", 3, 15, 5, step=1, key="training_pct")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        onboarding_pct = st.slider("Onboarding %", 0, 30, 10, step=2, key="onboarding_pct")
    with col2:
        qa_cost_pct = st.slider("QA/Audit %", 0, 15, 5, step=1, key="qa_cost_pct")
    with col3:
        compliance_pct = st.slider("Compliance %", 0, 10, 3, step=1, key="compliance_pct")
    with col4:
        tools_pct = st.slider("Tools/Tech %", 2, 10, 5, step=1, key="tools_pct")
    
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
    annual_cost_adjusted = annual_cost_base * complexity_mult * (1 + (1 - wfo_factor))
    
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
