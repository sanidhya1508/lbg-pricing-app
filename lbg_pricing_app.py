import streamlit as st
import pandas as pd
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Enterprise Pricing", layout="wide")

st.title("🎯 Enterprise Pricing Calculator - Decision Intelligence Edition")
st.markdown("**LBG | Palmetto | BCBS | Risk Assessment | Decision Support**")
st.markdown("---")

# ==================== PROJECT DEFINITIONS ====================

PROJECTS = {
    "LBG Fraud Proactive": {
        "color": "🔵",
        "icon": "🛡️",
        "description": "Fraud Detection & Compliance Services",
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
        "icon": "💼",
        "description": "Business Process Outsourcing & Tech Services",
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
    },
    "BCBS Telesales": {
        "color": "🟡",
        "icon": "☎️",
        "description": "Telesales & Contact Center Operations",
        "base_costs": {
            "United States": 28000,
            "Canada": 32000,
            "UK": 38000,
            "India": 8500,
            "Philippines": 7800
        },
        "regions": ["United States", "Canada", "UK", "India", "Philippines"],
        "delivery_models": {
            "Dedicated": 1.10,
            "Shared": 0.85,
            "Flexible": 0.95
        },
        "capabilities": {
            "Outbound Campaigns": 0.20,
            "Inbound Support": 0.25,
            "Sales Development": 0.32,
            "Premium Services": 0.38
        },
        "channels": {
            "Phone": 1.30,
            "Chat Support": 0.80,
            "Email": 0.70,
            "Multi-channel": 1.05
        },
        "complexity_multipliers": {
            "Basic": 1.0,
            "Standard": 1.10,
            "Advanced": 1.30,
            "Enterprise": 1.50
        }
    }
}

# ==================== RISK PARAMETERS ====================

RISK_CATEGORIES = {
    "Operational Risk": {
        "Attrition Risk": {"Low": 0.05, "Medium": 0.10, "High": 0.15, "Critical": 0.25},
        "Quality Risk": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.20},
        "Compliance Risk": {"Low": 0.03, "Medium": 0.07, "High": 0.12, "Critical": 0.18},
        "Technology Risk": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15}
    },
    "Financial Risk": {
        "Currency Risk": {"Low": 0.01, "Medium": 0.03, "High": 0.06, "Critical": 0.10},
        "Volume Risk": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Cost Inflation Risk": {"Low": 0.02, "Medium": 0.04, "High": 0.07, "Critical": 0.12},
        "Margin Compression Risk": {"Low": 0.03, "Medium": 0.06, "High": 0.10, "Critical": 0.15}
    },
    "Client Risk": {
        "Client Concentration": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Contract Renewal Risk": {"Low": 0.03, "Medium": 0.07, "High": 0.12, "Critical": 0.20},
        "Scope Creep Risk": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "SLA Non-Performance": {"Low": 0.02, "Medium": 0.04, "High": 0.08, "Critical": 0.12}
    },
    "Market Risk": {
        "Market Volatility": {"Low": 0.02, "Medium": 0.04, "High": 0.08, "Critical": 0.12},
        "Competition Risk": {"Low": 0.03, "Medium": 0.06, "High": 0.10, "Critical": 0.15},
        "Regulatory Risk": {"Low": 0.02, "Medium": 0.05, "High": 0.10, "Critical": 0.15},
        "Geopolitical Risk": {"Low": 0.01, "Medium": 0.03, "High": 0.06, "Critical": 0.12}
    }
}

# ==================== GLOBAL SETTINGS ====================

ATTRITION_RATES = {
    "Low (5%)": 0.05,
    "Medium (10%)": 0.10,
    "High (15%)": 0.15,
    "Very High (20%)": 0.20,
    "Critical (25%)": 0.25
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

# ==================== SESSION STATE ====================
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

if 'saved_projects' not in st.session_state:
    st.session_state.saved_projects = {}

if 'risk_assessments' not in st.session_state:
    st.session_state.risk_assessments = {}

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📊 Calculator",
    "🔄 Comparison",
    "💎 Pricing Tiers",
    "🌍 Multi-Currency",
    "📈 Advanced Analysis",
    "☎️ Contact Center",
    "⚠️ RISK ASSESSMENT",
    "🎯 Decision Dashboard",
    "💹 ROI & Break-Even",
    "⚙️ Customization"
])

