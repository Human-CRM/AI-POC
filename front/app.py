import streamlit as st
import requests
import json

base_url = "http://fastapi-app:8000"

if "info_text" not in st.session_state:
    st.session_state["info_text"] = ""

def load_messages():
    global base_url
    try:
        server_answer = requests.get(url=f"{base_url}/messages")
        raw_msg:dict = json.loads(server_answer.text)
    except Exception:
        st.session_state["info_text"] = "Error parsing response"
        return
    
    st.session_state["info_text"] = ""

    if server_answer.status_code == 200:
        for i in range(0, len(raw_msg)):
            s:str = str(raw_msg[f"{i}"])
            list_msg = eval(s)
            st.session_state["info_text"] += list_msg[0] + "\n\n----------------------------\n\n" + list_msg[-1] + "\n\n----------------------------\n\n"
            #for msg in list_msg:
            #    st.session_state["info_text"] += msg + "\n\n"
            #st.session_state["info_text"] += "\n\n----------------------------\n\n"

def send_message():
    print(requests.post(url=f"{base_url}/messages/?user_input={st.session_state.user_input}"))
    load_messages()

def reset_messages():
    print(requests.delete(url=f"{base_url}/messages/"))
    load_messages()

st.set_page_config(page_title="Alfred")
st.header("Alfred")

st.markdown(st.session_state['info_text'])

with st.form(key="message_form", clear_on_submit=True):
    st.text_area(label="Message", key="user_input")
    st.form_submit_button('Send', on_click=send_message)

st.button(label="RESET", type="primary", icon="⚠️", on_click=reset_messages)