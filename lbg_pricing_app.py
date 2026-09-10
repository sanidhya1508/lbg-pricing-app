import streamlit as st
import pandas as pd
import json
from datetime import datetime
import numpy as np

st.set_page_config(page_title="Enterprise Pricing", layout="wide")

st.title("🎯 Enterprise Pricing Calculator - Multi-Project Hybrid Flex Edition")
st.markdown("**Maximum Variability | Cross-Project Comparison | Advanced Scenarios**")
st.markdown("---")

# ==================== PROJECT DEFINITIONS ====================

PROJECTS = {
    "LBG Fraud Proactive": {
        "color": "🔵",
        "base_costs": {
            "UK": 44200,
            "India": 10400,
            "Philippines": 9650,
            "South Africa": 15600
        },
        "regions": ["UK", "India", "Philippines", "South Africa"],
        "delivery_models": {
            "EB (Existing Business)": 0.95,
            "NB_WAH (Work At Home)": 0.85,
            "NB_WAO (Work At Office)": 1.0
        },
        "capabilities": {
            "Account Servicing": 0.25,
            "Fraud Response": 0.30,
            "Compliance Support": 0.28,
            "Data Analytics": 0.35
        },
        "channels": {
            "Voice": 1.2,
            "Email": 0.9,
            "Chat": 1.0,
            "Blended": 1.05
        },
        "complexity_multipliers": {
            "Low": 1.0,
            "Medium": 1.15,
            "High": 1.35,
            "Very High": 1.60
        }
    },
    "Palmetto CMT": {
        "color": "🟢",
        "base_costs": {
            "North America": 38000,
            "Europe": 42000,
            "APAC": 12000,
            "LATAM": 11000
        },
        "regions": ["North America", "Europe", "APAC", "LATAM"],
        "delivery_models": {
            "Onshore": 1.15,
            "Nearshore": 0.95,
            "Offshore": 0.70
        },
        "capabilities": {
            "BPO Basic": 0.22,
            "BPO Advanced": 0.32,
            "Technology Services": 0.38,
            "Consulting": 0.40
        },
        "channels": {
            "Phone": 1.25,
            "Chat": 0.95,
            "Email": 0.85,
            "Omnichannel": 1.10
        },
        "complexity_multipliers": {
            "Standard": 1.0,
            "Complex": 1.25,
            "Highly Complex": 1.50,
            "Mission Critical": 1.80
        }
    }
}

# ==================== GLOBAL VARIABILITY FACTORS ====================

COMPLEXITY_LEVELS = {
    "Low": 1.0,
    "Medium": 1.15,
    "High": 1.35,
    "Very High": 1.60
}

ATTRITION_RATES = {
    "Low (5%)": 0.05,
    "Medium (10%)": 0.10,
    "High (15%)": 0.15,
    "Very High (20%)": 0.20
}

CLIENT_TYPES = {
    "Startup": 0.80,
    "SMB": 0.90,
    "Enterprise": 1.0,
    "Fortune 500": 1.15,
    "Government": 1.25
}

SLA_LEVELS = {
    "Basic (95%)": 0.95,
    "Standard (99%)": 1.0,
    "Premium (99.5%)": 1.10,
    "Elite (99.9%)": 1.25
}

SUPPORT_MODELS = {
    "Business Hours": 0.85,
    "24/5": 1.0,
    "24/7": 1.30,
    "24/7 + Dedicated": 1.50
}

CURRENCIES = {
    "USD": 1.0,
    "GBP": 1.27,
    "EUR": 0.92,
    "INR": 82.5,
    "PHP": 55.0,
    "CAD": 1.36
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "INR": "₹",
    "PHP": "₱",
    "CAD": "C$"
}

PRICING_TIERS = {
    "Bronze": {"margin": 0.20, "discount": 0.0, "description": "Standard"},
    "Silver": {"margin": 0.28, "discount": 0.05, "description": "Enhanced"},
    "Gold": {"margin": 0.35, "discount": 0.10, "description": "Premium"},
    "Platinum": {"margin": 0.42, "discount": 0.15, "description": "Elite"}
}

# Additional cost components
COST_COMPONENTS = {
    "Salary": 0.60,
    "Benefits": 0.12,
    "Overhead": 0.15,
    "Training": 0.08,
    "Tools & Tech": 0.05
}

# ==================== SESSION STATE ====================
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

