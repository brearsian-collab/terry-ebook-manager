import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# 1. Force the layout to look like a Desktop Window
st.set_page_config(page_title="Ebook Management", layout="wide")

# This hides the 'made with streamlit' footer to make it feel like a private app
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(url)
    
    # 2. Build the Desktop UI Logic
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Enable the "Excel" features
    gb.configure_default_column(
        resizable=True, 
        filterable=True, 
        sortable=True, 
        groupable=True
    )
    
    # PIN columns just like a Windows freeze-pane
    gb.configure_column("ID Number", pinned='left', width=90)
    gb.configure_column("First Name", width=120)
    gb.configure_column("Surname", width=120)
    gb.configure_column("Book Title", pinned='left', width=300)
    
    # Setup Pagination (the "First/Last" buttons)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)
    
    gridOptions = gb.build()

    # 3. Render the specialized Grid
    AgGrid(
        df,
        gridOptions=gridOptions,
        theme='balham', # This is the "Windows Professional" theme
        height=750, 
        width='100%',
        reload_data=False
    )

except Exception as e:
    st.error("The system is currently connecting to the data source. Please wait 30 seconds.")
