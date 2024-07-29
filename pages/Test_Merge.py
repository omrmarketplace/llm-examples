from openai import OpenAI
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page configuration to use the full width of the page
st.set_page_config(layout="wide")

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

st.title("Read Google Sheet as DataFrame")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1x83yhdkzC10ddFqYmYIUQ1lSwURDGOZiQtvIhKb-45M/edit?usp=sharing"

data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


# Calculate profit
data['profit'] = data['conv_value'] - data['spend']

# Step 1: Aggregate all data by item_name without any filters
aggregated_data = data.groupby('item_name').agg({
    'content_provider_name': 'first',  # assuming each item has a single content provider
    'spend': 'sum',
    'profit': 'sum'
}).reset_index()

# Display the temporary DataFrame for verification
st.subheader("Aggregated Data (No Filters Applied)")
st.write(aggregated_data)

# Step 2: Apply filters after aggregation

# Content provider filter
content_provider_names = aggregated_data['content_provider_name'].unique()
selected_content_provider = st.selectbox("Select Content Provider", content_provider_names)

# Spend floor filter
max_spend = aggregated_data['spend'].max()
spend_floor = st.slider("Set Spend Floor", min_value=0.0, max_value=float(max_spend), value=0.0)

# Profit filter (only positive profits)
filtered_data = aggregated_data[
    (aggregated_data['content_provider_name'] == selected_content_provider) &
    (aggregated_data['spend'] >= spend_floor) &
    (aggregated_data['profit'] > 0)
]

# Display the filtered DataFrame
st.subheader("Profitable Items")
st.write(filtered_data)

# Calculate total metrics after filtering
total_spend = filtered_data['spend'].sum()
total_profit = filtered_data['profit'].sum()

# Display total metrics
st.subheader("Total Metrics")
st.write(f"Total Spend: ${total_spend:,.2f}")
st.write(f"Total Profit: ${total_profit:,.2f}")


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

# Display the parsed response in a DataFrame
if "response" in st.session_state:
    # Extract the 'content' from the response object
    content = st.session_state.response.choices[0].message.content

    # Convert the content to a DataFrame
    data = {"Response": [content]}  # Create a dictionary to structure the DataFrame
    df = pd.DataFrame(data)  # Create a DataFrame

    # Display the DataFrame in Streamlit
    st.subheader("Response Data")
    st.dataframe(df)