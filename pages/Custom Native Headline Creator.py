from openai import OpenAI
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# Set page configuration to use the full width of the page
st.set_page_config(layout="wide")

with st.sidebar:
    api_key = st.secrets["openai"]["OPENAI_API_KEY"]

st.title("💬 Custom Headline Refresher")
st.caption("🚀 AI powered headline refresh tool. Every 2000 headlines you refresh costs us about $5")




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
                "content": input_text
            }
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

# Streamlit input for user to provide headline
input_text = st.text_area("Enter your advertising headline here:")

# Button to generate variants
if st.button("Generate Variants"):
    if input_text:
        response_content = generate_response(input_text)
        st.subheader("Generated Variants")
        
        # Split response content by line breaks
        variants = response_content.split("\n") 
        
        # Prepare the DataFrame
        df_variants = pd.DataFrame(variants, columns=["Generated Variants"])
        
        # Replace newlines and special characters with semicolons
        df_variants["Generated Variants"] = df_variants["Generated Variants"].apply(lambda x: x.replace("\n", ";"))
        
        # Display the DataFrame as a table
        st.write(df_variants)
    else:
        st.warning("Please enter a headline to generate variants.")
