import streamlit as st
import pandas as pd

# 1. Page Setup
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
    # Load and clean the data
    df = pd.read_csv(url)
    
    # 3. The "Windows App" Interface
    # This creates a search box that filters the whole sheet live
    search = st.text_input("🔍 Quick Search:", placeholder="Type any name, title, or ID...")
    
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    # 4. The Interactive Spreadsheet
    # 'st.data_editor' looks like Excel and allows column freezing
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.NumberColumn(width="small", pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True # This keeps it as 'View Only' for Terry
    )
    
    st.caption(f"Connected to Master Sheet. Total Records: {len(df)}")

except Exception as e:
    st.error("Connection link is valid, but the data is taking a moment to stream. Please refresh in 10 seconds.")
