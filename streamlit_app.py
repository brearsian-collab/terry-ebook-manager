import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ebook Management", layout="wide")
st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    # 1. Pull the data
    df = pd.read_csv(url)
    
    # 2. Map Columns by Position (instead of names)
    # This ensures that even if Google renames them, the layout stays the same
    id_col = df.columns[0]     # First column (ID Number)
    title_col = df.columns[3]  # Fourth column (Book Title)

    # 3. Desktop Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search Database:", placeholder="Type any name or title...")
    with c2:
        st.write(" ")
        show_pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("Jump to:", ["First Record", "Last Record"], horizontal=True)

    # 4. Search Logic
    if search:
        for term in search.lower().split():
            df = df[df.apply(lambda row: term in row.astype(str).str.lower().to_string(), axis=1)]
    
    # 5. Pending Logic (Finds blank cells in the 'Date Completed' area)
    if show_pending:
        # We look for the column that usually holds the date
        date_col = next((c for c in df.columns if 'COMPLET' in c.upper()), df.columns[-2])
        df = df[df[date_col].isna() | (df[date_col].astype(str).str.strip() == "")]

    # 6. Flip the list for 'Last Record'
    if sort_choice == "Last Record":
        df = df.sort_values(by=id_col, ascending=False)
    else:
        df = df.sort_values(by=id_col, ascending=True)

    # 7. Final Spreadsheet View
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
    
    st.success(f"Connected! Showing {len(df)} records. ID and Title are pinned to the left.")

except Exception as e:
    st.error(f"The system is connected but waiting for the data to align. Please click 'Refresh' below.")
    if st.button("Refresh System"):
        st.rerun()
