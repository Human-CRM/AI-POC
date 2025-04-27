import requests
import json

import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet

from albert_helper import albert

base_url = "http://fastapi-app:8000"

#########################
#                       #
#       HELPER FUNC     #
#                       #
#########################

def load_spreadsheet():
    df = st.session_state["org_df"]
    sheets, _ = spreadsheet(df)
    sheet_names = [name for name in dict(sheets).keys()]
    org_df = sheets[sheet_names[0]]
    st.session_state["org_df"] = org_df
    return org_df


def add_row():
    df:pd.DataFrame = st.session_state["org_df"]
    df.loc[len(df)] = pd.Series(dtype='object')
    st.session_state["org_df"] = df


def export_org_df():
    org_df: pd.DataFrame = st.session_state["org_df"]
    org_df_json = org_df.to_json()
    requests.put(f"{base_url}/org_db", data=org_df_json)


def refresh_org_df():
    response = requests.get(f"{base_url}/org_db")
    if response.status_code==200:
        st.session_state["org_df"] = pd.DataFrame(json.loads(response.text))
        

##################################
#                                #
#       ORGANIZATIONS PAGE       #
#                                #
##################################

st.set_page_config(page_title="H/UMAN", layout="wide")
st.header("CRM - Organizations")
albert()

if "org_df" not in st.session_state:
    refresh_org_df()

if "org_df" in st.session_state:
    st.session_state["org_df"] = load_spreadsheet()

col1, col2, col3 = st.columns(3)

with col1:
    st.button(label="Add Row", on_click=add_row)

with col2:
    st.button(label="Export db", on_click=export_org_df)

with col3:
    st.button(label="Refresh db", on_click=refresh_org_df)