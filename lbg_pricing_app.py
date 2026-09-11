import streamlit as st
import pandas as pd
import json
from datetime import datetime
import numpy as np
import os

st.set_page_config(page_title="Firstsource | Enterprise Pricing Platform", layout="wide", page_icon="🎯")

# ==================== FIRSTSOURCE BRAND CSS ====================
st.markdown("""
<style>
    /* === Firstsource Brand Colors === */
    /* Orange: #DF6014 | Dark Blue: #1E2247 | Mid Blue: #113190 | Bright Blue: #2844C4 | Light Blue: #6CB1DB | Gray: #ECF1F5 */

    /* Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', 'Franklin Gothic Medium', Arial, sans-serif;
    }

    /* Header bar */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #1E2247 0%, #113190 60%, #2844C4 100%);
    }

    /* Main title styling */
    h1 {
        color: #1E2247 !important;
        font-weight: 700 !important;
    }

    /* Subheaders */
    h2, h3 {
        color: #1E2247 !important;
        border-bottom: 2px solid #6CB1DB;
        padding-bottom: 8px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #ECF1F5;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #1E2247;
        font-weight: 500;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E2247 !important;
        color: white !important;
        border-radius: 6px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E2247 0%, #113190 100%);
        border-radius: 10px;
        padding: 16px 20px;
        color: white;
        box-shadow: 0 2px 8px rgba(30, 34, 71, 0.15);
    }
    [data-testid="stMetric"] label {
        color: #6CB1DB !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #DF6014 0%, #e87a35 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c45410 0%, #DF6014 100%);
        box-shadow: 0 4px 12px rgba(223, 96, 20, 0.3);
        color: white;
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1E2247 0%, #113190 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 28px;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #113190 0%, #2844C4 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(17, 49, 144, 0.3);
    }

    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #2E7D32;
    }
    .stInfo {
        background-color: #ECF1F5;
        border-left: 4px solid #113190;
    }

    /* Selectbox and inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        color: #1E2247 !important;
        font-weight: 500 !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #6CB1DB;
        border-radius: 8px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #ECF1F5;
        border-radius: 8px;
        color: #1E2247;
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E2247 0%, #113190 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    /* Divider line */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #DF6014, #6CB1DB, #1E2247);
        margin: 20px 0;
    }

    /* Footer styling */
    .fs-footer {
        background: linear-gradient(135deg, #1E2247 0%, #113190 60%, #2844C4 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
    .fs-footer a { color: #6CB1DB; }

    /* Logo header bar */
    .fs-header {
        background: linear-gradient(135deg, #1E2247 0%, #113190 60%, #2844C4 100%);
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .fs-header h1 {
        color: white !important;
        margin: 0;
        font-size: 1.8rem;
        border: none;
    }
    .fs-header p {
        color: #6CB1DB;
        margin: 4px 0 0 0;
        font-size: 0.9rem;
    }

    /* Orange accent bar */
    .fs-accent-bar {
        height: 4px;
        background: linear-gradient(90deg, #DF6014, #e87a35, #DF6014);
        border-radius: 2px;
        margin: 10px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FIRSTSOURCE HEADER ====================

# Try to show logo
logo_path = "firstsource_logo.png"
if os.path.exists(logo_path):
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(logo_path, width=200)
    with col_title:
        st.markdown("""
        <div>
            <h1 style="margin:0; color:#1E2247;">Enterprise Pricing Platform</h1>
            <p style="color:#113190; font-size:1rem; margin:4px 0;">Dynamic Pricing | Auto-Populated Defaults | We make it happen!</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="fs-header">
        <div>
            <h1>🎯 Firstsource | Enterprise Pricing Platform</h1>
            <p>Dynamic Pricing | Auto-Populated Defaults | We make it happen!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="fs-accent-bar"></div>', unsafe_allow_html=True)

# ==================== LOAD MASTER FILE ====================

@st.cache_data
def load_master_defaults():
    try:
        import openpyxl
        possible_names = [
            "Pricing_Master_Feb_26_v10.xlsm", "Pricing_Master_Feb'26_v10.xlsm",
            "Pricing Master_Feb'26_v10.xlsm", "Pricing Master_Feb_26_v10.xlsm",
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
                        for level in ["L1","L2","L3","L4","L5","L6"]:
                            if level in cell1 or level in cell0:
                                complexity_match = level
                                break
                        if skill_match and complexity_match:
                            for col_idx in range(2, min(len(row), 15)):
                                if row[col_idx]:
                                    try:
                                        val = float(row[col_idx])
                                        if val > 100:
                                            salary_defaults[f"{skill_match}_{complexity_match}_{geo_code}"] = val
                                            break
                                    except (ValueError, TypeError):
                                        pass
        return salary_defaults if salary_defaults else None
    except Exception:
        return None

master_defaults = load_master_defaults()

# ==================== DATA ====================

GEO_SALARIES = {
    "IND": {"Voice": {"L1":18000,"L2":22000,"L3":28000,"L4":35000,"L5":42000,"L6":50000},
            "Non-voice": {"L1":16000,"L2":20000,"L3":26000,"L4":32000,"L5":38000,"L6":45000},
            "Backoffice": {"L1":15000,"L2":19000,"L3":24000,"L4":30000,"L5":36000,"L6":42000}},
    "PHP": {"Voice": {"L1":20000,"L2":25000,"L3":32000,"L4":40000,"L5":48000,"L6":58000},
            "Non-voice": {"L1":18000,"L2":23000,"L3":30000,"L4":37000,"L5":44000,"L6":52000},
            "Backoffice": {"L1":17000,"L2":22000,"L3":28000,"L4":35000,"L5":42000,"L6":50000}},
    "UK":  {"Voice": {"L1":2200,"L2":2600,"L3":3200,"L4":3800,"L5":4500,"L6":5200},
            "Non-voice": {"L1":2000,"L2":2400,"L3":3000,"L4":3600,"L5":4200,"L6":4800},
            "Backoffice": {"L1":1900,"L2":2300,"L3":2800,"L4":3400,"L5":4000,"L6":4600}},
    "US":  {"Voice": {"L1":3200,"L2":3800,"L3":4500,"L4":5500,"L5":6500,"L6":7500},
            "Non-voice": {"L1":3000,"L2":3600,"L3":4200,"L4":5200,"L5":6000,"L6":7000},
            "Backoffice": {"L1":2800,"L2":3400,"L3":4000,"L4":5000,"L5":5800,"L6":6800}},
    "MEX": {"Voice": {"L1":14000,"L2":17000,"L3":22000,"L4":28000,"L5":34000,"L6":40000},
            "Non-voice": {"L1":12000,"L2":15000,"L3":20000,"L4":25000,"L5":30000,"L6":36000},
            "Backoffice": {"L1":11000,"L2":14000,"L3":18000,"L4":23000,"L5":28000,"L6":34000}},
    "AUS": {"Voice": {"L1":4200,"L2":5000,"L3":6000,"L4":7200,"L5":8500,"L6":10000},
            "Non-voice": {"L1":3800,"L2":4600,"L3":5500,"L4":6800,"L5":8000,"L6":9200},
            "Backoffice": {"L1":3600,"L2":4400,"L3":5200,"L4":6500,"L5":7600,"L6":8800}},
    "SA":  {"Voice": {"L1":12000,"L2":15000,"L3":19000,"L4":24000,"L5":29000,"L6":35000},
            "Non-voice": {"L1":10000,"L2":13000,"L3":17000,"L4":22000,"L5":27000,"L6":32000},
            "Backoffice": {"L1":9000,"L2":12000,"L3":16000,"L4":20000,"L5":25000,"L6":30000}},
    "ROM": {"Voice": {"L1":3500,"L2":4200,"L3":5200,"L4":6500,"L5":7800,"L6":9000},
            "Non-voice": {"L1":3200,"L2":3900,"L3":4800,"L4":6000,"L5":7200,"L6":8400},
            "Backoffice": {"L1":3000,"L2":3700,"L3":4500,"L4":5700,"L5":6800,"L6":8000}},
    "TT":  {"Voice": {"L1":8000,"L2":10000,"L3":13000,"L4":16000,"L5":19000,"L6":23000},
            "Non-voice": {"L1":7000,"L2":9000,"L3":12000,"L4":15000,"L5":18000,"L6":21000},
            "Backoffice": {"L1":6500,"L2":8500,"L3":11000,"L4":14000,"L5":17000,"L6":20000}},
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

SKILL_TYPES = {"Voice": "Voice/Phone Support", "Non-voice": "Chat/Email/Digital", "Backoffice": "Back Office/Processing"}
COMPLEXITY_LEVELS = {"L1": {"desc": "Basic", "mult": 1.0}, "L2": {"desc": "Intermediate", "mult": 1.15},
                     "L3": {"desc": "Advanced", "mult": 1.35}, "L4": {"desc": "Expert", "mult": 1.60},
                     "L5": {"desc": "Specialized", "mult": 1.85}, "L6": {"desc": "Premium", "mult": 2.10}}

WFO_OPTIONS = {"100% WFO": 1.00, "80% WFO": 0.80, "50% WFO": 0.50, "20% WFO": 0.20, "100% WFH": 0.00}
SHRINKAGE = {"Low (5%)": 0.05, "Normal (10%)": 0.10, "High (15%)": 0.15, "Very High (20%)": 0.20}
ATTRITION = {"Low (5%)": 0.05, "Medium (10%)": 0.10, "High (15%)": 0.15, "Critical (25%)": 0.25}
CURRENCIES = {"USD": 1.0, "GBP": 1.27, "EUR": 0.92, "INR": 82.5, "PHP": 55.0, "AUD": 1.50, "ZAR": 18.0, "MXN": 17.0, "TTD": 6.75}
CUR_SYM = {"USD": "$", "GBP": "£", "EUR": "€", "INR": "₹", "PHP": "₱", "AUD": "A$", "ZAR": "R", "MXN": "Mex$", "TTD": "TT$"}

RISK_CATEGORIES = {
    "Operational Risk": {"Attrition": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.20},
        "Quality": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15},
        "Compliance": {"Low":0.03,"Medium":0.07,"High":0.12,"Critical":0.18},
        "Technology": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15}},
    "Financial Risk": {"Currency": {"Low":0.01,"Medium":0.03,"High":0.06,"Critical":0.10},
        "Volume": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15},
        "Inflation": {"Low":0.02,"Medium":0.04,"High":0.07,"Critical":0.12},
        "Margin": {"Low":0.03,"Medium":0.06,"High":0.10,"Critical":0.15}},
    "Client Risk": {"Concentration": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15},
        "Renewal": {"Low":0.03,"Medium":0.07,"High":0.12,"Critical":0.20},
        "Scope Creep": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15},
        "SLA Risk": {"Low":0.02,"Medium":0.04,"High":0.08,"Critical":0.12}},
    "Market Risk": {"Volatility": {"Low":0.02,"Medium":0.04,"High":0.08,"Critical":0.12},
        "Competition": {"Low":0.03,"Medium":0.06,"High":0.10,"Critical":0.15},
        "Regulatory": {"Low":0.02,"Medium":0.05,"High":0.10,"Critical":0.15},
        "Geopolitical": {"Low":0.01,"Medium":0.03,"High":0.06,"Critical":0.12}}
}

