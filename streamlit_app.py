import streamlit as st
import pandas as pd

# 1. Setup
st.set_page_config(page_title="Ebook Management", layout="wide")

st.title("📚 Ebook Database Management System")

# 2. Direct Data Link (Simpler version)
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=300) # Keep data for 5 mins to stay fast
def load_data(url):
    df = pd.read_csv(url)
    # Ensure ID Number is column #1
    cols_to_show = ["ID Number", "First Name", "Surname", "Book Title", "Date Requested", "Found Date", "Days Searching", "Star Rating", "Date Completed", "Notes"]
    # Only keep columns that actually exist in the sheet
    existing_cols = [c for c in cols_to_show if c in df.columns]
    return df[existing_cols]

try:
    raw_df = load_data(url)
    display_df = raw_df.copy()

    # 3. Desktop-Style Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Quick Search:", placeholder="Search names, titles, or IDs...")
    with c2:
        st.write(" ")
        pending = st.checkbox("📋 Show Pending Only")
    with c3:
        st.write(" ")
        sort_choice = st.radio("View:", ["Top", "Bottom"], horizontal=True)

    # 4. Filter Logic
    if search:
        display_df = display_df[display_df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    
    if pending:
        # This handles cases where 'Date Completed' is empty or NaN
        display_df = display_df[display_df['Date Completed'].isna() | (display_df['Date Completed'] == "")]

    if sort_choice == "Bottom":
        display_df = display_df.sort_values(by="ID Number", ascending=False)
    else:
        display_df = display_df.sort_values(by="ID Number", ascending=True)

    # 5. The Spreadsheet View
    st.data_editor(
        display_df,
        height=650,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID Number": st.column_config.NumberColumn(width="small", pinned=True),
            "Book Title": st.column_config.TextColumn(width="large", pinned=True),
        },
        disabled=True
    )
    
    st.success(f"Viewing {len(display_df)} records.")

except Exception as e:
    st.warning("⚠️ The app is having trouble reaching the sheet. Please click 'Share' in Google Sheets and make sure it is set to 'Anyone with the link can view'.")
    if st.button("Retry Connection"):
        st.cache_data.clear()
        st.rerun()
