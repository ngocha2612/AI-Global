import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Go-Global Customer Intelligence", layout="wide")

# -------------------- STYLES --------------------
st.markdown("""
<style>
/* Header */
.header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.5rem 1rem; border-bottom: 1px solid #eee;
}
.header-title { font-size: 1.6rem; font-weight: 600; color: #222; }
.header-sub { font-size: 0.9rem; color: #777; margin-top: -5px; }
button[data-baseweb="button"] { border-radius: 8px !important; }

/* Metric cards */
.metric-container {
    display: flex; justify-content: space-between; margin: 1rem 0 1.5rem 0;
}
.metric-card {
    flex: 1; background: #fff; border-radius: 12px; padding: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08); margin-right: 1rem;
}
.metric-card:last-child { margin-right: 0; }
.metric-value { font-size: 1.4rem; font-weight: 600; color: #111; }
.metric-label { color: #777; font-size: 0.9rem; }

/* Project cards */
.project-card {
    background: #fff; border-radius: 12px; padding: 1rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 1rem;
}
.project-title { font-weight: 600; font-size: 1.1rem; color: #222; }
.project-meta { color: #666; font-size: 0.9rem; margin-top: -2px; }
.project-summary { margin-top: 0.5rem; font-size: 0.9rem; color: #333; }

/* Sidebar cards */
.sidebar-card {
    background: #fff; border-radius: 12px; padding: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.sidebar-title { font-weight: 600; margin-bottom: 0.8rem; color: #222; }
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
with st.container():
    st.markdown("""
    <div class="header">
        <div>
            <div class="header-title">Go-Global Customer Intelligence</div>
            <div class="header-sub">AI-Powered Decision Support System</div>
        </div>
        <div>
            <button class="css-1cpxqw2 edgvbvh10">Sync Data</button>
            <button class="css-1cpxqw2 edgvbvh10" style="margin-left:8px;">Export Report</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- SAMPLE DATA --------------------
data = [
    {"company_name": "BYD Southeast Asia Holdings", "region": "Southeast Asia", "industry": "Automotive & Manufacturing",
     "summary": "New EV battery plant announced in Thailand – $800M investment", "investment": 800, "date": "2025-10-05"},
    {"company_name": "CATL Europe Battery Innovation", "region": "Europe", "industry": "Energy & Battery Tech",
     "summary": "Expansion of Hungary facility hiring 500+ engineers", "investment": 500, "date": "2025-10-01"},
    {"company_name": "Huawei Middle East Infrastructure", "region": "Middle East", "industry": "Telecom",
     "summary": "5G network rollout delayed due to regulatory review", "investment": 300, "date": "2025-09-28"},
    {"company_name": "SAIC Motor Latin America", "region": "Latin America", "industry": "Automotive & Manufacturing",
     "summary": "Joint venture with local distributor for vehicle assembly", "investment": 120, "date": "2025-10-03"},
    {"company_name": "Longi Solar Africa Expansion", "region": "Africa", "industry": "Renewable Energy",
     "summary": "Solar module production facility in South Africa – Phase 1 complete", "investment": 60, "date": "2025-09-20"}
]
df = pd.DataFrame(data)

# -------------------- METRICS --------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tracked Customers", "50")
with col2:
    st.metric("Active Opportunities", "47")
with col3:
    st.metric("Average Match Score", "81%")
with col4:
    st.metric("Recent Alerts", "8")

# -------------------- MAIN LAYOUT --------------------
left_col, right_col = st.columns([2.3, 1])

# LEFT: PROJECT CARDS
with left_col:
    st.markdown("### Active Projects")
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">{row['company_name']}</div>
            <div class="project-meta">{row['region']} · {row['industry']}</div>
            <div class="project-summary">{row['summary']}</div>
            <div style="margin-top:6px; color:#666; font-size:0.85rem;">
                💰 ${row['investment']}M &nbsp;·&nbsp; 📅 {row['date']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# RIGHT: SIDEBAR PANELS
with right_col:
    # ---- Regional Overview ----
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">Regional Overview</div>', unsafe_allow_html=True)
    region_summary = df.groupby("region")["investment"].sum().reset_index()
    fig = px.bar(region_summary, x="region", y="investment",
                 title="", text_auto=True, height=250)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), xaxis_title=None, yaxis_title="Investment ($M)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Recent Insights ----
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">Recent Insights</div>', unsafe_allow_html=True)
    for i in range(3):
        st.markdown(f"• {df.iloc[i]['company_name']} – update {i+1} days ago")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Quick Actions ----
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-title">Quick Actions</div>
        <button class="css-1cpxqw2 edgvbvh10">Generate Weekly Report</button><br><br>
        <button class="css-1cpxqw2 edgvbvh10">Schedule Team Review</button><br><br>
        <button class="css-1cpxqw2 edgvbvh10">Export Customer Insights</button>
    </div>
    """, unsafe_allow_html=True)