if 'saved_projects' not in st.session_state:
    st.session_state.saved_projects = {}

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Calculator",
    "🔄 Comparison",
    "💎 Pricing Tiers",
    "🌍 Multi-Currency",
    "📈 Advanced Analysis",
    "⚙️ Customization"
])

# ==================== TAB 1: CALCULATOR ====================
with tab1:
    st.header("📊 Hybrid Flexibility Calculator")
    
    # Project Selection
    col_proj, col_save = st.columns([3, 1])
    with col_proj:
        project = st.selectbox("Select Project", list(PROJECTS.keys()))
        st.write(f"**Project:** {PROJECTS[project]['color']} {project}")
    
    with col_save:
        scenario_name = st.text_input("Scenario Name", value=f"{project}_Scenario", key="scenario_name_main")
    
    st.markdown("---")
    
    # SECTION 1: Core Parameters
    st.subheader("🎯 SECTION 1: Core Pricing Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        region = st.selectbox("Region/Geography", PROJECTS[project]["regions"], key="region")
    with col2:
        fte = st.slider("Number of FTEs", 10, 1000, 50, key="fte")
    with col3:
        delivery_model = st.selectbox("Delivery Model", list(PROJECTS[project]["delivery_models"].keys()), key="delivery")
    with col4:
        capability = st.selectbox("Capability", list(PROJECTS[project]["capabilities"].keys()), key="capability")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        complexity = st.selectbox("Complexity Level", list(PROJECTS[project]["complexity_multipliers"].keys()), key="complexity")
    with col2:
        channel = st.selectbox("Primary Channel", list(PROJECTS[project]["channels"].keys()), key="channel")
    with col3:
        years = st.slider("Contract Duration (Years)", 1, 10, 3, key="years")
    with col4:
        currency = st.selectbox("Currency", list(CURRENCIES.keys()), key="currency")
    
    st.markdown("---")
    
    # SECTION 2: Financial Adjustments
    st.subheader("💰 SECTION 2: Financial Adjustments & Pricing Multipliers")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        discount_markup = st.slider("Discount/Markup (%)", -50, 100, 0, step=5, key="discount")
    with col2:
        volume_discount = st.slider("Volume Discount (%)", 0, 30, 0, step=2, key="volume")
    with col3:
        long_term_discount = st.slider("Long-term Discount (%)", 0, 20, 0, step=2, key="longterm")
    with col4:
        client_type = st.selectbox("Client Type", list(CLIENT_TYPES.keys()), key="client")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sla_level = st.selectbox("SLA Level", list(SLA_LEVELS.keys()), key="sla")
    with col2:
        support_model = st.selectbox("Support Model", list(SUPPORT_MODELS.keys()), key="support")
    with col3:
        pricing_tier = st.selectbox("Pricing Tier", list(PRICING_TIERS.keys()), key="tier")
    with col4:
        margin_override = st.slider("Margin Override (%)", 15, 50, 0, step=2, key="margin_override")
    
    st.markdown("---")
    
    # SECTION 3: Operational Factors
    st.subheader("⚙️ SECTION 3: Operational & Risk Factors")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        attrition = st.selectbox("Annual Attrition Rate", list(ATTRITION_RATES.keys()), key="attrition")
    with col2:
        onboarding_cost_pct = st.slider("Onboarding Cost (% of salary)", 0, 50, 20, step=5, key="onboarding")
    with col3:
        training_depth = st.slider("Training Depth Multiplier", 0.5, 2.0, 1.0, step=0.1, key="training")
    with col4:
        compliance_cost = st.slider("Compliance Cost (% of total)", 0, 15, 3, step=1, key="compliance")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        quality_multiplier = st.slider("Quality/Audit Multiplier", 0.8, 1.5, 1.0, step=0.05, key="quality")
    with col2:
        management_overhead = st.slider("Management Overhead (% of salary)", 0, 40, 15, step=2, key="mgmt")
    with col3:
        travel_cost_pct = st.slider("Travel Cost (% of salary)", 0, 20, 2, step=1, key="travel")
    with col4:
        insurance_cost_pct = st.slider("Insurance Cost (% of salary)", 0, 10, 3, step=1, key="insurance")
    
    st.markdown("---")
    
    # SECTION 4: Ramp-Up & Utilization
    st.subheader("📅 SECTION 4: Ramp-Up Schedule & Utilization")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Month 1-3 Utilization**")
        ramp_m1_util = st.slider("Utilization %", 20, 100, 50, step=5, key="ramp_m1_util")
        ramp_m1_bonus = st.slider("Ramp Bonus Cost (%)", 0, 50, 10, step=5, key="ramp_m1_bonus")
    
    with col2:
        st.write("**Month 4-6 Utilization**")
        ramp_m4_util = st.slider("Utilization %", 50, 100, 75, step=5, key="ramp_m4_util")
        ramp_m4_bonus = st.slider("Ramp Bonus Cost (%)", 0, 30, 5, step=5, key="ramp_m4_bonus")
    
    with col3:
        st.write("**Month 7+ Utilization**")
        ramp_m7_util = st.slider("Utilization %", 75, 100, 100, step=5, key="ramp_m7_util")
        ramp_m7_bonus = st.slider("Ramp Bonus Cost (%)", 0, 20, 0, step=5, key="ramp_m7_bonus")
    
    st.markdown("---")
    
    # SECTION 5: Retention & Incentives
    st.subheader("🎁 SECTION 5: Retention & Performance Incentives")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        retention_bonus = st.slider("Retention Bonus (% of salary)", 0, 30, 5, step=2, key="retention")
    with col2:
        performance_bonus = st.slider("Performance Bonus (% of salary)", 0, 25, 3, step=2, key="performance")
    with col3:
        skill_premium = st.slider("Specialized Skills Premium (%)", 0, 50, 10, step=5, key="skill_premium")
    with col4:
        certification_cost = st.slider("Certification Cost (% of salary)", 0, 15, 2, step=1, key="certification")
    
    st.markdown("---")
    
    # ==================== CALCULATIONS ====================
    
    project_data = PROJECTS[project]
    base_annual_cost = project_data["base_costs"][region]
    
    # Apply complexity, delivery, channel multipliers
    complexity_mult = project_data["complexity_multipliers"][complexity]
    delivery_mult = project_data["delivery_models"][delivery_model]
    channel_mult = project_data["channels"][channel]
    client_mult = CLIENT_TYPES[client_type]
    sla_mult = SLA_LEVELS[sla_level]
    support_mult = SUPPORT_MODELS[support_model]
    
    # Base cost per FTE with all multipliers
    cost_per_fte = base_annual_cost * complexity_mult * delivery_mult * channel_mult * client_mult * sla_mult * support_mult
    
    # Cost breakdown
    salary = cost_per_fte * 0.60
    benefits = cost_per_fte * 0.12
    overhead = cost_per_fte * 0.15
    tools_tech = cost_per_fte * 0.08
    base_training = cost_per_fte * 0.05
    
    # Apply training depth
    final_training = base_training * training_depth
    
    # Adjust for additional costs
    onboarding = salary * (onboarding_cost_pct / 100)
    compliance = (salary + benefits + overhead + tools_tech + final_training) * (compliance_cost / 100)
    travel = salary * (travel_cost_pct / 100)
    insurance_add = salary * (insurance_cost_pct / 100)
    mgmt_overhead = salary * (management_overhead / 100)
    quality_cost = (salary + benefits + overhead + tools_tech + final_training) * quality_multiplier
    
    # Total cost per FTE (annual)
    total_cost_per_fte = (salary + benefits + overhead + tools_tech + final_training + 
                          compliance + travel + insurance_add + mgmt_overhead)
    
    # Apply ramp-up costs for year 1
    year1_adjustments = (ramp_m1_bonus + ramp_m4_bonus + ramp_m7_bonus) / 100 * salary * fte
    
    # Apply retention and incentives
    retention_cost = salary * (retention_bonus / 100) * fte
    performance_cost = salary * (performance_bonus / 100) * fte
    skill_cost = salary * (skill_premium / 100) * fte
    cert_cost = salary * (certification_cost / 100) * fte
    
    # Total annual cost per FTE
    total_fte_cost = total_cost_per_fte * fte
    
    # Attrition cost
    attrition_rate = ATTRITION_RATES[attrition]
    additional_attrition_cost = total_fte_cost * attrition_rate
    
    # Total operational cost
    total_operational_cost = total_fte_cost + additional_attrition_cost
    
    # Year 1 with ramp-up and incentives
    year1_cost = total_operational_cost + year1_adjustments + retention_cost + performance_cost + skill_cost + cert_cost
    
    # Apply financial discounts
    discount_factor = (1 + discount_markup / 100) * (1 - volume_discount / 100) * (1 - long_term_discount / 100)
    year1_cost_adjusted = year1_cost * discount_factor
    
    # Revenue calculation
    if margin_override > 0:
        margin_target = margin_override / 100
    else:
        margin_target = project_data["capabilities"][capability]
        if pricing_tier:
            tier_margin = PRICING_TIERS[pricing_tier]["margin"]
            margin_target = tier_margin
    
    acv = year1_cost_adjusted / (1 - margin_target)
    tcv = acv * years
    margin_dollars = acv - year1_cost_adjusted
    margin_pct = (margin_dollars / acv) * 100
    
    # Apply currency conversion
    currency_factor = CURRENCIES[currency]
    acv_converted = acv * currency_factor
    tcv_converted = tcv * currency_factor
    margin_converted = margin_dollars * currency_factor
    
    currency_symbol = CURRENCY_SYMBOLS[currency]
    
    # ==================== DISPLAY ====================
    
    st.markdown("---")
    st.subheader("💰 KEY FINANCIAL METRICS")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Annual Cost", f"{currency_symbol}{year1_cost_adjusted/currency_factor:,.0f}")
    with col2:
        st.metric("ACV", f"{currency_symbol}{acv_converted:,.0f}")
    with col3:
        st.metric("TCV", f"{currency_symbol}{tcv_converted:,.0f}")
    with col4:
        st.metric("Margin $", f"{currency_symbol}{margin_converted:,.0f}")
    with col5:
        st.metric("Margin %", f"{margin_pct:.1f}%")
    
    st.markdown("---")
    
    # Cost Breakdown
    st.subheader("📊 Detailed Cost Breakdown")
    
    breakdown = {
        "Cost Component": [
            "Base Salary (per FTE)",
            "Benefits",
            "Overhead",
            "Tools & Technology",
            "Training",
            "Compliance",
            "Travel",
            "Insurance",
            "Management Overhead",
            "Quality/Audit",
            "Onboarding (Y1 only)",
            "---",
            "SUBTOTAL (per FTE)",
            "Total FTEs",
            "Annual Cost (All FTEs)",
            "Attrition Cost",
            "Retention Bonus (Y1)",
            "Performance Bonus (Y1)",
            "Skills Premium (Y1)",
            "Certification (Y1)",
            "Ramp-up Adjustments (Y1)",
            "---",
            "YEAR 1 TOTAL",
            "Financial Adjustments",
            "FINAL YEAR 1 COST",
            "---",
            "Margin %",
            "ACV",
            "TCV"
        ],
        "Value": [
            f"{currency_symbol}{salary*currency_factor:,.0f}",
            f"{currency_symbol}{benefits*currency_factor:,.0f}",
            f"{currency_symbol}{overhead*currency_factor:,.0f}",
            f"{currency_symbol}{tools_tech*currency_factor:,.0f}",
            f"{currency_symbol}{final_training*currency_factor:,.0f}",
            f"{currency_symbol}{compliance*currency_factor:,.0f}",
            f"{currency_symbol}{travel*currency_factor:,.0f}",
            f"{currency_symbol}{insurance_add*currency_factor:,.0f}",
            f"{currency_symbol}{mgmt_overhead*currency_factor:,.0f}",
            f"{currency_symbol}{(quality_cost/fte)*currency_factor:,.0f}",
            f"{currency_symbol}{(onboarding/fte)*currency_factor:,.0f}",
            "—",
            f"{currency_symbol}{total_cost_per_fte*currency_factor:,.0f}",
            f"{fte}",
            f"{currency_symbol}{total_fte_cost*currency_factor:,.0f}",
            f"{currency_symbol}{additional_attrition_cost*currency_factor:,.0f}",
            f"{currency_symbol}{retention_cost*currency_factor:,.0f}",
            f"{currency_symbol}{performance_cost*currency_factor:,.0f}",
            f"{currency_symbol}{skill_cost*currency_factor:,.0f}",
            f"{currency_symbol}{cert_cost*currency_factor:,.0f}",
            f"{currency_symbol}{year1_adjustments*currency_factor:,.0f}",
            "—",
            f"{currency_symbol}{year1_cost*currency_factor:,.0f}",
            f"{discount_markup:+.0f}% / {-volume_discount:.0f}% / {-long_term_discount:.0f}%",
            f"{currency_symbol}{year1_cost_adjusted*currency_factor:,.0f}",
            "—",
            f"{margin_pct:.1f}%",
            f"{currency_symbol}{acv_converted:,.0f}",
            f"{currency_symbol}{tcv_converted:,.0f}"
        ]
    }
    
    st.dataframe(pd.DataFrame(breakdown), use_container_width=True)
    
    st.markdown("---")
    
    # Save scenario
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Scenario", key="save_main"):
            st.session_state.scenarios[scenario_name] = {
                "project": project,
                "region": region,
                "fte": fte,
                "delivery_model": delivery_model,
                "capability": capability,
                "complexity": complexity,
                "channel": channel,
                "years": years,
                "currency": currency,
                "discount_markup": discount_markup,
                "volume_discount": volume_discount,
                "long_term_discount": long_term_discount,
                "client_type": client_type,
                "sla_level": sla_level,
                "support_model": support_model,
                "pricing_tier": pricing_tier,
                "margin_override": margin_override,
                "attrition": attrition,
                "onboarding_cost_pct": onboarding_cost_pct,
                "training_depth": training_depth,
                "compliance_cost": compliance_cost,
                "quality_multiplier": quality_multiplier,
                "management_overhead": management_overhead,
                "travel_cost_pct": travel_cost_pct,
                "insurance_cost_pct": insurance_cost_pct,
                "retention_bonus": retention_bonus,
                "performance_bonus": performance_bonus,
                "skill_premium": skill_premium,
                "certification_cost": certification_cost,
                "acv": acv_converted,
                "tcv": tcv_converted,
                "margin_pct": margin_pct
            }
            st.success(f"✅ Saved: {scenario_name}")
    
    with col2:
        if st.button("📥 Export to JSON", key="export_json_main"):
            export_data = {
                "scenario": scenario_name,
                "timestamp": datetime.now().isoformat(),
                "project": project,
                "parameters": {
                    "region": region,
                    "fte": fte,
                    "complexity": complexity,
                    "years": years,
                    "currency": currency
                },
                "financial": {
                    "annual_cost": float(year1_cost_adjusted / currency_factor),
                    "acv": float(acv),
                    "tcv": float(tcv),
                    "margin_dollars": float(margin_dollars),
                    "margin_pct": float(margin_pct)
                }
            }
            
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                "📥 Download JSON",
                json_str,
                f"{scenario_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )


# ==================== TAB 2: COMPARISON ====================
with tab2:
    st.header("🔄 Multi-Project Scenario Comparison")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved yet. Create scenarios in the Calculator tab first!")
    else:
        scenarios_list = list(st.session_state.scenarios.keys())
        selected = st.multiselect("Select scenarios to compare:", scenarios_list, max_selections=6)
        
        if selected:
            comparison_data = []
            for scenario_name in selected:
                s = st.session_state.scenarios[scenario_name]
                comparison_data.append({
                    "Scenario": scenario_name,
                    "Project": s["project"],
                    "Region": s["region"],
                    "FTEs": s["fte"],
                    "Complexity": s["complexity"],
                    "Annual Cost": f"{s['currency']}{s['acv']/(s['years']):,.0f}",
                    "ACV": f"{s['currency']}{s['acv']:,.0f}",
                    "TCV": f"{s['currency']}{s['tcv']:,.0f}",
                    "Margin %": f"{s['margin_pct']:.1f}%"
                })
            
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
            
            # Best option
            if len(comparison_data) > 1:
                st.subheader("🏆 Recommendations")
                margins = [float(c["Margin %"].rstrip("%")) for c in comparison_data]
                best_idx = margins.index(max(margins))
                worst_idx = margins.index(min(margins))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"**Highest Margin:** {selected[best_idx]} ({max(margins):.1f}%)")
                with col2:
                    st.info(f"**Lowest Margin:** {selected[worst_idx]} ({min(margins):.1f}%)")


