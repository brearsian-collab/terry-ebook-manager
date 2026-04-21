import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(url)
    
    # 1. FIX THE COLUMN ORDER (ID Number first, then Name, then Title)
    cols = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df = df[[c for c in cols if c in df.columns]]

    # 2. NAVIGATION BUTTONS
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search Database:", placeholder="Type Author, Title, or ID...")
    
    with col2:
        st.write(" ") 
        nav1, nav2 = st.columns(2)
        
        # When pressed, these sort the data to bring the First or Last to the top
        if nav1.button("⏮️ First Record"):
            st.session_state.sort_order = "First"
        if nav2.button("⏭️ Last Record"):
            st.session_state.sort_order = "Last"

    # 3. APPLY NAVIGATION LOGIC
    if "sort_order" not in st.session_state:
        st.session_state.sort_order = "First"

    if st.session_state.sort_order == "Last":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 4. SMART SEARCH
    if search:
        search_terms = search.lower().split()
        mask = df.apply(lambda row: all(term in row.astype(str).str.lower().to_string() for term in search_terms), axis=1)
        df = df[mask]

    # 5. THE SPREADSHEET VIEW
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
    
    st.caption(f"Showing {len(df)} records. ID and Title are pinned to the left.")

except Exception as e:
    st.error("Connecting to Google Sheets...")
