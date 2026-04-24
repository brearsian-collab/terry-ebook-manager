import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")

# 1. Setup Scroll State
if 'scroll_trigger' not in st.session_state:
    st.session_state.scroll_trigger = 0

st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    df = pd.read_csv(url)
    df = df.fillna("")
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df.columns = new_names[:len(df.columns)]
    df['Days Searching'] = pd.to_numeric(df['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # --- CONTROLS ---
    c1, c2, c3, c4 = st.columns([2, 1, 0.5, 0.5])
    
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    with c2:
        st.write(" ")
        st.write(" ")
        show_pending = st.checkbox("📋 Show Only Unfound") 

    with c3:
        st.write(" ")
        if st.button("⏮️ First"):
            st.session_state.scroll_trigger = 1 # 1 = Top
            st.rerun()

    with c4:
        st.write(" ")
        if st.button("⏭️ Last"):
            st.session_state.scroll_trigger = 2 # 2 = Bottom
            st.rerun()

    # Filtering
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    df = df.sort_values(by="ID Number", ascending=True)

    # Styling
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
        </style>
    """, unsafe_allow_html=True)

    # Build Table
    html = '<table class="main-table"><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>' + ''.join([f'<td>{val}</td>' for val in row]) + '</tr>'
    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)

    # --- THE PERSISTENT SCROLL ENGINE ---
    # This script waits for the table to actually exist before moving
    if st.session_state.scroll_trigger > 0:
        target = "0" if st.session_state.scroll_trigger == 1 else "window.parent.document.body.scrollHeight"
        
        st.components.v1.html(f"""
            <script>
                function doScroll() {{
                    const scrollTarget = {target};
                    window.parent.scrollTo({{top: scrollTarget, behavior: 'auto'}});
                }}
                // Run immediately, then again after a tiny delay to ensure the table "settled"
                doScroll();
                setTimeout(doScroll, 100);
                setTimeout(doScroll, 300);
            </script>
        """, height=0)
        
        st.session_state.scroll_trigger = 0 # Reset

except Exception as e:
    st.error(f"Error: {e}")
