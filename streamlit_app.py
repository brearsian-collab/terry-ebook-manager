import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Ebook Management", layout="wide")

# Function to force the browser to the top of the page
def scroll_to_top():
    st.components.v1.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'auto'});
        </script>
        """,
        height=0,
    )

st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    df_raw = pd.read_csv(url)
    df_raw = df_raw.fillna("")
    new_names = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    df_raw.columns = new_names[:len(df_raw.columns)]
    df_raw['Days Searching'] = pd.to_numeric(df_raw['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # Search and Filter
    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type name or title...")
    with c2:
        st.write(" ")
        st.write(" ")
        show_pending = st.checkbox("📋 Show Only Unfound") 

    df = df_raw.copy()
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    df = df.sort_values(by="ID Number", ascending=True)

    # Pagination
    items_per_page = 50
    total_pages = math.ceil(len(df) / items_per_page)
    
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    # NAVIGATION UI
    def render_nav(suffix):
        col_prev, col_page, col_next, col_jump1, col_jump2 = st.columns([1, 1.5, 1, 1.5, 1.5])
        
        with col_prev:
            if st.button("⬅️ Previous", key=f"prev_{suffix}") and st.session_state.page_number > 1:
                st.session_state.page_number -= 1
                scroll_to_top()
                st.rerun()
        
        with col_page:
            st.write(f"**Page {st.session_state.page_number} of {total_pages}**")
            
        with col_next:
            if st.button("Next ➡️", key=f"next_{suffix}") and st.session_state.page_number < total_pages:
                st.session_state.page_number += 1
                scroll_to_top()
                st.rerun()

        with col_jump1:
            if st.button("⏮️ Jump to First", key=f"first_{suffix}"):
                st.session_state.page_number = 1
                scroll_to_top()
                st.rerun()

        with col_jump2:
            if st.button("⏭️ Jump to Last", key=f"last_{suffix}"):
                st.session_state.page_number = total_pages
                scroll_to_top()
                st.rerun()

    # Top Navigation
    render_nav("top")

    # Slice Data
    start_idx = (st.session_state.page_number - 1) * items_per_page
    df_page = df.iloc[start_idx : start_idx + items_per_page]

    # Table Styling
    st.markdown("""
        <style>
            .main-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
            .main-table th { background-color: #f0f2f6; padding: 10px; border: 1px solid #dee2e6; text-align: center; }
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; background-color: white; }
            .center-text { text-align: center !important; }
            .left-text { text-align: left !important; }
        </style>
    """, unsafe_allow_html=True)

    html = '<table class="main-table"><thead><tr>'
    for col in df_page.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'

    for _, row in df_page.iterrows():
        html += '<tr>'
        for i, val in enumerate(row):
            alignment = "center-text" if i in [0, 4, 5, 6, 7, 8] else "left-text"
            html += f'<td class="{alignment}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)
    
    # Bottom Navigation
    st.write("---")
    render_nav("bottom")

except Exception as e:
    st.error(f"Error: {e}")
