import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet

from albert_helper import albert

#########################
#                       #
#       HELPER FUNC     #
#                       #
#########################

def load_spreadsheet(crm_data):
    df = pd.DataFrame(crm_data)
    sheets, _ = spreadsheet(df)
    sheet_names = [name for name in dict(sheets).keys()]
    org_df = sheets[sheet_names[0]]
    return org_df


def add_row():
    df:pd.DataFrame = st.session_state["org_df"]
    df.loc[len(df)] = pd.Series(dtype='object')
    st.session_state["org_df"] = df


def remove_row(row_index):
    df = st.session_state["org_df"]
    if row_index >= 0 and row_index < len(df):
        df = df.drop(row_index)
    st.session_state["org_df"] = df


def get_org_df():
    org_df = pd.DataFrame(st.session_state["org_df"])
    org_df.dropna(axis=0, inplace=True)
    return org_df


##################################
#                                #
#       ORGANIZATIONS PAGE       #
#                                #
##################################

st.set_page_config(page_title="H/UMAN", layout="wide")
st.header("CRM - Organizations")
albert()

if "org_df" not in st.session_state:
    crm_data = {
        "id": [],
        "Name": [],
        "Domain": [],
        "Industry": [],
        "Description": [],
    }
    st.session_state["org_df"] = pd.DataFrame(crm_data)


st.session_state["org_df"] = load_spreadsheet(st.session_state["org_df"])

st.button(label="Add Row", on_click=add_row)
