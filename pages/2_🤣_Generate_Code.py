import traceback

from services import prompts
import streamlit as st
from openai import OpenAI
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import asyncio
from helpers import util
from services.llm import converse, converse_2

st.set_page_config(
    page_title="Code Editor Tutorial: Advanced Code Editor",
    page_icon="📄",
    layout="wide",
    # initial_sidebar_state="collapsed"
)
import helpers.sidebar
helpers.sidebar.show()

# st.sidebar.title(":memo: Editor settings")
# st.title("Code Editor Tutorial: Advanced Code Editor")
# st.warning("Note: Select different button below to interact your code with the LLM!")

# Every time we reload the page, make a new editor with a new id
EDITOR_KEY_PREFIX = "ace-editor"
if 'editor_id' not in st.session_state:
    st.session_state.editor_id = 0

# Empty code on first run
if "code" not in st.session_state:
    st.session_state.code = ""

if "followups" not in st.session_state:
    st.session_state.followups = []

# This is how we update code in the editor - saving it in a session variable "code".
INITIAL_CODE = st.session_state.code

# The component parameters are documented in the Streamlit Ace documentation
# Command-Click on the st_ace function to see the documentation in PyCharm
# (Ctrl-Click on Windows)

st.write(f"#### Code Editor ID: {st.session_state.editor_id}")
code = st_ace(
    value=INITIAL_CODE,
    language=st.sidebar.selectbox("Language mode", options=LANGUAGES, index=121),
    placeholder="Placeholder text when no code is present",
    theme=st.sidebar.selectbox("Theme", options=THEMES, index=25),
    keybinding=st.sidebar.selectbox(
        "Keybinding mode", options=KEYBINDINGS, index=3
    ),
    font_size=st.sidebar.slider("Font size", 5, 24, 14),
    tab_size=st.sidebar.slider("Tab size", 1, 8, 4),
    wrap=st.sidebar.checkbox("Wrap lines", value=False),
    show_gutter=st.sidebar.checkbox("Show gutter", value=True),
    show_print_margin=st.sidebar.checkbox("Show print margin", value=True),
    auto_update=st.sidebar.checkbox("Auto update", value=True),
    readonly=st.sidebar.checkbox("Read only", value=False),
    key=f"{EDITOR_KEY_PREFIX}-{st.session_state.editor_id}",
    height=300,
    min_lines=12,
    max_lines=20
)

# Let's save the code in session state as the value changes
st.session_state.code = code

# print("STATE", st.session_state, "INITIAL", INITIAL_CODE, "CURRENT", code)

# Let's pretend we are modifying that code...and handle errors
try:
    modified_code = code + "\n# Modified code"
    st.session_state.code = modified_code
except Exception as e:
    traceback.print_exc()
    st.error(icon="🔥", body=f":red[Error encountered: {e}]")
    st.session_state.code = code

# Read code from the editor
# st.write("The code you've written in the editor is:")
# st.code(code, language="python")

# Read code from session state
# st.write("The code you've pretended to modify is:")
# st.code(st.session_state.code, language="python")

col1, col2, col3, col4 = st.columns(4)
reload_button = col1.button("🛜 Reload Page", help="⚠️CAREFUL! Code won't be saved")
review_button = col2.button("🧐 Review Code")
debug_button = col3.button("🐞 Debug Code")
modify_button = col4.button("🖊️ Modify Code")

info = ""

if reload_button:
    # Clear the session code
    del st.session_state['code']
    # del st.session_state['llm_response']
    del st.session_state['followups']
    # Clear the editor component by id
    for k in st.session_state.keys():
        if k.startswith(EDITOR_KEY_PREFIX):
            del st.session_state[k]
    # Increment the editor id
    st.session_state.editor_id += 1
    # Restart the page
    st.rerun()

if review_button:
    response, messages = converse_2(prompts.review_prompt(code))
    initial_messages = [{"role": "assistant", "content": response}]
    st.session_state.followups = initial_messages

if debug_button:
    response, messages = converse_2(prompts.debug_prompt(code))
    initial_messages = [{"role": "assistant", "content": response}]
    st.session_state.followups = initial_messages


if modify_button:
    response, messages = converse_2(prompts.modify_code_prompt(code))
    initial_messages = [{"role": "assistant", "content": response}]
    st.session_state.followups = initial_messages


"""    
* Click BUTTON to start a NEW conversation with your code
* Then use chatbot continue with follow up questions.
"""

# Print all messages in the session state?? show the conversation
for message in [m for m in st.session_state.followups]:# if m["role"] != "system"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat with the LLM, and update the messages list with the response.
# Handles the chat UI and partial responses along the way.
async def chat(messages):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        messages = await util.run_conversation(messages, message_placeholder)
        st.session_state.messages = messages
    return messages

# React to the user prompt
if prompt := st.chat_input("Ask a coding question..."):
    st.session_state.followups.append({"role": "user", "content": prompt})
    asyncio.run(chat(st.session_state.followups))


