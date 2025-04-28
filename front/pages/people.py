import requests
import json
import pandas as pd
import random

import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet

from albert_helper import albert


base_url = "http://fastapi-app:8000"

#############################
#                           #
#       HELPER FUNCS        #
#                           #
#############################

def load_spreadsheet():
    df = st.session_state["people_df"]
    sheet_key = st.session_state.get("mito_key", "initial")
    sheets, _ = spreadsheet(df, key=sheet_key)  # key ensures refresh
    sheet_names = list(sheets.keys())
    people_df = sheets[sheet_names[0]]
    st.session_state["people_df"] = people_df
    return people_df

def add_row():
    df: pd.DataFrame = st.session_state["people_df"]
    df.loc[len(df)] = pd.Series(dtype='object')
    st.session_state["people_df"] = df

def export_people_df():
    people_df: pd.DataFrame = st.session_state["people_df"]
    people_df_json = people_df.to_json()
    requests.put(f"{base_url}/people_db", data=people_df_json)

def refresh_people_df():
    response = requests.get(f"{base_url}/people_db")
    if response.status_code == 200:
        st.session_state["people_df"] = pd.DataFrame(json.loads(response.text))
        # Change mito_key to force spreadsheet reload
        st.session_state["mito_key"] = str(random.randint(0, 1000000))

###########################
#                         #
#       PEOPLE PAGE       #
#                         #
###########################

st.set_page_config(page_title="H/UMAN", layout="wide")
st.header("CRM - People")
albert()

if "people_df" not in st.session_state:
    refresh_people_df()

if "people_df" in st.session_state:
    load_spreadsheet()

col1, col2, col3 = st.columns(3)

with col1:
    st.button(label="Add Row", on_click=add_row)

with col2:
    st.button(label="Export db", on_click=export_people_df)

with col3:
    st.button(label="Refresh db", on_click=refresh_people_df)