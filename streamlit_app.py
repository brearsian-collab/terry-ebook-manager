import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")

# JavaScript for Pixel-Perfect Jumping
def scroll_to_id(target_top=True):
    if target_top:
        # Snaps to the absolute top of the page
        js = "window.parent.scrollTo({top: 0, behavior: 'auto'});"
    else:
        # Snaps to the absolute bottom of the entire document
        js = "window.parent.scrollTo({top: window.parent.document.body.scrollHeight, behavior: 'auto'});"
    
    st.components.v1.html(f"<script>{js}</script>", height=0)

st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    df = pd.read_csv(url)
    df = df.fillna("")
    
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df.columns = new_names[:len(df.columns)]
    
    # Clean up Days Searching
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
        if st.button("⏮️ First Record"):
            scroll_to_id(target_top=True)

    with c4:
        st.write(" ")
        if st.button("⏭️ Last Record"):
            scroll_to_id(target_top=False)

    # Filtering Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # Natural 1-2292 order
    df = df.sort_values(by="ID Number", ascending=True)

    # CSS for Sticky Headers and Visual Clarity
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
            .main-table th { 
                background-color: #f0f2f6 !important; 
                padding: 12px; 
                border: 1px solid #dee2e6; 
                text-align: center; 
                position: sticky; 
                top: 0; 
                z-index: 100;
                box-shadow: 0 2px 2px rgba(0,0,0,0.1);
            }
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; background-color: white; }
            .center-text { text-align: center !important; }
            .left-text { text-align: left !important; }
        </style>
    """, unsafe_allow_html=True)

    # Build the one big table
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

    st.markdown(html, unsafe_allow_html=True)
    
    # --- BOTTOM NAVIGATION ---
    st.write("---")
    bc1, bc2 = st.columns([5, 1])
    with bc2:
        if st.button("⏮️ Back to First Record"):
            scroll_to_id(target_top=True)

except Exception as e:
    st.error(f"Something went wrong: {e}")
