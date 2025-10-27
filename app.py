import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Expansion Tracker", layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("projects.csv")
    df.columns = df.columns.str.strip().str.lower()
    ###
    if "investment" in df.columns:
        df["investment"] = pd.to_numeric(df["investment"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    ###
    return df

df = load_data()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("Filters")

# --- Search by company name
search_term = st.sidebar.text_input("🔍 Search by company name")

# --- Region filter
host_country = sorted([r for r in df["host_country"].dropna().unique()])
selected_regions = st.sidebar.multiselect("🌏 Select Region(s)", host_country)

# --- Industry filter
sectors = sorted([i for i in df["sector"].dropna().unique()])
selected_industries = st.sidebar.multiselect("🏭 Select Industry", sectors)

# --- Apply filters
filtered_df = df.copy()
if search_term:
    filtered_df = filtered_df[filtered_df["company_name"].str.contains(search_term, case=False, na=False)]
if selected_regions:
    filtered_df = filtered_df[filtered_df["host_country"].isin(selected_regions)]
if selected_industries:
    filtered_df = filtered_df[filtered_df["sector"].isin(selected_industries)]

# -------------------- DASHBOARD HEADER --------------------
st.title("🌐 Global Expansion Tracker")
st.markdown("Monitor Chinese companies’ global investment, factory, and R&D expansion projects.")

# -------------------- METRICS --------------------
col1, col2, col3, col4 = st.columns(4)

tracked_companies = df["company_name"].nunique()
active_projects = len(df)
#avg_investment = df["investment"].mean() if "investment" in df.columns else 0
#recent_projects = df[df["date"] >= (pd.Timestamp.now().date() - pd.Timedelta(days=7))] if "date" in df.columns else pd.DataFrame()

with col1:
    st.metric("Tracked Companies", tracked_companies)
with col2:
    st.metric("Active Projects", active_projects)
###
#with col3:
#    st.metric("Avg Investment", f"${avg_investment:,.0f}M" if avg_investment else "N/A")
#with col4:
#    st.metric("Recent (7d)", len(recent_projects))
###

st.divider()

# -------------------- MAIN LAYOUT --------------------
left_col, right_col = st.columns([2.5, 1.5], gap="large")

with left_col:
    st.subheader("📋 Project List")

    if filtered_df.empty:
        st.warning("No projects found for your search/filter.")
    else:
        for _, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"**{row['company_name']}** — {row.get('host_country', 'N/A')} • {row.get('sector', 'N/A')}")
                st.caption(f"📅 {row.get('date', 'N/A')}")
                st.write(row.get("summary_of_project", "No summary available."))
                st.markdown(f"💰 **Investment:** {row.get('investment_amount', 'N/A')} M")
                st.divider()

with right_col:
    st.subheader("📊 Regional Overview")
    if not filtered_df.empty and "host_country" in filtered_df.columns:
        chart_data = filtered_df.groupby("host_country").size().reset_index(name="Projects")
        fig = px.bar(chart_data, x="Projects", y="region", orientation="h", title="Projects by Region")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for chart.")
