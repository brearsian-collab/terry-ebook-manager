import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")

# Unique keys for anchors
TOP_ANCHOR = "top_of_table"
BOTTOM_ANCHOR = "bottom_of_table"

# Invisible anchor at the very top
st.markdown(f'<div id="{TOP_ANCHOR}"></div>', unsafe_allow_html=True)

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

    # --- TOP NAVIGATION CONTROLS ---
    c1, c2, c3, c4 = st.columns([2, 1, 0.5, 0.5])
    
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    
    with c2:
        st.write(" ")
        st.write(" ")
        show_pending = st.checkbox("📋 Show Only Unfound") 

    with c3:
        st.write(" ")
        if st.button("⏮️ First", key="btn_top_first"):
            st.components.v1.html(f'<script>window.parent.document.getElementById("{TOP_ANCHOR}").scrollIntoView();</script>', height=0)

    with c4:
        st.write(" ")
        if st.button("⏭️ Last", key="btn_top_last"):
            st.components.v1.html(f'<script>window.parent.document.getElementById("{BOTTOM_ANCHOR}").scrollIntoView();</script>', height=0)

    # Filtering Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # Natural 1-2292 order
    df = df.sort_values(by="ID Number", ascending=True)

    # Styling
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; margin-bottom: 20px; }
            .main-table th { background-color: #f0f2f6; padding: 10px; border: 1px solid #dee2e6; text-align: center; position: sticky; top: 0; z-index: 10; }
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; }
            .center-text { text-align: center !important; }
            .left-text { text-align: left !important; }
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
            alignment = "center-text" if i in [0, 4, 5, 6, 7, 8] else "left-text"
            html += f'<td class="{alignment}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    # Render Table
    st.markdown(html, unsafe_allow_html=True)
    
    # Invisible anchor at the very bottom
    st.markdown(f'<div id="{BOTTOM_ANCHOR}"></div>', unsafe_allow_html=True)

    # --- BOTTOM NAVIGATION CONTROLS ---
    # This adds a "Back to Top" bar at the very bottom so Terry isn't stuck.
    bc1, bc2, bc3 = st.columns([3, 0.5, 0.5])
    with bc2:
        if st.button("⏮️ First Record", key="btn_bot_first"):
             st.components.v1.html(f'<script>window.parent.document.getElementById("{TOP_ANCHOR}").scrollIntoView();</script>', height=0)
    with bc3:
        # Just to let him know he's at the end
        st.write("🏁 End of List")

except Exception as e:
    st.info("Updating view... please wait.")
