import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== CONFIG =====================
st.set_page_config(page_title="Global Expansion Tracker", layout="wide")

# ===================== DATA =====================
@st.cache_data
def load_data():
    df = pd.read_csv("projects.csv")
    return df

df = load_data()

# ===================== HEADER =====================
st.title("🌏 Global Expansion Tracker")

# ===================== METRICS =====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Projects", len(df))
col2.metric("Unique Companies", df["company_main"].nunique() if "company_main" in df else 0)
col3.metric("Countries Covered", df["host_country"].nunique() if "host_country" in df else 0)
#col4.metric("Average Investment (M USD)", f"{df['investment_amount'].mean():.2f}" if "investment_amount" in df else "N/A")

st.divider()

# ===================== MAIN LAYOUT =====================
left, right = st.columns([3, 1])

# ---------- LEFT: PROJECT CARDS ----------
with left:
    st.subheader("📁 Project Details")

    # Pagination setup
    items_per_page = 6
    total_projects = len(df)
    total_pages = (total_projects - 1) // items_per_page + 1

    # Session state for page index
    if "page" not in st.session_state:
        st.session_state.page = 1

    # Slice data by current page
    start_idx = (st.session_state.page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    # Display project cards
    for _, row in page_data.iterrows():
        st.markdown(f"""
        <div style="background-color:#f8f9fa;padding:15px;margin-bottom:10px;border-radius:10px;">
            <h4>{row.get('company_name', 'Unknown Company')}</h4>
            <p><b>Country:</b> {row.get('host_country', 'N/A')}</p>
            <p><b>Project Type:</b> {row.get('project_type', 'N/A')}</p>
            <p><b>Sector:</b> {row.get('sector', 'N/A')}</p>
            <p><b>Investment:</b> {row.get('investment_amount', 'N/A')}</p>
            <p><b>Stage:</b> {row.get('project_stage', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- PAGINATION CONTROLS ----------
    st.divider()
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.page > 1:
            if st.button("⬅️ Previous Page"):
                st.session_state.page -= 1
                st.rerun()
    with col_page:
        st.markdown(f"<center>Page {st.session_state.page} of {total_pages}</center>", unsafe_allow_html=True)
    with col_next:
        if st.session_state.page < total_pages:
            if st.button("Next Page ➡️"):
                st.session_state.page += 1
                st.rerun()

# ---------- RIGHT: PLOTLY CHART ----------
with right:
    st.subheader("📊 Regional Overview")

    if "region" in df.columns:
        region_summary = df.groupby("region").size().reset_index(name="count")
        fig = px.bar(region_summary, x="region", y="count", title="Projects by Region", text_auto=True)
        fig.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No 'region' column found in your CSV.")
