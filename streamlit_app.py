import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Ebook Management", layout="wide")

st.title("📚 Ebook Database Management System")

# 2. Connection
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

try:
    # Load and clean data
    df = pd.read_csv(url)
    
    # 3. Smart Search & Navigation Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("🔍 Search Database:", placeholder="Type Author, Title, or ID...")
    
    with col2:
        st.write(" ") # Alignment space
        nav_col1, nav_col2 = st.columns(2)
        # These act as "jump" buttons
        if nav_col1.button("⏮️ First Record"):
            st.session_state.scroll_to = 0
        if nav_col2.button("⏭️ Last Record"):
            st.session_state.scroll_to = len(df)

    # 4. Improved Search Logic
    if search:
        # This splits "Ian Rankin" into two words and finds rows containing BOTH
        search_terms = search.lower().split()
        mask = df.apply(lambda row: all(term in row.astype(str).str.lower().to_string() for term in search_terms), axis=1)
        df = df[mask]

    # 5. Display the Spreadsheet
    # Sorting by 'Date Requested' or 'ID' helps with "Pending" visibility
    st.data_editor(
        df,
        height=650,
        use_container_width=True,
        hide_index=False, # Showing index helps Terry see row numbers
        column_config={
            "ID Number": st.column_config.NumberColumn(pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True
    )
    
    st.success(f"Viewing {len(df)} records.")

except Exception as e:
    st.error("Connection sync in progress... please refresh.")
