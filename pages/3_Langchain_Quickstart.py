import streamlit as st
from langchain.llms import OpenAI

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

client = OpenAI(api_key=openai_api_key)

# Function to generate response using OpenAI API
def generate_response(input_text):
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Make sure to use an available model
        messages=[
            {
                "role": "system",
                "content": "Your task is to take the successful advertising headline provided and create 3 variants that hit on the same core value propositions. Use synonyms for core value propositions and probe curiosity in the user."
            },
            {
                "role": "user",
                "content": "A Top Pick: A Credit Card Winner with Good Credit"
            },
            {
                "role": "assistant",
                "content": "Absolutely One of the Best Cards for Those with Good Credit\nWhy This Top Credit Card For Good Credit Is A No Brainer\nUndoubtedly One of the Premier Credit Cards for Good Credit Holders"
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=0.52,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.63,
        presence_penalty=0
    )
    return response.choices[0].message['content']

# Streamlit form for user input
with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        generate_response(text)