# ==================== TAB 1: CALCULATOR ====================
with tab1:
    st.header("📊 Hybrid Flexibility Calculator")
    
    col_proj, col_info, col_save = st.columns([2, 2, 2])
    with col_proj:
        project = st.selectbox("🎯 Select Project", list(PROJECTS.keys()))
        project_info = PROJECTS[project]
    
    with col_info:
        st.write(f"**{project_info['color']} {project}**")
        st.caption(project_info['description'])
    
    with col_save:
        scenario_name = st.text_input("Scenario Name", value=f"{project}_Scenario", key="scenario_name_main")
    
    st.markdown("---")
    
    st.subheader("🎯 SECTION 1: Core Pricing Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        region = st.selectbox("Region/Geography", project_info["regions"], key="region")
    with col2:
        fte = st.slider("Number of Agents/FTEs", 10, 2000, 100, step=10, key="fte")
    with col3:
        delivery_model = st.selectbox("Delivery Model", list(project_info["delivery_models"].keys()), key="delivery")
    with col4:
        capability = st.selectbox("Capability/Service Type", list(project_info["capabilities"].keys()), key="capability")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        complexity = st.selectbox("Complexity Level", list(project_info["complexity_multipliers"].keys()), key="complexity")
    with col2:
        channel = st.selectbox("Primary Channel", list(project_info["channels"].keys()), key="channel")
    with col3:
        years = st.slider("Contract Duration (Years)", 1, 10, 3, key="years")
    with col4:
        currency = st.selectbox("Currency", list(CURRENCIES.keys()), key="currency")
    
    st.markdown("---")
    
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
    
    if project == "BCBS Telesales":
        st.markdown("---")
        st.subheader("☎️ SECTION 6: Contact Center Specific Factors")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calls_per_hour = st.slider("Avg Calls/Hour", 4, 20, 8, key="calls_per_hour")
        with col2:
            handle_time_min = st.slider("Avg Handle Time (min)", 2, 30, 5, key="handle_time")
        with col3:
            qa_level = st.slider("QA Score Target (%)", 85, 99, 95, key="qa_level")
        with col4:
            adherence_pct = st.slider("Schedule Adherence (%)", 75, 98, 90, key="adherence")
        
        cc_enabled = True
    else:
        calls_per_hour = 0
        handle_time_min = 0
        qa_level = 95
        adherence_pct = 90
        cc_enabled = False
    
    st.markdown("---")
    
    # ==================== CALCULATIONS ====================
    
    base_annual_cost = project_info["base_costs"][region]
    complexity_mult = project_info["complexity_multipliers"][complexity]
    delivery_mult = project_info["delivery_models"][delivery_model]
    channel_mult = project_info["channels"][channel]
    client_mult = CLIENT_TYPES[client_type]
    sla_mult = SLA_LEVELS[sla_level]
    support_mult = SUPPORT_MODELS[support_model]
    
    cost_per_fte = base_annual_cost * complexity_mult * delivery_mult * channel_mult * client_mult * sla_mult * support_mult
    
    if cc_enabled:
        adherence_mult = adherence_pct / 100
        cost_per_fte = cost_per_fte * adherence_mult
    
    salary = cost_per_fte * 0.60
    benefits = cost_per_fte * 0.12
    overhead = cost_per_fte * 0.15
    tools_tech = cost_per_fte * 0.08
    base_training = cost_per_fte * 0.05
    
    final_training = base_training * training_depth
    
    onboarding = salary * (onboarding_cost_pct / 100)
    compliance = (salary + benefits + overhead + tools_tech + final_training) * (compliance_cost / 100)
    travel = salary * (travel_cost_pct / 100)
    insurance_add = salary * (insurance_cost_pct / 100)
    mgmt_overhead = salary * (management_overhead / 100)
    quality_cost = (salary + benefits + overhead + tools_tech + final_training) * quality_multiplier
    qa_cost = (salary + benefits) * (100 - qa_level) / 100 * 0.1 if cc_enabled else 0
    
    total_cost_per_fte = (salary + benefits + overhead + tools_tech + final_training + 
                          compliance + travel + insurance_add + mgmt_overhead + qa_cost)
    
    year1_adjustments = (ramp_m1_bonus + ramp_m4_bonus + ramp_m7_bonus) / 100 * salary * fte
    
    retention_cost = salary * (retention_bonus / 100) * fte
    performance_cost = salary * (performance_bonus / 100) * fte
    skill_cost = salary * (skill_premium / 100) * fte
    cert_cost = salary * (certification_cost / 100) * fte
    
    total_fte_cost = total_cost_per_fte * fte
    
    attrition_rate = ATTRITION_RATES[attrition]
    additional_attrition_cost = total_fte_cost * attrition_rate
    
    total_operational_cost = total_fte_cost + additional_attrition_cost
    
    year1_cost = total_operational_cost + year1_adjustments + retention_cost + performance_cost + skill_cost + cert_cost
    
    discount_factor = (1 + discount_markup / 100) * (1 - volume_discount / 100) * (1 - long_term_discount / 100)
    year1_cost_adjusted = year1_cost * discount_factor
    
    if margin_override > 0:
        margin_target = margin_override / 100
    else:
        margin_target = project_info["capabilities"][capability]
        if pricing_tier:
            tier_margin = PRICING_TIERS[pricing_tier]["margin"]
            margin_target = tier_margin
    
    acv = year1_cost_adjusted / (1 - margin_target)
    tcv = acv * years
    margin_dollars = acv - year1_cost_adjusted
    margin_pct = (margin_dollars / acv) * 100
    
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
            "---",
            "SUBTOTAL (per FTE)",
            "Total FTEs",
            "Annual Cost (All FTEs)",
            "Attrition Cost",
            "Retention Bonus (Y1)",
            "Performance Bonus (Y1)",
            "Skills Premium (Y1)",
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
            "—",
            f"{currency_symbol}{total_cost_per_fte*currency_factor:,.0f}",
            f"{fte}",
            f"{currency_symbol}{total_fte_cost*currency_factor:,.0f}",
            f"{currency_symbol}{additional_attrition_cost*currency_factor:,.0f}",
            f"{currency_symbol}{retention_cost*currency_factor:,.0f}",
            f"{currency_symbol}{performance_cost*currency_factor:,.0f}",
            f"{currency_symbol}{skill_cost*currency_factor:,.0f}",
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
    
    col1, col2, col3 = st.columns(3)
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
                "acv": acv_converted,
                "tcv": tcv_converted,
                "margin_pct": margin_pct,
                "year1_cost": year1_cost_adjusted / currency_factor,
                "total_fte_cost": total_fte_cost / currency_factor
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
    
    with col3:
        st.caption(f"✅ Saved Scenarios: {len(st.session_state.scenarios)}")


# ==================== TAB 2: COMPARISON ====================
with tab2:
    st.header("🔄 Multi-Project Scenario Comparison")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved yet. Create scenarios in the Calculator tab first!")
    else:
        scenarios_list = list(st.session_state.scenarios.keys())
        selected = st.multiselect("Select scenarios to compare:", scenarios_list, max_selections=8)
        
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
                    "ACV": f"{s['currency']}{s['acv']:,.0f}",
                    "TCV": f"{s['currency']}{s['tcv']:,.0f}",
                    "Margin %": f"{s['margin_pct']:.1f}%"
                })
            
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
            
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
        
        st.write("**FTE Sensitivity:**")
        fte_scenarios = [base_data["fte"] * 0.8, base_data["fte"], base_data["fte"] * 1.2]
        
        whatif_results = []
        for fte_var in fte_scenarios:
            factor = fte_var / base_data["fte"]
            whatif_results.append({
                "FTE Scenario": f"{int(fte_var)}",
                "Change": f"{(factor-1)*100:+.0f}%",
                "Est. ACV": f"${base_data['acv'] * factor:,.0f}",
                "Est. Margin %": f"{base_data['margin_pct']:.1f}%"
            })
        
        st.dataframe(pd.DataFrame(whatif_results), use_container_width=True)
    else:
        st.warning("Create a scenario first to enable What-If analysis")