# ==================== TAB 3: PRICING TIERS ====================
with tab3:
    st.header("💎 Pricing Tier Comparison")
    
    project_sel = st.selectbox("Select Project:", list(PROJECTS.keys()), key="tier_project")
    region_sel = st.selectbox("Select Region:", PROJECTS[project_sel]["regions"], key="tier_region")
    fte_sel = st.slider("FTEs:", 10, 500, 100, key="tier_fte")
    
    tier_data = []
    for tier_name, tier_info in PRICING_TIERS.items():
        base = PROJECTS[project_sel]["base_costs"][region_sel] * fte_sel
        margin = tier_info["margin"]
        acv_tier = base / (1 - margin)
        tier_data.append({
            "Tier": tier_name,
            "Margin": f"{margin*100:.0f}%",
            "Discount": f"{tier_info['discount']*100:.0f}%",
            "Description": tier_info['description'],
            "Annual Cost": f"${base:,.0f}",
            "ACV": f"${acv_tier:,.0f}"
        })
    
    st.dataframe(pd.DataFrame(tier_data), use_container_width=True)


# ==================== TAB 4: MULTI-CURRENCY ====================
with tab4:
    st.header("🌍 Multi-Currency Analysis")
    
    base_amount = st.number_input("Base Amount (USD):", value=100000, step=1000)
    
    curr_data = []
    for curr, factor in CURRENCIES.items():
        symbol = CURRENCY_SYMBOLS[curr]
        curr_data.append({
            "Currency": curr,
            "Symbol": symbol,
            "Converted Amount": f"{symbol}{base_amount * factor:,.0f}",
            "Rate": f"{factor}x"
        })
    
    st.dataframe(pd.DataFrame(curr_data), use_container_width=True)


