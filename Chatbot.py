

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

# Add checkbox column for selection
grouped_data.insert(0, 'Select', False)

# Display the dataframe
st.dataframe(grouped_data, use_container_width=True)





