import streamlit as st

import helpers.sidebar
import streamlit as st
from streamlit_modal import Modal
import os

st.set_page_config(
	page_title="HooHack",
	page_icon="💸",
	layout="wide"
)

modal = Modal(key="Demo Key",title="Log you in", max_width=600)
# for col in st.columns(8):
#     with col:
# if os.getenv('OPENAI_API_KEY') is None:
# open_modal = st.button(label='Log in', key='modal-button')
# if open_modal:
# 	with modal.container():
# 		user_input = st.text_input(
# 				"Please enter you openai key:",
# 				"",
# 				key="placeholder",
# 			)
# 		st.button("Submit", key="submit")
# 		# if st.button("Submit", key="submit"):
	
# 		os.environ['OPENAI_API_KEY'] = user_input
# 		print(f"api_key2: {os.getenv('OPENAI_API_KEY')}")

modal = Modal(key="Demo Key", title="Log you in", max_width=600)
open_modal = st.button(label='Log in', key='modal-button')

if open_modal:
    with modal.container():
        user_input = st.text_input("Please enter your openai key:",
                                   disabled=st.session_state.disabled,
       								 placeholder=st.session_state.placeholder,
                                     key="placeholder")
        submitted = st.button("Submit", key="submit")  # Capture the submit action

        if submitted:
            # Set the environment variable here
            os.environ['OPENAI_API_KEY'] = user_input
            # Optionally, display the API key, but be cautious with this for security reasons
            print(f"API Key set: {user_input}")  # Note: For security, generally avoid printing the full API key.

helpers.sidebar.show()

st.toast("Welcome to HooHack!", icon="💸")

st.markdown("Welcome to HooHack, your AI-powered personal coding assistant!")
st.write("HooHack is designed to help you explore and understand your coding problems.")

