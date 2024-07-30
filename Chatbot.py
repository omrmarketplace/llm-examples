from openai import OpenAI
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# Set page configuration to use the full width of the page
st.set_page_config(layout="wide")

openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

st.title("💬 Native Advertising Headline Refresh")
st.caption("🚀 AI powered headline refresh tool")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1x83yhdkzC10ddFqYmYIUQ1lSwURDGOZiQtvIhKb-45M/edit?usp=sharing"

data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


# Calculate profit
data['profit'] = data['conv_value'] - data['spend']

# Filter by content_provider_name
content_provider_names = data['content_provider_name'].unique()
selected_content_provider = st.selectbox("Select Buyside Account", content_provider_names)

# Filter data based on selected content provider
filtered_data = data[data['content_provider_name'] == selected_content_provider]

# Group by item_name and calculate total profit and spend
grouped_data = filtered_data.groupby('item_name').agg({
    'spend': 'sum',
    'profit': 'sum'
}).reset_index()

# Set up profit filter slider
min_profit = float(grouped_data['profit'].min())
max_profit = float(grouped_data['profit'].max())
if min_profit == max_profit:
    max_profit += 1  # Ensure slider has a range
profit_floor = st.slider(
    "Set Minimum Required Profit (default is 0)", 
    min_value=min_profit, 
    max_value=max_profit, 
    value=min_profit,
    key="profit_slider"
)

# Filter out rows where profit is less than profit_floor
profitable_data = grouped_data[grouped_data['profit'] > profit_floor]

# Set up spend filter slider after grouping
min_spend = float(profitable_data['spend'].min())
max_spend = float(profitable_data['spend'].max())
if min_spend == max_spend:
    max_spend += 1  # Ensure slider has a range
spend_floor = st.slider(
    "Set Minimum Required Spend (starts at the lowest profitable headline spend amount)", 
    min_value=min_spend, 
    max_value=max_spend, 
    value=min_spend,
    key="spend_slider"
)


# Apply spend floor filter to the already calculated profitable_data
final_profitable_data = profitable_data[profitable_data['spend'] >= spend_floor]

# Sort the final data by profit in descending order
final_profitable_data = final_profitable_data.sort_values(by='profit', ascending=False)

# Display the filtered DataFrame
st.subheader("Profitable Headlines")
st.write(final_profitable_data)

client = OpenAI(api_key=openai_api_key)

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

def generate_variants():
    # Iterate over each item_name in final_profitable_data and generate response
    responses = []
    for index, row in final_profitable_data.iterrows():
        item_name = row['item_name']
        response_content = generate_response(item_name)
        responses.append({"Item Name": item_name, "Generated Response": response_content})

    # Convert the list of responses to a DataFrame
    response_df = pd.DataFrame(responses)
    
    # Store the generated responses in session state to avoid regeneration on re-renders
    st.session_state.response_df = response_df

# Button to generate variants
if st.button("Generate Variants"):
    generate_variants()

# Display the responses DataFrame if available
if 'response_df' in st.session_state:
    st.subheader("Generated Responses for Profitable Items")
    st.write(st.session_state.response_df)
