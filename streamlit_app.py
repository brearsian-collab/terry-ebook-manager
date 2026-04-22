import streamlit as st
import pandas as pd

# 1. Setup
st.set_page_config(page_title="Ebook Management", layout="wide")

st.title("📚 Ebook Database Management System")

# 2. Connection
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # Pull fresh data
    df = pd.read_csv(url)
    
    # 3. FORCE EXACT COLUMN ORDER (Matching your Google Sheet)
    # This ensures ID Number is 1st, then Name, then Title, etc.
    original_cols = [
        "ID Number", "First Name", "Surname", "Book Title", 
        "Date Requested", "Found Date", "Days Searching", 
        "Star Rating", "Date Completed", "Notes"
    ]
    
    # Only include columns that actually exist in your sheet to avoid errors
    df = df[[c for c in original_cols if c in df.columns]]

    # 4. Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Quick Search:", placeholder="Search names, titles, or IDs...")
    with c2:
        st.write(" ")
        pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 5. Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if pending:
        # Filters for rows with no 'Date Completed'
        df = df[df['Date Completed'].isna() | (df['Date Completed'].astype(str).str.strip() == "")]

    if sort_choice == "Last Record":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 6. FIXED ALIGNMENT VIEW
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.Column(width="small", pinned=True),
            "First Name": st.column_config.Column(width="medium"),
            "Surname": st.column_config.Column(width="medium"),
            "Book Title": st.column_config.Column(width="large", pinned=True),
            "Date Requested": st.column_config.Column(width="medium"),
            "Notes": st.column_config.Column(width="large"),
        },
        disabled=True
    )
    
    st.success(f"Connected: {len(df)} records aligned.")

except Exception as e:
    st.error(f"Waiting for data alignment... if this persists, check the 'ID Number' column header in your sheet.")
    if st.button("Refresh System"):
        st.rerun()
