import streamlit as st

from albert_helper import albert

#########################
#                       #
#       MAIN PAGE       #
#                       #
#########################

st.set_page_config(page_title="H/UMAN", layout="wide")
st.header("H/UMAN CRM")
albert()

st.write("Welcome to the H/UMAN, powered by AI.\nPlease choose a page to start !")
