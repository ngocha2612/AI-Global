import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Go-Global Customer Intelligence", layout="wide")

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    df = pd.read_csv("projects.csv")
    # Normalize columns (you can rename based on your CSV headers)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Ensure date and investment types
    #if "date" in df.columns:
        #df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    #if "investment_amount" in df.columns:
        #df["investment_amount"] = pd.to_numeric(df["investment_amount"], errors="coerce")
    return df.dropna(subset=["company_name", "host_country"])

df = load_data()

# ===================== HEADER =====================
st.markdown("""
    <style>
        .main-title {font-size: 30px; font-weight: 700; color: #1E293B;}
        .subtitle {font-size: 16px; color: #475569; margin-bottom: 1.5rem;}
        .metric-card {padding: 1rem; background: #F8FAFC; border-radius: 1rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
        .project-card {background: white; border-radius: 1rem; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
        .project-title {font-size: 18px; font-weight: 600; color: #0f172a;}
        .project-summary {color: #475569; margin-top: 0.2rem;}
        .tag {display: inline-block; padding: 0.25rem 0.6rem; background: #e2e8f0; border-radius: 9999px; font-size: 12px; margin-right: 5px;}
        .right-panel {background: #F8FAFC; padding: 1rem; border-radius: 1rem;}
        .section-title {font-weight: 600; color: #1e293b; font-size: 16px; margin-bottom: 0.8rem;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown('<div class="main-title">Go-Global Customer Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Decision Support System</div>', unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align:right'><button>📤 Export Report</button> <button>🔄 Sync Data</button></div>", unsafe_allow_html=True)

st.markdown("---")

# ===================== METRICS =====================
tracked_customers = df["company_name"].nunique()
active_opps = len(df)
##avg_investment = df["investment_amount"].mean() if "investment_amount" in df.columns else 0
##recent_projects = df[df["date"] >= (datetime.now().date() - timedelta(days=7))] if "date" in df.columns else []

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tracked Customers", tracked_customers)
col2.metric("Active Opportunities", active_opps)
##col3.metric("Avg Investment", f"${avg_investment:,.0f}M")
##col4.metric("Recent Projects (7d)", len(recent_projects))

st.markdown("")

# ===================== LAYOUT =====================
left_col, right_col = st.columns([0.65, 0.35])

# ========== LEFT PANEL: PROJECT CARDS ==========
with left_col:
    st.markdown("### Active Projects")

    # Optional filters
    # regions = st.multiselect("Filter by Region", sorted(df["region"].dropna().unique()))
    # industries = st.multiselect("Filter by Industry", sorted(df["industry"].dropna().unique()) if "industry" in df.columns else [])
    host_country = st.multiselect("Filter by Region", sorted(df["host_country"].dropna().unique()))
    sector = st.multiselect("Filter by Industry", sorted(df["sector"].dropna().unique()) if "sector" in df.columns else [])
    
    filtered = df.copy()
    if host_country:
        filtered = filtered[filtered["host_country"].isin(host_country)]
    if sector and "sector" in df.columns:
        filtered = filtered[filtered["sector"].isin(sector)]

    # Display cards
    for _, row in filtered.iterrows():
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">{row['company_name']}</div>
            <div class="project-summary">{row.get('summary_of_project', '')}</div>
            <div style="margin-top: 0.5rem;">
                <span class="tag">{row.get('host_country', '')}</span>
                <span class="tag">{row.get('sector', '')}</span>
                <span class="tag">${row.get('investment_amount', 0):,.0f}M</span>
                <span class="tag">{row.get('date', '')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== RIGHT PANEL ==========
with right_col:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Regional Overview</div>', unsafe_allow_html=True)

    # Chart: average investment by region
    ###
    if "region" in df.columns:
        chart_data = df.groupby("region")["investment"].sum().reset_index()
        fig = px.bar(chart_data, x="region", y="investment", color="region",
                     labels={"investment": "Total Investment (M USD)", "region": "Region"},
                     title=None)
        fig.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    ###
    # Recent insights
    ###
    st.markdown('<div class="section-title">🕒 Recent Insights</div>', unsafe_allow_html=True)
    if "date" in df.columns:
        recent = df.sort_values("date", ascending=False).head(5)
        for _, r in recent.iterrows():
            st.markdown(f"- **{r['company_name']}** — {r['summary'][:70]}...  *(updated {r['date']})*")
    ###
    st.markdown('<div class="section-title">⚙️ Quick Actions</div>', unsafe_allow_html=True)
    st.button("Generate Weekly Report")
    st.button("Schedule Team Review")
    st.button("Export Customer Insights")

    st.markdown("</div>", unsafe_allow_html=True)
