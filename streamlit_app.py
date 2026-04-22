import streamlit as st
import pandas as pd

# 1. Setup
st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 2. Pull Data and Clean
    df = pd.read_csv(url)
    df = df.fillna("") # Clears out 'None' values

    # 3. Rename Columns by Position to ensure logic works
    # This guarantees the code knows exactly where 'ID' and 'Found Date' are
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    # Only rename what exists in the actual file
    df.columns = new_names[:len(df.columns)]

    # 4. Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type any name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 5. Search Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    # 6. FIXED: Show Pending (Checks if 'Found Date' is empty)
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # 7. Sorting
    if sort_choice == "Last Record":
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # 8. Display with Strict Alignment & Labels
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.Column(width="small", pinned=True),
            "First Name": st.column_config.Column(width="medium"),
            "Surname": st.column_config.Column(width="medium"),
            "Book Title": st.column_config.Column(width="large"),
            "Date Requested": st.column_config.Column(width="medium"),
            "Found Date": st.column_config.Column(width="medium"),
            "Days Searching": st.column_config.Column(width="small"),
            "Star Rating": st.column_config.Column(width="small"),
            "Date Completed": st.column_config.Column(width="medium"),
            "Notes": st.column_config.Column(width="large"),
        },
        disabled=True
    )
    
    # CSS to force centering for IDs and Dates
    st.markdown("""
        <style>
            /* Centers ID Number, Dates, and Ratings */
            [data-testid="stHeaderBlock"] div:nth-child(1) {text-align: center;}
            [data-testid="stHeaderBlock"] div:nth-child(5) {text-align: center;}
            [data-testid="stHeaderBlock"] div:nth-child(6) {text-align: center;}
            [data-testid="stHeaderBlock"] div:nth-child(8) {text-align: center;}
            [data-testid="stHeaderBlock"] div:nth-child(9) {text-align: center;}
        </style>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Waiting for layout to sync... {e}")
