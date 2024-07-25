import streamlit as st
from openai import OpenAI


st.title("🦜🔗 Native Headline Refresh Tool")

with st.sidebar:
    api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

client = OpenAI(api_key=api_key)
def generate_response(input_text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Your task is to take the successful advertising headline provided and create 3 variants that hit on the same core value propositions. You can use synonyms for the core value propositions such as:\n\nA value proposition of 18 months free could also be:\nFree until 2026 (based on the current date of the task request). If it was April 2024, you could say \"free until nearly 2026\"\n\nA value proposition of 0% APR credit card could also be:\nNo interest, Pause your credit card interest, or halt interest\n\nWhen there is an offer in the advertisement that could be localized, use the dynamic replacement ${region:capitalized}$ in the refreshed creatives, where relevant. Credit card offers would not be a local offer. But home insurance would be a local offer.\n\nIn Native advertising it is EXTREMELY IMPORTANT that you probe curiosity in the user. Here are some ways to do this that you can incorporate into your refreshes:\n1. Use language that hints at a unique truth such as: the real truth, what something actually costs, why something suddenly is so cheap, etc. - with the key words of addition there being \"real\", \"actually\", and \"suddenly\"\n\n2. Use english slang for superlative synonyms such as: hands down, absolutely, must-have, can't-miss, slam dunk, no brainer, etc.\n\n"
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
                "content": text
            }
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


# Create a form in the Streamlit app
with st.form("my_form"):
    text = st.text_area("Enter your prompt:", "What are 3 key pieces of advice for learning how to code?", height=150)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.response = generate_response(text)  # Store response in session state

# Display the parsed response
if "response" in st.session_state:
        st.write(generate_response(text))