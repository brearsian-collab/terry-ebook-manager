import streamlit as st
import pandas as pd

# 1. Setup
st.set_page_config(page_title="Ebook Management", layout="wide")

st.title("📚 Ebook Database Management System")

# 2. Data Connection
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60) # Refreshes every minute automatically
def load_data():
    data = pd.read_csv(url)
    # Define exact order Terry expects
    cols = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    return data[[c for c in cols if c in data.columns]]

try:
    raw_df = load_data()
    display_df = raw_df.copy()

    # 3. Navigation Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search Database:", placeholder="Type any name or title...")
    
    with col2:
        st.write(" ")
        show_pending = st.toggle("📋 Show Pending Only")
        
    with col3:
        st.write(" ")
        # Toggle between Top and Bottom of list
        sort_btn = st.radio("Jump to:", ["Top (First)", "Bottom (Last)"], horizontal=True)

    # 4. Filter and Sort Logic
    if search:
        display_df = display_df[display_df.apply(lambda r: search.lower() in r.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        # Filters for rows where 'Date Completed' is empty
        display_df = display_df[display_df['Date Completed'].isna()]

    if "Bottom" in sort_btn:
        display_df = display_df.sort_values(by="ID Number", ascending=False)
    else:
        display_df = display_df.sort_values(by="ID Number", ascending=True)

    # 5. The Main Spreadsheet Grid
    st.data_editor(
        display_df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.NumberColumn(width="small", pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True
    )
    
    st.info(f"Viewing {len(display_df)} of {len(raw_df)} total records.")

except Exception as e:
    st.error("Connecting... if this takes more than 10 seconds, please refresh your browser.")
