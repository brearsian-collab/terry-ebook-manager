import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Terry's Ebook Manager", layout="wide")
st.title("📚 Terry's Ebook Database")

# 2. Connection Details
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
SHEET_NAME = "Ebook%20Requests"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# 3. Load Data
try:
    df = pd.read_csv(url)
    
    # 4. Search Filter
    search = st.text_input("🔍 Search for a book or author:")
    
    if search:
        # This filters the table as Terry types
        df = df[df.stack().str.contains(search, case=False, na=False).any(level=0)]

    # 5. Display the Table
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.success(f"Successfully loaded {len(df)} records.")

except Exception as e:
    st.error("Connection successful, but had trouble formatting the data.")
    st.info("Check your Google Sheet column headers.")
