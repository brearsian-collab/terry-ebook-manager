import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 1. Load data and clean up 'None' values
    df = pd.read_csv(url)
    df = df.fillna("")

    # 2. FORCE EXACT COLUMN ORDER
    # This ensures names/titles don't jump around
    expected_order = [
        "ID Number", "First Name", "Surname", "Book Title", 
        "Date Requested", "Found Date", "Days Searching", 
        "Star Rating", "Date Completed", "Notes"
    ]
    # Filter to only columns that exist, keeping your preferred sequence
    df = df[[c for c in expected_order if c in df.columns]]

    # 3. UI Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type any name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 4. Search & Filter Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        # Look for the column that contains 'Completed' or use position 8
        target = "Date Completed" if "Date Completed" in df.columns else df.columns[8]
        df = df[df[target].astype(str).str.strip() == ""]

    # 5. Sorting (Ascending ensures 2292 is at the bottom)
    df = df.sort_values(by=df.columns[0], ascending=True)

    # 6. STYLING & ALIGNMENT MAP
    # We define exactly how each column should behave
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.Column(width="small", pinned=True, help="ID"),
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
    
    # Custom CSS to force text alignment (Center vs Left)
    st.markdown("""
        <style>
            /* Center align specific columns (1st, 5th, 6th, 8th, 9th) */
            [data-testid="stTable"] td:nth-child(1), 
            [data-testid="stTable"] td:nth-child(5),
            [data-testid="stTable"] td:nth-child(6),
            [data-testid="stTable"] td:nth-child(8),
            [data-testid="stTable"] td:nth-child(9) {
                text-align: center !important;
            }
        </style>
        """, unsafe_allow_html=True)

    if sort_choice == "Last Record":
        st.info("Showing natural order. Scroll down to see record #2292.")

except Exception as e:
    st.error(f"Layout Alignment Error: {e}")
