from openai import OpenAI
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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

# Calculate profit
data['profit'] = data['conv_value'] - data['spend']

# Streamlit UI components
st.title("Profitable Items Analysis")

# Filter by content_provider_name
content_provider_names = data['content_provider_name'].unique()
selected_content_provider = st.selectbox("Select Content Provider", content_provider_names)

# Spend floor slider
spend_floor = st.slider("Set Spend Floor", min_value=float(data['spend'].min()), max_value=float(data['spend'].max()), value=float(data['spend'].min()))

# Filter data based on selections
filtered_data = data[(data['content_provider_name'] == selected_content_provider) & (data['spend'] >= spend_floor)]

# Group by item_name and calculate total profit and spend
grouped_data = filtered_data.groupby('item_name').agg({
    'spend': 'sum',
    'profit': 'sum'
}).reset_index()

# Sort by profit
grouped_data = grouped_data.sort_values(by='profit', ascending=False)

# Filter out rows where profit is less than or equal to 0
profitable_data = grouped_data[grouped_data['profit'] > 0]

# Display the filtered DataFrame
st.subheader("Profitable Items")
st.write(profitable_data)

# Select an item_name to extract its profit and spend
selected_item_name = st.selectbox("Select Item Name", profitable_data['item_name'])

# Extract values for the selected item name
selected_item_data = profitable_data[profitable_data['item_name'] == selected_item_name]

with st.sidebar:
    api_key = st.secrets["openai"]["OPENAI_API_KEY"]
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Function to generate response using OpenAI API
def generate_response(input_text):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4",
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
    return response

# Generate response for the selected item name
if st.button("Generate Response"):
    response = generate_response(selected_item_name)
    st.subheader("Generated Response")
    st.write(response)
