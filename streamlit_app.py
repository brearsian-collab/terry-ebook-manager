import streamlit as st
import pandas as pd

# 1. Setup
st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

# 2. Connection Logic
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
# Using the most basic export URL possible
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # No caching - force a fresh download every time
    df = pd.read_csv(url)
    
    # Force the layout order
    cols = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df = df[[c for c in cols if c in df.columns]]

    # 3. Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type any name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 4. Search and Filter
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        # Finds rows where Date Completed is truly empty
        df = df[df['Date Completed'].isna() | (df['Date Completed'].astype(str).str.strip() == "")]

    # 5. First/Last Toggle
    if sort_choice == "Last Record":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 6. The Grid
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.NumberColumn(width="small", pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True
    )
    
    st.success(f"System Active: {len(df)} Records Loaded")

except Exception as e:
    st.error(f"Connection failed. Error details: {e}")
    st.info("Check that your Google Sheet is shared as 'Anyone with the link can view'.")
