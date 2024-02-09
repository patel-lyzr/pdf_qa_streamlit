from PIL import Image

import streamlit as st
import tempfile
import os
import time
from lyzr import ChatBot

st.set_page_config(
    page_title="Lyzr QA Bot",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load and display the logo
image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr QA-Bot Demo")
st.markdown("### Welcome to the Lyzr QA-Bot!")
st.markdown("Upload an pdf and Ask your queries.")

# Instruction for the users
st.markdown("#### 📄 Upload a Pdf")

# Input for API key
api_key = st.sidebar.text_input("API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    # Prompt for API key if not provided
    st.sidebar.warning("Please enter your API key to proceed.")

uploaded_files = st.file_uploader(
    "Choose PDF files", type=["pdf"], accept_multiple_files=True
)
pdf_file_paths = []  # This will store paths to the saved files

if uploaded_files:
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            tmpfile.write(uploaded_file.getvalue())
            pdf_file_paths.append(tmpfile.name)

    # Update session state with new PDF file paths
    st.session_state.pdf_file_paths = pdf_file_paths

    # Generate a unique index name based on the current timestamp
    unique_index_name = f"IndexName_{int(time.time())}"
    vector_store_params = {"index_name": unique_index_name}
    st.session_state["chatbot"] = ChatBot.pdf_chat(
        input_files=pdf_file_paths, vector_store_params=vector_store_params
    )

    # Inform the user that the files have been uploaded and processed
    st.success("PDFs uploaded and processed. You can now interact with the chatbot.")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "chatbot" in st.session_state:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.session_state["chatbot"].chat(prompt)
            chat_response = response.response
            response = st.write(chat_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": chat_response}
        )
else:
    st.warning("Please upload PDF files to continue.")


# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """
    This app uses Lyzr Core to generate notes from transcribed audio. The audio transcription is powered by OpenAI's Whisper model. For any inquiries or issues, please contact Lyzr.

    """
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
