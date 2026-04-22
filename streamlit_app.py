import streamlit as st
import pandas as pd

# 1. Page Config for Maximum Width
st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 2. Pull Data and Force Column Names
    df = pd.read_csv(url)
    df = df.fillna("")
    
    # We rename purely to ensure our 'Found Date' filter works perfectly
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df.columns = new_names[:len(df.columns)]

    # 3. Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 4. Search Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    # 5. FIXED: Show Pending (Filters for blank Found Date)
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # 6. Sorting
    if sort_choice == "Last Record":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 7. THE WIDE VIEW DISPLAY
    # Using st.dataframe instead of data_editor for better horizontal visibility
    st.dataframe(
        df,
        height=750,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.Column(width="small", pinned=True),
            "Book Title": st.column_config.Column(width="large"),
            "Notes": st.column_config.Column(width="large"),
        }
    )
    
    # CSS to force the ID column back to the left and fix centering
    st.markdown("""
        <style>
            /* Force center text in specific columns */
            [data-testid="stDataFrame"] div[data-testid="styled-td"]:nth-child(1),
            [data-testid="stDataFrame"] div[data-testid="styled-td"]:nth-child(5),
            [data-testid="stDataFrame"] div[data-testid="styled-td"]:nth-child(6) {
                text-align: center !important;
                justify-content: center !important;
            }
        </style>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Syncing layout... if this stays, refresh the page. Error: {e}")