# ==================== TAB 6: CONTACT CENTER ANALYTICS ====================
with tab6:
    st.header("☎️ Contact Center Analytics (BCBS)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        agents = st.slider("Number of Agents:", 10, 500, 100, key="cc_agents")
        calls_per_day = st.slider("Avg Calls/Agent/Day:", 20, 100, 60, key="cc_calls_day")
    
    with col2:
        avg_handle_time = st.slider("Avg Handle Time (min):", 2, 30, 5, key="cc_handle")
        work_days_year = st.slider("Working Days/Year:", 200, 260, 250, key="cc_workdays")
    
    with col3:
        service_level = st.slider("Service Level Target (%):", 70, 99, 85, key="cc_sl")
        shrinkage_pct = st.slider("Shrinkage (%)", 0, 30, 15, key="cc_shrinkage")
    
    total_calls_year = agents * calls_per_day * work_days_year
    total_minutes = total_calls_year * avg_handle_time
    total_hours = total_minutes / 60
    productive_fte = total_hours / (8 * work_days_year)
    required_fte = productive_fte / (1 - shrinkage_pct / 100)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calls/Year", f"{total_calls_year:,.0f}")
    with col2:
        st.metric("Total AHT Hours", f"{total_hours:,.0f}")
    with col3:
        st.metric("Productive FTE", f"{productive_fte:,.0f}")
    with col4:
        st.metric("Required FTE (w/ Shrinkage)", f"{required_fte:,.0f}")


# ==================== TAB 7: RISK ASSESSMENT ====================
with tab7:
    st.header("⚠️ RISK ASSESSMENT DASHBOARD")
    st.markdown("**Comprehensive Risk Analysis for All Deals**")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved yet. Create scenarios in the Calculator tab first!")
    else:
        risk_scenario = st.selectbox("Select Scenario for Risk Assessment:", list(st.session_state.scenarios.keys()), key="risk_scenario")
        scenario_data = st.session_state.scenarios[risk_scenario]
        
        st.markdown("---")
        st.subheader("📊 Risk Scoring Input")
        
        # Operational Risk
        with st.expander("🏭 OPERATIONAL RISK", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                attrition_risk = st.selectbox("Attrition Risk:", list(RISK_CATEGORIES["Operational Risk"]["Attrition Risk"].keys()), key="op_attrition")
                quality_risk = st.selectbox("Quality Risk:", list(RISK_CATEGORIES["Operational Risk"]["Quality Risk"].keys()), key="op_quality")
            with col2:
                compliance_risk = st.selectbox("Compliance Risk:", list(RISK_CATEGORIES["Operational Risk"]["Compliance Risk"].keys()), key="op_compliance")
                tech_risk = st.selectbox("Technology Risk:", list(RISK_CATEGORIES["Operational Risk"]["Technology Risk"].keys()), key="op_tech")
            
            op_score = (
                RISK_CATEGORIES["Operational Risk"]["Attrition Risk"][attrition_risk] +
                RISK_CATEGORIES["Operational Risk"]["Quality Risk"][quality_risk] +
                RISK_CATEGORIES["Operational Risk"]["Compliance Risk"][compliance_risk] +
                RISK_CATEGORIES["Operational Risk"]["Technology Risk"][tech_risk]
            ) / 4
            
            st.metric("Operational Risk Score", f"{op_score:.2%}")
        
        # Financial Risk
        with st.expander("💰 FINANCIAL RISK"):
            col1, col2 = st.columns(2)
            with col1:
                currency_risk = st.selectbox("Currency Risk:", list(RISK_CATEGORIES["Financial Risk"]["Currency Risk"].keys()), key="fin_currency")
                volume_risk = st.selectbox("Volume Risk:", list(RISK_CATEGORIES["Financial Risk"]["Volume Risk"].keys()), key="fin_volume")
            with col2:
                inflation_risk = st.selectbox("Cost Inflation Risk:", list(RISK_CATEGORIES["Financial Risk"]["Cost Inflation Risk"].keys()), key="fin_inflation")
                margin_risk = st.selectbox("Margin Compression Risk:", list(RISK_CATEGORIES["Financial Risk"]["Margin Compression Risk"].keys()), key="fin_margin")
            
            fin_score = (
                RISK_CATEGORIES["Financial Risk"]["Currency Risk"][currency_risk] +
                RISK_CATEGORIES["Financial Risk"]["Volume Risk"][volume_risk] +
                RISK_CATEGORIES["Financial Risk"]["Cost Inflation Risk"][inflation_risk] +
                RISK_CATEGORIES["Financial Risk"]["Margin Compression Risk"][margin_risk]
            ) / 4
            
            st.metric("Financial Risk Score", f"{fin_score:.2%}")
        
        # Client Risk
        with st.expander("🤝 CLIENT RISK"):
            col1, col2 = st.columns(2)
            with col1:
                concentration_risk = st.selectbox("Client Concentration:", list(RISK_CATEGORIES["Client Risk"]["Client Concentration"].keys()), key="client_concentration")
                renewal_risk = st.selectbox("Contract Renewal Risk:", list(RISK_CATEGORIES["Client Risk"]["Contract Renewal Risk"].keys()), key="client_renewal")
            with col2:
                scope_risk = st.selectbox("Scope Creep Risk:", list(RISK_CATEGORIES["Client Risk"]["Scope Creep Risk"].keys()), key="client_scope")
                sla_risk = st.selectbox("SLA Non-Performance:", list(RISK_CATEGORIES["Client Risk"]["SLA Non-Performance"].keys()), key="client_sla")
            
            client_score = (
                RISK_CATEGORIES["Client Risk"]["Client Concentration"][concentration_risk] +
                RISK_CATEGORIES["Client Risk"]["Contract Renewal Risk"][renewal_risk] +
                RISK_CATEGORIES["Client Risk"]["Scope Creep Risk"][scope_risk] +
                RISK_CATEGORIES["Client Risk"]["SLA Non-Performance"][sla_risk]
            ) / 4
            
            st.metric("Client Risk Score", f"{client_score:.2%}")
        
        # Market Risk
        with st.expander("📈 MARKET RISK"):
            col1, col2 = st.columns(2)
            with col1:
                volatility_risk = st.selectbox("Market Volatility:", list(RISK_CATEGORIES["Market Risk"]["Market Volatility"].keys()), key="market_volatility")
                competition_risk = st.selectbox("Competition Risk:", list(RISK_CATEGORIES["Market Risk"]["Competition Risk"].keys()), key="market_competition")
            with col2:
                regulatory_risk = st.selectbox("Regulatory Risk:", list(RISK_CATEGORIES["Market Risk"]["Regulatory Risk"].keys()), key="market_regulatory")
                geopolitical_risk = st.selectbox("Geopolitical Risk:", list(RISK_CATEGORIES["Market Risk"]["Geopolitical Risk"].keys()), key="market_geopolitical")
            
            market_score = (
                RISK_CATEGORIES["Market Risk"]["Market Volatility"][volatility_risk] +
                RISK_CATEGORIES["Market Risk"]["Competition Risk"][competition_risk] +
                RISK_CATEGORIES["Market Risk"]["Regulatory Risk"][regulatory_risk] +
                RISK_CATEGORIES["Market Risk"]["Geopolitical Risk"][geopolitical_risk]
            ) / 4
            
            st.metric("Market Risk Score", f"{market_score:.2%}")
        
        st.markdown("---")
        
        # Overall Risk Assessment
        overall_risk = (op_score + fin_score + client_score + market_score) / 4
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("OVERALL RISK SCORE", f"{overall_risk:.2%}")
        
        with col2:
            if overall_risk < 0.05:
                st.success("🟢 **LOW RISK**")
            elif overall_risk < 0.10:
                st.info("🟡 **MODERATE RISK**")
            else:
                st.error("🔴 **HIGH RISK**")
        
        with col3:
            # Risk-adjusted margin
            risk_adjustment = overall_risk * 100
            risk_adjusted_margin = scenario_data['margin_pct'] - risk_adjustment
            st.metric("Risk-Adjusted Margin", f"{risk_adjusted_margin:.1f}%", delta=f"-{risk_adjustment:.1f}%")
        
        st.markdown("---")
        
        # Risk Heatmap
        st.subheader("🔥 Risk Heatmap")
        
        risk_matrix = pd.DataFrame({
            "Risk Category": ["Operational", "Financial", "Client", "Market"],
            "Risk Score": [op_score * 100, fin_score * 100, client_score * 100, market_score * 100]
        })
        
        fig, ax = plt.subplots(figsize=(10, 4))
        colors = ['green' if x < 5 else 'yellow' if x < 10 else 'red' for x in risk_matrix["Risk Score"]]
        bars = ax.barh(risk_matrix["Risk Category"], risk_matrix["Risk Score"], color=colors)
        ax.set_xlabel("Risk Score (%)")
        ax.set_title("Risk Assessment by Category")
        ax.set_xlim(0, 20)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                   f'{width:.1f}%', ha='left', va='center')
        
        st.pyplot(fig)
        
        st.markdown("---")
        
        # Mitigation Strategies
        st.subheader("🛡️ Risk Mitigation Strategies")
        
        mitigation = {
            "Attrition Risk": "Increase retention bonuses, improve training programs, career development paths",
            "Quality Risk": "Implement QA processes, staff training, performance monitoring systems",
            "Compliance Risk": "Regular audits, documentation, dedicated compliance team, regulatory tracking",
            "Technology Risk": "Technology refreshes, vendor management, disaster recovery plans",
            "Currency Risk": "Currency hedging, multi-currency contracts, local partnerships",
            "Volume Risk": "Flexible staffing models, scalable infrastructure, volume commitments",
            "Cost Inflation Risk": "Fixed-cost contracts, cost-sharing agreements, efficiency improvements",
            "Margin Compression Risk": "Premium positioning, value-add services, cost optimization",
            "Client Concentration": "Diversify client base, expand service offerings, long-term contracts",
            "Contract Renewal Risk": "Strong relationship management, continuous value delivery, early renewal talks",
            "Scope Creep Risk": "Clear SLAs, change control procedures, documented deliverables",
            "SLA Non-Performance": "Buffer capacity, performance monitoring, escalation procedures"
        }
        
        for risk_type, strategy in mitigation.items():
            st.write(f"**{risk_type}:** {strategy}")
        
        # Save risk assessment
        if st.button("💾 Save Risk Assessment"):
            st.session_state.risk_assessments[risk_scenario] = {
                "timestamp": datetime.now().isoformat(),
                "operational_risk": op_score,
                "financial_risk": fin_score,
                "client_risk": client_score,
                "market_risk": market_score,
                "overall_risk": overall_risk,
                "risk_adjusted_margin": risk_adjusted_margin
            }
            st.success(f"✅ Risk Assessment Saved for {risk_scenario}")


# ==================== TAB 8: DECISION DASHBOARD ====================
with tab8:
    st.header("🎯 Decision Support Dashboard")
    st.markdown("**AI-Powered Decision Making Tools**")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved. Create scenarios in the Calculator tab first!")
    else:
        st.subheader("📊 Deal Scoring Matrix")
        
        decision_scenario = st.selectbox("Select Scenario:", list(st.session_state.scenarios.keys()), key="decision_scenario")
        scenario = st.session_state.scenarios[decision_scenario]
        
        # Scoring criteria
        st.write("**Score Each Criterion (1-10, where 10 is excellent)**")
        
        col1, col2 = st.columns(2)
        with col1:
            margin_score = st.slider("Margin Attractiveness", 1, 10, 7, key="margin_score")
            growth_score = st.slider("Growth Potential", 1, 10, 6, key="growth_score")
            client_score_input = st.slider("Client Quality", 1, 10, 7, key="client_quality_score")
            stability_score = st.slider("Market Stability", 1, 10, 6, key="stability_score")
        
        with col2:
            risk_score_input = st.slider("Risk Level (1=High Risk, 10=Low Risk)", 1, 10, 5, key="risk_input")
            execution_score = st.slider("Execution Capability", 1, 10, 7, key="execution_score")
            scalability_score = st.slider("Scalability", 1, 10, 6, key="scalability_score")
            strategic_fit = st.slider("Strategic Alignment", 1, 10, 7, key="strategic_fit")
        
        # Calculate weighted score
        weights = {
            "Margin": 0.20,
            "Growth": 0.15,
            "Client Quality": 0.15,
            "Stability": 0.10,
            "Risk": 0.15,
            "Execution": 0.10,
            "Scalability": 0.10,
            "Strategic": 0.05
        }
        
        weighted_score = (
            margin_score * weights["Margin"] +
            growth_score * weights["Growth"] +
            client_score_input * weights["Client Quality"] +
            stability_score * weights["Stability"] +
            risk_score_input * weights["Risk"] +
            execution_score * weights["Execution"] +
            scalability_score * weights["Scalability"] +
            strategic_fit * weights["Strategic"]
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Weighted Decision Score", f"{weighted_score:.1f}/10")
        with col2:
            if weighted_score >= 8:
                st.success("🟢 STRONG BUY")
            elif weighted_score >= 6.5:
                st.info("🟡 BUY")
            else:
                st.error("🔴 PASS/RECONSIDER")
        with col3:
            st.metric("Margin (%)", f"{scenario['margin_pct']:.1f}%")
        
        st.markdown("---")
        
        # Criteria Breakdown
        st.subheader("📋 Scoring Breakdown")
        
        breakdown = pd.DataFrame({
            "Criteria": ["Margin", "Growth", "Client Quality", "Stability", "Risk", "Execution", "Scalability", "Strategic"],
            "Score": [margin_score, growth_score, client_score_input, stability_score, risk_score_input, execution_score, scalability_score, strategic_fit],
            "Weight": [weights["Margin"]*100, weights["Growth"]*100, weights["Client Quality"]*100, weights["Stability"]*100, weights["Risk"]*100, weights["Execution"]*100, weights["Scalability"]*100, weights["Strategic"]*100],
            "Weighted Score": [
                margin_score * weights["Margin"],
                growth_score * weights["Growth"],
                client_score_input * weights["Client Quality"],
                stability_score * weights["Stability"],
                risk_score_input * weights["Risk"],
                execution_score * weights["Execution"],
                scalability_score * weights["Scalability"],
                strategic_fit * weights["Strategic"]
            ]
        })
        
        st.dataframe(breakdown, use_container_width=True)
        
        # Visualization
        fig, ax = plt.subplots(figsize=(12, 5))
        criteria = breakdown["Criteria"]
        scores = breakdown["Score"]
        colors = ['green' if x >= 7 else 'yellow' if x >= 5 else 'red' for x in scores]
        
        bars = ax.bar(criteria, scores, color=colors, alpha=0.7, edgecolor='black')
        ax.set_ylabel("Score (1-10)")
        ax.set_title(f"Deal Scoring Matrix - Overall Score: {weighted_score:.1f}/10")
        ax.set_ylim(0, 10)
        ax.axhline(y=7, color='green', linestyle='--', alpha=0.5, label='Excellent (7+)')
        ax.axhline(y=5, color='yellow', linestyle='--', alpha=0.5, label='Good (5-7)')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{int(height)}', ha='center', va='bottom')
        
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)


# ==================== TAB 9: ROI & BREAK-EVEN ====================
with tab9:
    st.header("💹 ROI & Break-Even Analysis")
    
    if len(st.session_state.scenarios) == 0:
        st.warning("⚠️ No scenarios saved. Create scenarios in the Calculator tab first!")
    else:
        roi_scenario = st.selectbox("Select Scenario:", list(st.session_state.scenarios.keys()), key="roi_scenario")
        scenario = st.session_state.scenarios[roi_scenario]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            investment = st.number_input("Initial Investment (USD):", value=100000, step=10000, key="initial_investment")
        with col2:
            discount_rate = st.slider("Discount Rate (%)", 0, 20, 10, key="discount_rate")
        with col3:
            payback_years = st.slider("Analysis Period (Years)", 1, 10, 5, key="analysis_period")
        
        # Calculations
        annual_profit = scenario['acv'] - scenario['year1_cost']
        
        # Break-even calculation
        breakeven_months = (investment / annual_profit * 12) if annual_profit > 0 else float('inf')
        breakeven_years = breakeven_months / 12
        
        # ROI Calculation
        total_profit = annual_profit * payback_years - investment
        roi_pct = (total_profit / investment * 100) if investment > 0 else 0
        
        # NPV Calculation
        npv = -investment
        for year in range(1, int(payback_years) + 1):
            npv += annual_profit / ((1 + discount_rate / 100) ** year)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Annual Profit", f"${annual_profit:,.0f}")
        with col2:
            st.metric("Break-Even (Months)", f"{breakeven_months:.1f}" if breakeven_months != float('inf') else "N/A")
        with col3:
            st.metric(f"ROI ({payback_years:.0f}yr)", f"{roi_pct:.1f}%")
        with col4:
            st.metric(f"NPV ({discount_rate}% discount)", f"${npv:,.0f}")
        
        st.markdown("---")
        
        # ROI Timeline
        st.subheader("📈 ROI Timeline")
        
        timeline_data = []
        cumulative_profit = -investment
        
        for year in range(1, int(payback_years) + 1):
            year_profit = annual_profit
            cumulative_profit += year_profit
            roi = (cumulative_profit / investment * 100) if investment > 0 else 0
            
            timeline_data.append({
                "Year": year,
                "Annual Profit": f"${year_profit:,.0f}",
                "Cumulative Profit": f"${cumulative_profit:,.0f}",
                "ROI (%)": f"{roi:.1f}%"
            })
        
        st.dataframe(pd.DataFrame(timeline_data), use_container_width=True)
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Profit chart
        years = list(range(1, int(payback_years) + 1))
        cumulative_profits = [-investment]
        for year in years:
            cumulative_profits.append(cumulative_profits[-1] + annual_profit)
        
        ax1.plot(list(range(0, int(payback_years) + 1)), cumulative_profits, marker='o', linewidth=2, markersize=8)
        ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax1.fill_between(list(range(0, int(payback_years) + 1)), cumulative_profits, 0, alpha=0.3)
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Cumulative Profit ($)")
        ax1.set_title("Cumulative Profit Over Time")
        ax1.grid(True, alpha=0.3)
        
        # ROI chart
        rois = [(cumulative_profits[i] / investment * 100) for i in range(len(cumulative_profits))]
        ax2.plot(list(range(0, int(payback_years) + 1)), rois, marker='s', linewidth=2, markersize=8, color='green')
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax2.set_xlabel("Year")
        ax2.set_ylabel("ROI (%)")
        ax2.set_title("Return on Investment Over Time")
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)


# ==================== TAB 10: CUSTOMIZATION ====================
with tab10:
    st.header("⚙️ Customization & Extensibility")
    
    st.subheader("➕ Add New Project")
    
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
                    "color": "🟣",
                    "icon": "💡",
                    "description": "Custom Project",
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
    
    st.subheader("📚 Saved Custom Projects")
    if st.session_state.saved_projects:
        for proj_name, proj_data in st.session_state.saved_projects.items():
            st.write(f"**{proj_name}** - Regions: {', '.join(proj_data['regions'])}")
    else:
        st.info("No custom projects yet")


# ==================== FOOTER ====================
st.markdown("---")
st.success("✅ **Enterprise Pricing Calculator - Decision Intelligence Edition**")
st.caption("🔵 LBG | 🟢 Palmetto | 🟡 BCBS | ⚠️ Risk Assessment | 🎯 Decision Support | 💹 ROI Analysis")
st.caption(f"📊 Scenarios: {len(st.session_state.scenarios)} | Risk Assessments: {len(st.session_state.risk_assessments)} | Custom Projects: {len(st.session_state.saved_projects)}")
