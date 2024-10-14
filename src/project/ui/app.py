import os
import time

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from google.generativeai.types import HarmBlockThreshold, HarmCategory

load_dotenv()

# Initialize model client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL")
IMG_PATH = os.getenv("IMG_PATH")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
            GEMINI_CHAT_MODEL,
            system_instruction="You are a helpful assistant named Github PI who is also a Github expert. Respond like you are a Private Investigator."
        )

# Safety settings
safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH
}

# Set Tab title
st.set_page_config(page_title="Github PI", page_icon=":robot_face:")

# Add custom CSS styles
st.markdown(
    """
    <style>
    .sidebar-content {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50px;
    }
    .sidebar-content button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Function to reset chat
def reset_chat():
    st.session_state.chat_session = model.start_chat(history=[])


# Function to transform chat history to Gemini format
def transform_history(history):
    conversation_history = []

    for h in history:
        conversation_history.append(
                {
                    'role': 'user' if h['role'] == 'user' else 'model',
                    'parts': [{'text': h['content']}]}
                )

    return conversation_history


# Streamlit components setup
st.title("Github PI")
expander = st.expander("Disclaimer", icon="ℹ️")
expander.write('''
    The information displayed is summary generated by Gemini AI
    trained on Github repository readme files.
    Trust the contents at your own discretion.
''')
octo_img_url = IMG_PATH + '/octocat-1728395775384.png'
with st.sidebar:
    st.markdown("<h1 class='sidebar-content'>!Github Inc.</h1>",
                unsafe_allow_html=True)

st.sidebar.image(octo_img_url)
st.sidebar.button("Reset Chat", on_click=reset_chat, use_container_width=True)
st.sidebar.title("About")
st.sidebar.info("Github PI is presented by: Group-11 => Anand, Finn, Georgios & Markus")
# Initialize chat history
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat history on rerun
for message in st.session_state.chat_session.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user prompt to chat history
    request = {"role": "user", "content": prompt}
    st.session_state.chat_session.history.append(request)

    chat = model.start_chat(history=[])
    # Initialize chat history
    chat.history = transform_history(st.session_state.chat_session.history)
    stream = chat.send_message(prompt, stream=True, safety_settings=safety_settings)
    # Generate streamed assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = ""
        for chunk in stream:
            for ch in chunk.text.split(' '):
                response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(response + ' ')
        message_placeholder.write(response)
    # Add assistant response to chat history
    st.session_state.chat_session.history.append(
            {"role": "assistant", "content": response}
            )
    print(f"[*] INFO: History: {st.session_state.chat_session.history}")