# ==================== TAB 5: ADVANCED ANALYSIS ====================
with tab5:
    st.header("📈 Advanced Scenario Analysis")
    
    st.subheader("What-If Analysis")
    
    if len(st.session_state.scenarios) > 0:
        base_scenario = st.selectbox("Base Scenario:", list(st.session_state.scenarios.keys()), key="whatif_scenario")
        base_data = st.session_state.scenarios[base_scenario]
        
        # FTE variation
        st.write("**FTE Sensitivity:**")
        fte_scenarios = [base_data["fte"] * 0.8, base_data["fte"], base_data["fte"] * 1.2]
        
        whatif_results = []
        for fte_var in fte_scenarios:
            # Simplified calculation for comparison
            factor = fte_var / base_data["fte"]
            whatif_results.append({
                "FTE Scenario": f"{int(fte_var)}",
                "Change": f"{(factor-1)*100:+.0f}%",
                "Est. ACV": f"${base_data['acv'] * factor:,.0f}",
                "Est. Margin $": f"${(base_data['acv'] - (base_data['acv']/(1-base_data['margin_pct']/100))) * factor:,.0f}"
            })
        
        st.dataframe(pd.DataFrame(whatif_results), use_container_width=True)
    else:
        st.warning("Create a scenario first to enable What-If analysis")


