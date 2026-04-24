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
    
    # Clean up 'Days Searching'
    df['Days Searching'] = pd.to_numeric(df['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # --- CONTROLS ---
    c1, c2, c3 = st.columns([2, 1, 1.5])
    
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    
    with c2:
        st.write(" ")
        st.write(" ")
        show_pending = st.checkbox("📋 Show Only Unfound") 

    with c3:
        st.write(" ")
        # THIS REPLACES THE JUMP BUTTON: It moves the last records to the top instantly.
        sort_order = st.radio("Show records in order:", ["Oldest First (1 to 2291)", "Newest First (2291 to 1)"], horizontal=True)

    # Filtering Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # --- THE SORTING MAGIC ---
    if "Newest" in sort_order:
        df = df.sort_values(by="ID Number", ascending=False)
    else:
        df = df.sort_values(by="ID Number", ascending=True)

    # Styling for a clean table with a sticky header
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
            .main-table th { 
                background-color: #f0f2f6 !important; 
                padding: 12px; border: 1px solid #dee2e6; text-align: center; 
                position: sticky; top: 0; z-index: 100;
                box-shadow: 0 2px 2px rgba(0,0,0,0.1);
            }
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; background-color: white; }
            .center-text { text-align: center !important; }
        </style>
    """, unsafe_allow_html=True)

    # Build Table
    html = '<table class="main-table"><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'

    for _, row in df.iterrows():
        html += '<tr>'
        for i, val in enumerate(row):
            alignment = "center-text" if i in [0, 4, 5, 6, 7, 8] else ""
            html += f'<td class="{alignment}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