def get_salary(sk, lv, geo):
    if master_defaults:
        key = f"{sk}_{lv}_{geo}"
        if key in master_defaults:
            return int(master_defaults[key])
    if geo in GEO_SALARIES and sk in GEO_SALARIES[geo] and lv in GEO_SALARIES[geo][sk]:
        return GEO_SALARIES[geo][sk][lv]
    return 15000

# ==================== SESSION STATE ====================
for key, default in [('scenarios', {}), ('templates', {}), ('prev_selection', ''), ('dynamic_salary', 18000)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Calculator", "📚 Templates", "🔄 Comparison", "⚠️ Risk Assessment",
    "🎯 Decision Dashboard", "💹 ROI Analysis", "📈 Advanced Analysis", "⚙️ Settings"
])

# ==================== TAB 1: CALCULATOR ====================
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
        st.caption(SKILL_TYPES[skill_type])
    with col2:
        complexity = st.selectbox("📊 Complexity Level", list(COMPLEXITY_LEVELS.keys()), key="complexity",
                                   format_func=lambda x: f"{x} — {COMPLEXITY_LEVELS[x]['desc']}")
    with col3:
        geography = st.selectbox("🌍 Geography", list(GEOGRAPHIES.keys()), key="geography",
                                  format_func=lambda x: f"{x} — {GEOGRAPHIES[x]['name']}")

    current_sel = f"{skill_type}_{complexity}_{geography}"
    default_sal = get_salary(skill_type, complexity, geography)
    geo_cur = GEOGRAPHIES[geography]['currency']
    geo_sym = GEOGRAPHIES[geography]['symbol']

    if current_sel != st.session_state.prev_selection:
        st.session_state.prev_selection = current_sel
        st.session_state.dynamic_salary = default_sal

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        base_salary = st.number_input(f"💰 Base Monthly Salary ({geo_sym})", value=st.session_state.dynamic_salary,
                                       step=1000, min_value=100, key=f"sal_{current_sel}")
        src = "📂 Master" if master_defaults and current_sel in (master_defaults or {}) else "📋 Built-in"
        st.caption(f"{src} | {geo_cur}")
    with col2:
        ftes = st.number_input("👥 FTEs/Agents", value=100, step=10, min_value=1, max_value=5000, key="ftes")
    with col3:
        wfo_model = st.selectbox("🏢 WFO/WFH", list(WFO_OPTIONS.keys()), key="wfo")
    with col4:
        years = st.slider("📅 Contract (Yrs)", 1, 10, 3, key="years")

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cl = list(CURRENCIES.keys())
        di = cl.index(geo_cur) if geo_cur in cl else 0
        currency = st.selectbox("💱 Display Currency", cl, index=di, key="currency")
    with col2: shrinkage = st.selectbox("📉 Shrinkage", list(SHRINKAGE.keys()), key="shrinkage")
    with col3: attrition = st.selectbox("🔄 Attrition", list(ATTRITION.keys()), key="attrition")
    with col4: margin_target = st.slider("🎯 Target Margin %", 15, 50, 30, step=2, key="margin")

    st.markdown("---")
    st.subheader("💰 Cost Components (%)")
    col1, col2, col3, col4 = st.columns(4)
    with col1: salary_pct = st.slider("Salary", 50, 75, 60, key="sp")
    with col2: benefits_pct = st.slider("Benefits", 5, 20, 12, key="bp")
    with col3: overhead_pct = st.slider("Overhead", 5, 20, 15, key="op")
    with col4: training_pct = st.slider("Training", 3, 15, 5, key="tp")

    col1, col2, col3, col4 = st.columns(4)
    with col1: onboarding_pct = st.slider("Onboarding", 0, 30, 10, step=2, key="obp")
    with col2: qa_pct = st.slider("QA/Audit", 0, 15, 5, key="qap")
    with col3: compliance_pct = st.slider("Compliance", 0, 10, 3, key="cp")
    with col4: tools_pct = st.slider("Tools/Tech", 2, 10, 5, key="tlp")

    st.markdown("---")
    st.subheader("📅 Ramp-Up Schedule")
    col1, col2, col3 = st.columns(3)
    with col1: st.write("**Months 1-3**"); ramp1 = st.slider("Ramp Cost %", 0, 50, 15, step=5, key="r1")
    with col2: st.write("**Months 4-6**"); ramp4 = st.slider("Ramp Cost %", 0, 30, 8, step=5, key="r4")
    with col3: st.write("**Months 7+**"); ramp7 = st.slider("Ramp Cost %", 0, 20, 0, step=5, key="r7")

    st.markdown("---")
    st.subheader("🎁 Incentives & Adjustments")
    col1, col2, col3, col4 = st.columns(4)
    with col1: ret_bonus = st.slider("Retention %", 0, 30, 5, step=2, key="rb")
    with col2: perf_bonus = st.slider("Performance %", 0, 25, 3, step=2, key="pb")
    with col3: skill_prem = st.slider("Skill Premium %", 0, 50, 10, step=5, key="skp")
    with col4: disc_markup = st.slider("Discount/Markup %", -50, 100, 0, step=5, key="dm")

    st.markdown("---")

    # ========== CALCULATIONS ==========
    wfo_f = WFO_OPTIONS[wfo_model]
    comp_m = COMPLEXITY_LEVELS[complexity]['mult']
    shr_r = SHRINKAGE[shrinkage]
    att_r = ATTRITION[attrition]
    cur_f = CURRENCIES[currency]
    cur_s = CUR_SYM[currency]

    tcp = salary_pct + benefits_pct + overhead_pct + training_pct
    mc = base_salary * (tcp / salary_pct) if salary_pct > 0 else 0
    acb = mc * 12
    aca = acb * comp_m * (1 + (1 - wfo_f) * 0.15)

    obc = (base_salary * 12) * (onboarding_pct / 100)
    qac = aca * (qa_pct / 100)
    coc = aca * (compliance_pct / 100)
    tlc = aca * (tools_pct / 100)

    tac_fte = aca + obc + qac + coc + tlc
    shr_c = tac_fte * shr_r
    att_c = tac_fte * att_r
    tac_per_fte = tac_fte + shr_c + att_c
    team_cost = tac_per_fte * ftes

    ramp_cost = (base_salary*12*ramp1/100)*ftes*0.25 + (base_salary*12*ramp4/100)*ftes*0.25 + (base_salary*12*ramp7/100)*ftes*0.50
    ret_c = (base_salary*12*ret_bonus/100)*ftes
    perf_c = (base_salary*12*perf_bonus/100)*ftes
    sk_c = (base_salary*12*skill_prem/100)*ftes

    y1_cost = team_cost + ramp_cost + ret_c + perf_c + sk_c
    final_y1 = y1_cost * (1 + disc_markup/100)

    md = margin_target / 100
    acv = final_y1 / (1 - md) if md < 1 else 0
    tcv = acv * years
    margin_amt = acv - final_y1
    margin_pct = (margin_amt / acv * 100) if acv > 0 else 0

    g2u = 1.0 / CURRENCIES.get(geo_cur, 1.0)
    conv = g2u * cur_f

    # ========== DISPLAY ==========
    st.subheader("💰 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Cost/FTE/Year", f"{cur_s}{tac_per_fte*conv:,.0f}")
    with col2: st.metric("Team Cost/Year", f"{cur_s}{team_cost*conv:,.0f}")
    with col3: st.metric("ACV", f"{cur_s}{acv*conv:,.0f}")
    with col4: st.metric("TCV", f"{cur_s}{tcv*conv:,.0f}")
    with col5: st.metric("Margin", f"{margin_pct:.1f}%")

    st.markdown("---")
    st.info(f"📌 **{skill_type} | {complexity} | {GEOGRAPHIES[geography]['name']}** → Base: {geo_sym}{base_salary:,}/mo")

    st.subheader("📊 Cost Breakdown (per FTE)")
    cost_df = pd.DataFrame({
        "Component": ["Salary","Benefits","Overhead","Training","QA/Audit","Compliance","Tools/Tech","Onboarding","Shrinkage","Attrition","TOTAL"],
        f"Local ({geo_sym})": [f"{geo_sym}{aca*salary_pct/tcp:,.0f}", f"{geo_sym}{aca*benefits_pct/tcp:,.0f}",
            f"{geo_sym}{aca*overhead_pct/tcp:,.0f}", f"{geo_sym}{aca*training_pct/tcp:,.0f}",
            f"{geo_sym}{qac:,.0f}", f"{geo_sym}{coc:,.0f}", f"{geo_sym}{tlc:,.0f}", f"{geo_sym}{obc:,.0f}",
            f"{geo_sym}{shr_c:,.0f}", f"{geo_sym}{att_c:,.0f}", f"{geo_sym}{tac_per_fte:,.0f}"],
        f"Display ({cur_s})": [f"{cur_s}{aca*salary_pct/tcp*conv:,.0f}", f"{cur_s}{aca*benefits_pct/tcp*conv:,.0f}",
            f"{cur_s}{aca*overhead_pct/tcp*conv:,.0f}", f"{cur_s}{aca*training_pct/tcp*conv:,.0f}",
            f"{cur_s}{qac*conv:,.0f}", f"{cur_s}{coc*conv:,.0f}", f"{cur_s}{tlc*conv:,.0f}", f"{cur_s}{obc*conv:,.0f}",
            f"{cur_s}{shr_c*conv:,.0f}", f"{cur_s}{att_c*conv:,.0f}", f"{cur_s}{tac_per_fte*conv:,.0f}"]
    })
    st.dataframe(cost_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    sn = st.text_input("Scenario Name", value=f"{skill_type}_{complexity}_{geography}_{datetime.now().strftime('%Y%m%d')}", key="sn")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Scenario"):
            st.session_state.scenarios[sn] = {
                "skill_type":skill_type,"complexity":complexity,"geography":geography,
                "base_salary":base_salary,"ftes":ftes,"wfo_model":wfo_model,"years":years,
                "currency":currency,"shrinkage":shrinkage,"attrition":attrition,
                "margin_target":margin_target,"acv":acv*conv,"tcv":tcv*conv,
                "margin_pct":margin_pct,"annual_cost":team_cost*conv,"timestamp":datetime.now().isoformat()
            }
            st.success(f"✅ Saved: {sn}")
    with col2:
        if st.button("📥 Save Template"):
            st.session_state.templates[sn] = {"skill_type":skill_type,"complexity":complexity,"geography":geography,
                "wfo_model":wfo_model,"currency":currency,"margin_target":margin_target}
            st.success("✅ Template Saved")
    with col3:
        st.metric("Scenarios", len(st.session_state.scenarios))

    # ========== EXCEL DOWNLOAD ==========
    st.markdown("---")
    st.subheader("📥 Download Pricing Sheet")

    def gen_excel():
        import io
        out = io.BytesIO()
        with pd.ExcelWriter(out, engine='openpyxl') as w:
            pd.DataFrame({"Parameter":["Skill Type","Complexity","Geography","Geography Name","Base Monthly Salary",
                "Salary Currency","FTEs","WFO/WFH","Contract Years","Display Currency","Shrinkage","Attrition",
                "Target Margin %","","--- Cost % ---","","Salary %","Benefits %","Overhead %","Training %",
                "Onboarding %","QA/Audit %","Compliance %","Tools/Tech %","","--- Ramp-Up ---","",
                "M1-3 Ramp %","M4-6 Ramp %","M7+ Ramp %","","--- Incentives ---","",
                "Retention %","Performance %","Skill Premium %","Discount/Markup %"],
                "Value":[skill_type,complexity,geography,GEOGRAPHIES[geography]['name'],base_salary,
                geo_cur,ftes,wfo_model,years,currency,shrinkage,attrition,margin_target,"","","",
                salary_pct,benefits_pct,overhead_pct,training_pct,onboarding_pct,qa_pct,compliance_pct,tools_pct,
                "","","",ramp1,ramp4,ramp7,"","","",ret_bonus,perf_bonus,skill_prem,disc_markup]
            }).to_excel(w, sheet_name="Inputs", index=False)

            pd.DataFrame({"Metric":["Cost/FTE (Local)","Cost/FTE (Display)","Team Cost (Local)","Team Cost (Display)",
                "ACV","TCV","Margin %","Margin Amount","","--- Y1 ---","","Team Cost","Ramp","Retention",
                "Performance","Skill Premium","Y1 Total","Final Y1"],
                "Value":[f"{geo_sym}{tac_per_fte:,.0f}",f"{cur_s}{tac_per_fte*conv:,.0f}",
                f"{geo_sym}{team_cost:,.0f}",f"{cur_s}{team_cost*conv:,.0f}",f"{cur_s}{acv*conv:,.0f}",
                f"{cur_s}{tcv*conv:,.0f}",f"{margin_pct:.1f}%",f"{cur_s}{margin_amt*conv:,.0f}",
                "","","",f"{geo_sym}{team_cost:,.0f}",f"{geo_sym}{ramp_cost:,.0f}",f"{geo_sym}{ret_c:,.0f}",
                f"{geo_sym}{perf_c:,.0f}",f"{geo_sym}{sk_c:,.0f}",f"{geo_sym}{y1_cost:,.0f}",f"{geo_sym}{final_y1:,.0f}"],
                "Numeric":[tac_per_fte,tac_per_fte*conv,team_cost,team_cost*conv,acv*conv,tcv*conv,
                margin_pct,margin_amt*conv,"","","",team_cost,ramp_cost,ret_c,perf_c,sk_c,y1_cost,final_y1]
            }).to_excel(w, sheet_name="Key Metrics", index=False)

            pd.DataFrame({"Component":["Salary","Benefits","Overhead","Training","QA","Compliance","Tools","Onboarding","Shrinkage","Attrition","TOTAL"],
                f"Local ({geo_sym})":[round(aca*salary_pct/tcp),round(aca*benefits_pct/tcp),round(aca*overhead_pct/tcp),
                round(aca*training_pct/tcp),round(qac),round(coc),round(tlc),round(obc),round(shr_c),round(att_c),round(tac_per_fte)],
                f"Display ({cur_s})":[round(aca*salary_pct/tcp*conv),round(aca*benefits_pct/tcp*conv),round(aca*overhead_pct/tcp*conv),
                round(aca*training_pct/tcp*conv),round(qac*conv),round(coc*conv),round(tlc*conv),round(obc*conv),round(shr_c*conv),round(att_c*conv),round(tac_per_fte*conv)]
            }).to_excel(w, sheet_name="Cost Breakdown", index=False)

            yr_rows = []
            for yr in range(1, years+1):
                yc = final_y1 if yr==1 else team_cost*(1+disc_markup/100)
                ya = yc/(1-md) if md<1 else 0
                ym = ya-yc
                yr_rows.append({"Year":yr,f"Cost ({geo_sym})":round(yc),f"Revenue ({geo_sym})":round(ya),
                    f"Margin ({geo_sym})":round(ym),"Margin %":f"{(ym/ya*100) if ya>0 else 0:.1f}%",
                    f"Cost ({cur_s})":round(yc*conv),f"Revenue ({cur_s})":round(ya*conv)})
            pd.DataFrame(yr_rows).to_excel(w, sheet_name="Multi-Year", index=False)

            if geography in GEO_SALARIES:
                sr = []
                for sk in ["Voice","Non-voice","Backoffice"]:
                    for lv in ["L1","L2","L3","L4","L5","L6"]:
                        mv = master_defaults.get(f"{sk}_{lv}_{geography}") if master_defaults else None
                        bv = GEO_SALARIES.get(geography,{}).get(sk,{}).get(lv,"N/A")
                        sr.append({"Skill":sk,"Level":lv,"Geo":geography,f"Built-in ({geo_sym})":bv,
                            f"Master ({geo_sym})":mv if mv else "N/A","Source":"Master" if mv else "Built-in"})
                pd.DataFrame(sr).to_excel(w, sheet_name="Salary Reference", index=False)

            for sname in w.sheets:
                ws = w.sheets[sname]
                for cc in ws.columns:
                    ml = max(len(str(c.value or "")) for c in cc)
                    ws.column_dimensions[cc[0].column_letter].width = min(ml+3, 40)
        out.seek(0)
        return out

    fn = f"Firstsource_Pricing_{skill_type}_{complexity}_{geography}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    st.download_button("📥 Download Full Pricing Sheet (Excel)", gen_excel(), fn,
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.caption(f"5 sheets: Inputs | Metrics | Breakdown | {years}-Year Projection | Salary Reference")

# ==================== TAB 2-8 (same logic, branded) ====================
with tab2:
    st.header("📚 Pricing Templates")
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Saved Templates")
        if st.session_state.templates:
            for tn,t in st.session_state.templates.items():
                st.write(f"**{tn}** — {t['skill_type']} | {t['complexity']} | {t['geography']}")
        else: st.info("No templates saved yet")
    with c2:
        st.subheader("Quick Start")
        for t in ["Voice L1 (India)","Backoffice L2 (Phil)","Non-voice L3 (US)"]: st.write(f"**{t}**")

with tab3:
    st.header("🔄 Scenario Comparison")
    if not st.session_state.scenarios: st.warning("⚠️ Save scenarios first!")
    else:
        sel = st.multiselect("Compare", list(st.session_state.scenarios.keys()), max_selections=6)
        if sel:
            rows = [{"Scenario":n,"Skill":s["skill_type"],"Level":s["complexity"],"Geo":s["geography"],
                "FTEs":s["ftes"],"ACV":f"${s['acv']:,.0f}","TCV":f"${s['tcv']:,.0f}","Margin":f"{s['margin_pct']:.1f}%"}
                for n,s in st.session_state.scenarios.items() if n in sel]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tab4:
    st.header("⚠️ Risk Assessment")
    if not st.session_state.scenarios: st.warning("⚠️ Create scenarios first!")
    else:
        rsc = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="rsc")
        scores = []
        for cat, factors in RISK_CATEGORIES.items():
            with st.expander(cat, expanded=(cat=="Operational Risk")):
                c1,c2 = st.columns(2)
                cs = []
                for i,(fn2,fv) in enumerate(factors.items()):
                    with (c1 if i%2==0 else c2):
                        v = st.selectbox(fn2, ["Low","Medium","High","Critical"], key=f"r_{cat}_{fn2}")
                        cs.append(fv[v])
                a = np.mean(cs); scores.append(a); st.metric(f"{cat}", f"{a:.2%}")
        st.markdown("---")
        ov = np.mean(scores)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("OVERALL RISK", f"{ov:.2%}")
        with c2:
            if ov<0.05: st.success("🟢 LOW")
            elif ov<0.10: st.info("🟡 MODERATE")
            else: st.error("🔴 HIGH")
        with c3: st.metric("Risk-Adj Margin", f"{st.session_state.scenarios[rsc]['margin_pct']-ov*100:.1f}%")

