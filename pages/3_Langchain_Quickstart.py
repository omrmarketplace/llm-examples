import streamlit as st
from langchain.llms import OpenAI

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"



def generate_response(input_text):
  client = OpenAI(api_key=openai_api_key)  # Assuming your API key is stored

  # Define the few-shot learning prompt
  prompt = {
      "model": "gpt-4-turbo",  # Update with a supported model if needed
      "messages": [
          {
              "role": "system",
              "content": [
                  {
                      "type": "text",
                      "text": "Your task is to take the successful advertising headline provided and create 3 variants that hit on the same core value propositions. You can use synonyms for the core value propositions such as:\n\nA value proposition of 18 months free could also be:\nFree until 2026 (based on the current date of the task request). If it was April 2024, you could say \"free until nearly 2026\"\n\nA value proposition of 0% APR credit card could also be:\nNo interest, Pause your credit card interest, or halt interest\n\nWhen there is an offer in the advertisement that could be localized, use the dynamic replacement ${region:capitalized}$ in the refreshed creatives, where relevant. Credit card offers would not be a local offer. But home insurance would be a local offer.\n\nIn Native advertising it is EXTREMELY IMPORTANT that you probe curiosity in the user. Here are some ways to do this that you can incorporate into your refreshes:\n1. Use language that hints at a unique truth such as: the real truth, what something actually costs, why something suddenly is so cheap, etc. - with the key words of addition there being \"real\", \"actually\", and \"suddenly\"\n\n2. Use english slang for superlative synonyms such as: hands down, absolutely, must-have, can't-miss, slam dunk, no brainer, etc.\n\n"
                  }
              ]
          },
          {
              "role": "user",
              "content": [
                  {
                      "text": "A Top Pick: A Credit Card Winner with Good Credit",
                      "type": "text"
                  }
              ]
          },
          {
              "role": "assistant",
              "content": [
                  {
                      "text": "Absolutely One of the Best Cards for Those with Good Credit\nWhy This Top Credit Card For Good Credit Is A No Brainer\nUndoubtedly One of the Premier Credit Cards for Good Credit Holders",
                      "type": "text"
                  }
              ]
          },
          {
              "role": "user",
              "content": input_text  # User input goes here
          }
      ],
      "temperature": 0.52,
      "max_tokens": 256,
      "top_p": 1,
      "frequency_penalty": 0.63,
      "presence_penalty": 0
  }

  # Generate response using chat completions
  response = client.chat.completions.create(**prompt)
  return response.choices[0].message['content']


with st.form("my_form"):
    input_text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(input_text)