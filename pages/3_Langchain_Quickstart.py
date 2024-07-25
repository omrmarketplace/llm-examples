
import streamlit as st
import openai

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7,
        max_tokens=150
    )
    message = response.choices[0].message["content"].strip()
    st.info(message)

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
