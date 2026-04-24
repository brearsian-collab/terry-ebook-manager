import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Ebook Management", layout="wide")

# This is the "Magic Script" that fixes the scroll issues
def force_scroll_top():
    st.components.v1.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'smooth'});
        </script>
        """,
        height=0,
    )

def force_scroll_bottom():
    st.components.v1.html(
        """
        <script>
            window.parent.scrollTo({top: window.parent.document.body.scrollHeight, behavior: 'smooth'});
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
    
    # Cleaning
    df_raw['Days Searching'] = pd.to_numeric(df_raw['Days Searching'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', '')

    # Controls
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

    # Navigation UI
    def render_nav(suffix):
        col_prev, col_page, col_next, col_jump = st.columns([1, 2, 1, 2])
        with col_jump:
            sub1, sub2 = st.columns(2)
            if sub1.button("⏮️ Jump to First", key=f"first_{suffix}"):
                st.session_state.page_number = 1
                force_scroll_top()
                st.rerun()
            if sub2.button("⏭️ Jump to Last", key=f"last_{suffix}"):
                st.session_state.page_number = total_pages
                # We trigger the scroll top here so they see the start of the last page
                force_scroll_top() 
                st.rerun()
        with col_prev:
            if st.button("⬅️ Previous", key=f"prev_{suffix}") and st.session_state.page_number > 1:
                st.session_state.page_number -= 1
                force_scroll_top()
                st.rerun()
        with col_next:
            if st.button("Next ➡️", key=f"next_{suffix}") and st.session_state.page_number < total_pages:
                st.session_state.page_number += 1
                force_scroll_top()
                st.rerun()
        with col_page:
            st.write(f"**Page {st.session_state.page_number} of {total_pages}**")

    render_nav("top")

    # Display Data
    start_idx = (st.session_state.page_number - 1) * items_per_page
    df_page = df.iloc[start_idx : start_idx + items_per_page]

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
    
    # Bottom Nav
    render_nav("bottom")
    
    st.write("---")
    
    # Dedicated Scroll Buttons
    b1, b2 = st.columns(2)
    if b1.button("⬆️ Scroll to Top of Tab"):
        force_scroll_top()
    if b2.button("⬇️ Scroll to Bottom of Tab"):
        force_scroll_bottom()

except Exception as e:
    st.error(f"Error: {e}")