with tab5:
    st.header("🎯 Decision Dashboard")
    if not st.session_state.scenarios: st.warning("⚠️ Create scenarios first!")
    else:
        ds = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="ds")
        s = st.session_state.scenarios[ds]
        c1,c2 = st.columns(2)
        with c1: d1=st.slider("Margin",1,10,7,key="d1"); d2=st.slider("Growth",1,10,6,key="d2"); d3=st.slider("Client",1,10,7,key="d3"); d4=st.slider("Stability",1,10,6,key="d4")
        with c2: d5=st.slider("Risk(1=Hi)",1,10,5,key="d5"); d6=st.slider("Execution",1,10,7,key="d6"); d7=st.slider("Scalability",1,10,6,key="d7"); d8=st.slider("Strategic",1,10,7,key="d8")
        ws=d1*.20+d2*.15+d3*.15+d4*.10+d5*.15+d6*.10+d7*.10+d8*.05
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Score",f"{ws:.1f}/10")
        with c2:
            if ws>=8: st.success("🟢 STRONG BUY")
            elif ws>=6.5: st.info("🟡 BUY")
            else: st.error("🔴 PASS")
        with c3: st.metric("Margin",f"{s['margin_pct']:.1f}%")

with tab6:
    st.header("💹 ROI Analysis")
    if not st.session_state.scenarios: st.warning("⚠️ Create scenarios first!")
    else:
        rs2 = st.selectbox("Scenario", list(st.session_state.scenarios.keys()), key="rs2")
        s = st.session_state.scenarios[rs2]
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
            ss=st.selectbox("Scenario",list(st.session_state.scenarios.keys()),key="ss")
            s=st.session_state.scenarios[ss]
            rows=[{"FTEs":int(s['ftes']*m),"Change":f"{(m-1)*100:+.0f}%","ACV":f"${s['acv']*m:,.0f}"} for m in [0.8,0.9,1.0,1.1,1.2]]
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
        with st.expander("🔍 Loaded Entries"):
            for k,v in sorted(master_defaults.items()): st.caption(f"{k}: {v:,.0f}")

# ==================== FIRSTSOURCE FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div class="fs-footer">
    <strong>Firstsource | Enterprise Pricing Platform</strong><br>
    <span style="color:#6CB1DB; font-size:0.85rem;">Salary auto-updates with Skill × Level × Geography | Editable FTE | 9 Geographies | 6 Levels</span><br>
    <span style="font-size:0.75rem; color:#9ca3af;">Copyright © {datetime.now().year} Firstsource. All rights reserved. | We make it happen!</span>
</div>
""", unsafe_allow_html=True)
