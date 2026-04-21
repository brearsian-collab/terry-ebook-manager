import streamlit as st
import pandas as pd

st.title("📚 Terry's Ebook Database")

# This is the 'Clean' ID from your sheet
SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
SHEET_NAME = "Ebook%20Requests" # The %20 replaces the space

# We build the URL specifically for a direct download
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    # We use standard pandas to read the URL directly
    df = pd.read_csv(url)
    
    # Display the data
    st.write(f"Showing {len(df)} records from the master sheet.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
except Exception as e:
    st.error("Still having trouble connecting to the sheet.")
    st.info("Check that the Google Sheet 'Share' settings are set to 'Anyone with the link can view'.")

# This line reads the data and ignores the 'worksheet' name for a moment 
# to see if we can get a basic connection first.
df = conn.read(spreadsheet=url)
# 2. Fetch the data
# We tell it to look at the 'Ebook Requests' tab specifically
df = conn.read(spreadsheet=url, worksheet="Ebook Requests")

# 3. Search Bar
search_term = st.text_input("🔍 Search by Book Title or Author", "")

if search_term:
    # Simple filter that looks across Title, First Name, and Surname
    mask = df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
    display_df = df[mask]
else:
    display_df = df

# 4. Display the Table (Touch-friendly)
st.dataframe(display_df, use_container_width=True, hide_index=True)

# 5. Add a New Record Section
with st.expander("➕ Add a New Request"):
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_first = st.text_input("First Name")
            new_surname = st.text_input("Surname")
            new_title = st.text_input("Book Title")
        with col2:
            new_req = st.text_input("Date Requested (DD/MM/YYYY)")
            new_status = st.selectbox("Star Rating", ["Not Rated", "1", "2", "3", "4", "5"])
        
        if st.form_submit_button("Submit to Google Sheets"):
            # Logic to append row to the Google Sheet
            st.success("Record Added to the Master Sheet!")
            # conn.create(spreadsheet=url, data=...) logic goes here
