import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Expansion Tracker", layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("projects.csv")
    df.columns = df.columns.str.strip().str.lower()
    if "investment_amount" in df.columns:
        df["investment_amount"] = pd.to_numeric(df["investment_amount"], errors="coerce")
    #if "date" in df.columns:
        #df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    df = df[(df['host_country'] != "China") & (df["host_country"] != "Hong Kong") & (df["host_country"].isna()==False)]
    df = df[df["project_type"].isna()==False]
    return df

df = load_data()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("Filters")

search_term = st.sidebar.text_input("🔍 Search by company name")

host_countries = sorted(df["host_country"].dropna().unique()) if "host_country" in df.columns else []
selected_countries = st.sidebar.multiselect("🌏 Select Host Country", host_countries)

sectors = sorted(df["sector"].dropna().unique()) if "sector" in df.columns else []
selected_sectors = st.sidebar.multiselect("🏭 Select Sector", sectors)

# -------------------- APPLY FILTERS --------------------
filtered_df = df.copy()
if search_term:
    filtered_df = filtered_df[filtered_df["company_name"].str.contains(search_term, case=False, na=False)]
if selected_countries:
    filtered_df = filtered_df[filtered_df["host_country"].isin(selected_countries)]
if selected_sectors:
    filtered_df = filtered_df[filtered_df["sector"].isin(selected_sectors)]

# -------------------- DASHBOARD HEADER --------------------
st.title("🌐 Global Expansion Tracker")
st.markdown("Monitor Chinese companies’ global investment, factory, and R&D expansion projects.")

# -------------------- METRICS --------------------
col1, col2, col3, col4 = st.columns(4)

tracked_companies = df["company_main"].nunique() if "company_main" in df.columns else df["company_name"].nunique()
active_projects = len(df)

with col1:
    st.metric("Tracked Companies", tracked_companies)
with col2:
    st.metric("Active Projects", active_projects)

st.divider()

# -------------------- PAGINATION SETUP --------------------
items_per_page = 5  # Number of project cards per page
total_projects = len(filtered_df)
total_pages = max(1, (total_projects + items_per_page - 1) // items_per_page)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# Slice the dataframe for the current page
start_idx = (st.session_state.current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_df = filtered_df.iloc[start_idx:end_idx]

# -------------------- MAIN LAYOUT --------------------
left_col, right_col = st.columns([2.5, 1.5], gap="large")

with left_col:
    st.header("📋 Project List")

    if page_df.empty:
        st.warning("No projects found for your search/filter.")
    else:
        for _, row in page_df.iterrows():
            with st.container():
                st.subheader(f"**{row['company_name']}**")
                st.markdown(f"📍 {row.get('host_country', 'N/A')} • {row.get('sector', 'N/A')}")
                st.markdown(f"**Project Scope:** {row.get('project_type', 'N/A')}")
                st.write(row.get("summary_of_project", "No summary available."))
                st.markdown(f"📅 **Project Stage:** {row.get('project_stage', 'N/A')}")
                st.markdown(f"💰 **Investment:** {row.get('investment_amount', 'N/A')}")
                st.caption(f"Last updated: {row.get('date', 'N/A')}")
                st.divider()

        # -------------------- PAGINATION CONTROLS (MOVED TO END) --------------------
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.session_state.current_page > 1:
                if st.button("⬅️ Previous"):
                    st.session_state.current_page -= 1
                    st.rerun()
        with col_page:
            st.markdown(
                f"<p style='text-align:center;'>Page {st.session_state.current_page} of {total_pages}</p>",
                unsafe_allow_html=True,
            )
        with col_next:
            if st.session_state.current_page < total_pages:
                if st.button("Next ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

with right_col:
    st.subheader("📊 Regional Overview")
    if not filtered_df.empty and "host_country" in filtered_df.columns:
        chart_data = filtered_df.groupby("host_country").size().reset_index(name="Projects")
        fig = px.bar(chart_data, x="Projects", y="host_country", orientation="h", title="Projects by Region")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for chart.")
