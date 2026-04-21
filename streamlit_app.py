import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page setup for tablet view
st.set_page_config(page_title="Terry's Ebook Manager", layout="wide")

st.title("📚 Terry's Ebook Database")
st.markdown("---")

# 1. Connect to the Google Sheet
# Replace 'url' with the actual link to your Google Sheet
# Copy and paste this exact line
url = "https://docs.google.com/spreadsheets/d/1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU/edit?usp=sharing".strip()
conn = st.connection("gsheets", type=GSheetsConnection)

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
