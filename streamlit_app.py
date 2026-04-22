import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 1. Pull the data directly
    df = pd.read_csv(url)
    
    # 2. Identify columns by position so names don't matter
    # Position 0 = ID, 1 = First Name, 2 = Surname, 3 = Title
    id_col = df.columns[0]
    title_col = df.columns[3] if len(df.columns) > 3 else df.columns[-1]

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
        # Tries to find a 'Date' column to filter
        date_cols = [c for c in df.columns if 'DATE' in c.upper() or 'COMPLET' in c.upper()]
        filter_col = date_cols[-1] if date_cols else df.columns[-1]
        df = df[df[filter_col].isna() | (df[filter_col].astype(str).str.strip() == "")]

    # 5. Flip for First/Last
    if sort_choice == "Last Record":
        df = df.sort_values(by=id_col, ascending=False)
    else:
        df = df.sort_values(by=id_col, ascending=True)

    # 6. Display with Pinned Columns
    st.data_editor(
        df,
        height=700,
        use_container_width=True,
        hide_index=True,
        column_config={
            id_col: st.column_config.Column(pinned=True, width="small"),
            title_col: st.column_config.Column(pinned=True, width="large"),
        },
        disabled=True
    )
    
    st.success(f"System Online: {len(df)} Records Loaded")

except Exception as e:
    st.info("🔄 Refreshing the connection to your Google Sheet...")
    if st.button("Manual Refresh"):
        st.rerun()