# ==================== TAB 6: CUSTOMIZATION ====================
with tab6:
    st.header("⚙️ Customization & Extensibility")
    
    st.subheader("Add New Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_project_name = st.text_input("New Project Name:")
        new_project_regions = st.text_input("Regions (comma-separated):", "Region1, Region2, Region3")
        new_project_base_cost = st.number_input("Base Cost (USD):", value=40000, step=1000)
    
    with col2:
        if st.button("➕ Add Project"):
            if new_project_name and new_project_regions:
                regions_list = [r.strip() for r in new_project_regions.split(",")]
                new_proj_data = {
                    "color": "🟡",
                    "base_costs": {r: new_project_base_cost for r in regions_list},
                    "regions": regions_list,
                    "delivery_models": {"Standard": 1.0, "Premium": 1.2},
                    "capabilities": {"Basic": 0.25, "Advanced": 0.35},
                    "channels": {"Standard": 1.0, "Omnichannel": 1.15},
                    "complexity_multipliers": {"Standard": 1.0, "Complex": 1.3}
                }
                st.session_state.saved_projects[new_project_name] = new_proj_data
                st.success(f"✅ Added project: {new_project_name}")
    
    st.markdown("---")
    
    st.subheader("Saved Custom Projects")
    if st.session_state.saved_projects:
        for proj_name, proj_data in st.session_state.saved_projects.items():
            st.write(f"**{proj_name}** - Regions: {', '.join(proj_data['regions'])}")
    else:
        st.info("No custom projects yet")


# ==================== FOOTER ====================
st.markdown("---")
st.success("✅ **Enterprise Pricing Calculator - Hybrid Flexibility Edition**")
st.caption("🚀 MAXIMUM VARIABILITY | Multi-Project | Advanced Scenarios | Cross-Project Comparison")
st.caption(f"📊 Saved Scenarios: {len(st.session_state.scenarios)} | Custom Projects: {len(st.session_state.saved_projects)}")
