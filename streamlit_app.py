import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Terry's Ebook Database", layout="wide")

# This CSS makes the app look more like a Windows program (tighter spacing)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stApp { max-width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Ebook Database Management System")

SHEET_ID = "1BnFTueD2eJABxOOuhkgga0pDRz4fpJCY6Qj49ICZ5eU"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Ebook%20Requests"

try:
    df = pd.read_csv(url)
    
    # 1. Configure the "Windows-style" Grid
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Make columns sortable and filterable like Excel
    gb.configure_default_column(resizable=True, filterable=True, sortable=True, editable=False)
    
    # Pin the ID and Title so they stay put when scrolling right
    gb.configure_column("ID Number", pinned='left', width=100)
    gb.configure_column("Book Title", pinned='left', width=250)
    
    # Enable Pagination (First/Last buttons)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    
    # Enable the "Side Bar" for quick filters
    gb.configure_side_bar()
    
    gridOptions = gb.build()

    # 2. Display the Grid
    AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme='balham', # 'balham' is the theme that looks most like a Windows App
        height=700,
        width='100%'
    )

except Exception as e:
    st.error(f"Error connecting: {e}")
