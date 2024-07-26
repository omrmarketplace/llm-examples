

from openai import OpenAI
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Set page configuration to use the full width of the page
st.set_page_config(layout="wide")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

st.title("Read Google Sheet as DataFrame")



conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1x83yhdkzC10ddFqYmYIUQ1lSwURDGOZiQtvIhKb-45M/edit?usp=sharing"

data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])





