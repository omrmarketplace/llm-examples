
import streamlit as st
import openai

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


openai.api_key = openai_api_key

def generate_response(input_text):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=input_text,
        temperature=0.7,
        max_tokens=150
    )
    message = response.choices[0].text.strip()
    st.info(message)

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)

