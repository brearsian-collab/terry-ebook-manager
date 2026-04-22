import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 1. Pull and Clean Data
    df = pd.read_csv(url)
    df = df.fillna("")
    
    # Standardize column names for the code to use
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df.columns = new_names[:len(df.columns)]
    
    # Clean up the decimal points in 'Days Searching'
    df['Days Searching'] = pd.to_numeric(df['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # 2. Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    with c2:
        st.write(" ")
        # Renamed to match your screenshot intent
        show_pending = st.checkbox("📋 Show Only Unfound") 
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 3. Filtering Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    # FIXED: Strict filter for Unfound books
    if show_pending:
        # This keeps ONLY rows where Found Date is totally empty
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # 4. FIXED: Always keep 1 at the top, 2292 at the bottom
    df = df.sort_values(by="ID Number", ascending=True)

    # 5. Build the Table with Fixed Centering
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
            .main-table th { background-color: #f0f2f6; padding: 10px; border: 1px solid #dee2e6; text-align: left; }
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; }
            .center-text { text-align: center !important; }
            .left-text { text-align: left !important; }
        </style>
    """, unsafe_allow_html=True)

    html = '<table class="main-table"><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'

    for _, row in df.iterrows():
        html += '<tr>'
        for i, val in enumerate(row):
            # ID, Dates, and Rating are centered
            alignment = "center-text" if i in [0, 4, 5, 7, 8] else "left-text"
            html += f'<td class="{alignment}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)

    # 6. Navigation Aid
    if sort_choice == "Last Record":
        st.info("Showing natural order (1-2292). Scroll to the bottom for the latest entries.")

except Exception as e:
    st.info("Refreshing database connection...")
