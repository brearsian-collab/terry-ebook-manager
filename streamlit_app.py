import streamlit as st
import pandas as pd

# 1. Page Config & Layout
st.set_page_config(page_title="Ebook Management", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Ebook Database Management System")

# 2. Connection
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(url)
    
    # 3. FORCE ORIGINAL COLUMN ORDER
    # This keeps ID Number first, then Name, then Title, just like the original layout
    cols = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df = df[[c for c in cols if c in df.columns]]

    # 4. Navigation & Search UI
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("🔍 Search Database:", placeholder="Type Author, Title, or ID...")
    
    with col2:
        st.write(" ") 
        nav1, nav2 = st.columns(2)
        
        # We use session_state to remember if Terry wants to see the top or bottom
        if nav1.button("⏮️ First Record"):
            st.session_state.view_mode = "First"
        if nav2.button("⏭️ Last Record"):
            st.session_state.view_mode = "Last"

    # Default to showing the first records
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "First"

    # 5. Search Logic
    if search:
        search_terms = search.lower().split()
        mask = df.apply(lambda row: all(term in row.astype(str).str.lower().to_string() for term in search_terms), axis=1)
        df = df[mask]

    # 6. Apply "First/Last" Logic by Sorting
    if st.session_state.view_mode == "Last":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 7. Final Spreadsheet Display
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
    
    st.caption(f"Currently viewing: {st.session_state.view_mode} Records | Total: {len(df)}")

except Exception as e:
    st.info("🔄 Synchronizing with Google Sheets... please wait a few seconds.")
