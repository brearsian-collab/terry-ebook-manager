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

    # JAVASCRIPT FOR PERFECT SCROLLING
    scroll_script = """
        <script>
            function scrollApp(toTop) {
                const scrollContainer = window.parent.document.querySelector('.main .block-container');
                if (toTop) {
                    window.parent.scrollTo({top: 0, behavior: 'smooth'});
                    if(scrollContainer) scrollContainer.scrollIntoView({behavior: 'smooth', block: 'start'});
                } else {
                    window.parent.scrollTo({top: window.parent.document.body.scrollHeight, behavior: 'smooth'});
                    const bottomMarker = window.parent.document.getElementById('bottom_of_table');
                    if(bottomMarker) bottomMarker.scrollIntoView({behavior: 'smooth', block: 'end'});
                }
            }
        </script>
    """

    with c3:
        st.write(" ")
        if st.button("⏮️ First", key="btn_top_first"):
            st.components.v1.html(scroll_script + '<script>scrollApp(true);</script>', height=0)

    with c4:
        st.write(" ")
        if st.button("⏭️ Last", key="btn_top_last"):
            st.components.v1.html(scroll_script + '<script>scrollApp(false);</script>', height=0)

    # Filtering Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    if show_pending:
        df = df[df["Found Date"].astype(str).str.strip() == ""]

    # Natural 1-2292 order
    df = df.sort_values(by="ID Number", ascending=True)

    # Styling - FIXED STICKY HEADERS AND SCROLL WRAPPING
    st.markdown("""
        <style>
            .main-table { 
                width: 100%; 
                border-collapse: collapse; 
                font-family: sans-serif; 
                margin-bottom: 20px; 
            }
            
            .main-table th { 
                background-color: #f0f2f6 !important; 
                color: black;
                padding: 12px; 
                border: 1px solid #dee2e6; 
                text-align: center; 
                position: sticky; 
                top: 0; 
                z-index: 99; 
                box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.4);
            }
            
            .main-table td { padding: 8px; border: 1px solid #dee2e6; font-size: 14px; background-color: white; }
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

    st.markdown(html, unsafe_allow_html=True)
    
    # Invisible anchor at the very bottom
    st.markdown(f'<div id="{BOTTOM_ANCHOR}" style="padding-bottom: 50px;"></div>', unsafe_allow_html=True)

    # --- BOTTOM NAVIGATION CONTROLS ---
    bc1, bc2, bc3 = st.columns([3, 1, 0.5])
    with bc2:
        if st.button("⏮️ Back to Top", key="btn_bot_first"):
             st.components.v1.html(scroll_script + '<script>scrollApp(true);</script>', height=0)
    with bc3:
        st.write("🏁 End of List")

except Exception as e:
    st.info("Updating view... please wait.")
