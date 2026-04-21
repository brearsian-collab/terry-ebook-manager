import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def get_data(u):
    # This is the most "Forceful" way to get the data
    return pd.read_csv(u)

try:
    df = get_data(url)
    
    # Force the layout order
    cols = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df = df[[c for c in cols if c in df.columns]]

    # UI Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Quick Search:", placeholder="Search names or titles...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        view_sort = st.radio("View:", ["Top (First)", "Bottom (Last)"], horizontal=True)

    # 1. Search Logic (Splits "Ian Rankin" into two words to find both)
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]

    # 2. Pending Logic (Finds blank 'Date Completed' or 'Found Date')
    if show_pending:
        df = df[df['Date Completed'].isna() | (df['Date Completed'].astype(str).str.strip() == "")]

    # 3. First/Last Logic
    if "Bottom" in view_sort:
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 4. Display
    st.data_editor(
        df,
        height=650,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.NumberColumn(width="small", pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True
    )
    st.success(f"System Online: {len(df)} records matched.")

except Exception as e:
    st.warning("⚠️ Access Denied by Google. Please set your Google Sheet to 'Anyone with the link can view' via the Share button.")
    if st.button("Retry Connection"):
        st.cache_data.clear()
        st.rerun()
