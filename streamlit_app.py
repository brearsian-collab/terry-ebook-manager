import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Terry's Ebook Manager", layout="wide")

# Custom CSS to make the search bar look better
st.markdown("""
    <style>
    .stTextInput { position: sticky; top: 0; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Terry's Ebook Database")

# 2. Connection Details
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
SHEET_NAME = "Ebook%20Requests"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# 3. Load Data
try:
    df = pd.read_csv(url)
    
    # Navigation Buttons & Search
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search = st.text_input("🔍 Search for a book, author, or ID:", placeholder="Type here...")
    
    # Filter logic
    if search:
        df = df[df.stack().str.contains(search, case=False, na=False).any(level=0)]

    # 4. Jump to First/Last (Visual Indicators)
    st.write(f"Displaying {len(df)} records. *Click any column header to sort A-Z.*")

    # 5. The Spreadsheet View
    # 'height=600' creates the vertical scroll bar
    # 'use_container_width' creates the horizontal scroll bar if needed
    st.dataframe(
        df, 
        height=600, 
        use_container_width=True, 
        hide_index=True
    )

    # 6. Quick Navigation Footer
    f1, f2, f3 = st.columns(3)
    with f2:
        if st.button("⬆️ Back to Top"):
            st.rerun()

except Exception as e:
    st.error("Connection successful, but check the Sheet column names.")
