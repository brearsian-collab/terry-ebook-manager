import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    df = pd.read_csv(url)
    df = df.fillna("")
    
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df.columns = new_names[:len(df.columns)]
    
    # Clean up the decimal points in 'Days Searching'
    df['Days Searching'] = pd.to_numeric(df['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Only Unfound") 
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # Natural 1-2292 order
    df = df.sort_values(by="ID Number", ascending=True)

    # Styling with Days Searching (index 6) centered
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
            .main-table th { background-color: #f0f2f6; padding: 10px; border: 1px solid #dee2e6; text-align: center; }
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
            # Centering ID(0), Requested(4), Found(5), Days(6), Star(7), Completed(8)
            alignment = "center-text" if i in [0, 4, 5, 6, 7, 8] else "left-text"
            html += f'<td class="{alignment}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)

    if sort_choice == "Last Record":
        st.info("Showing natural order. Scroll down for the newest records.")

except Exception as e:
    st.info("Updating view... please wait.")
