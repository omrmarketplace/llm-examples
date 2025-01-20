import streamlit as st
import requests
import pandas as pd
import json
import base64
from urllib.parse import urlencode

# Taboola API details
TABOOLA_API_URL = "https://backstage.taboola.com/backstage/api/1.0/{account_id}/reports"
CLIENT_ID = "YOUR_CLIENT_ID"  # Replace with your actual Client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Replace with your actual Client Secret
ACCOUNT_ID = "YOUR_ACCOUNT_ID"  # Replace with your actual Account ID

# Function to obtain an OAuth2 token
def get_oauth_token(client_id, client_secret):
    auth_url = "https://backstage.taboola.com/backstage/oauth/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(auth_url, data=auth_data)

    if response.status_code == 200:
        auth_response = response.json()
        return auth_response["access_token"]
    else:
        st.error(f"Failed to authenticate. Status code: {response.status_code}")
        return None

# Function to fetch Taboola ads data
def fetch_taboola_data(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Example request to get Taboola ads data (modify based on your needs)
    payload = {
        "start_date": "2025-01-01",  # Modify according to your data range
        "end_date": "2025-01-15",    # Modify according to your data range
        "granularity": "day",        # Can be hour, day, week, etc.
        "dimensions": ["campaign", "ad"],
        "metrics": ["impressions", "clicks", "revenue"]
    }

    response = requests.post(TABOOLA_API_URL.format(account_id=ACCOUNT_ID),
                             headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Function to process the response and return it as a DataFrame
def process_data_to_dataframe(data):
    if data:
        # Extracting data from the API response (adjust keys as needed)
        rows = []
        for entry in data.get('data', []):
            row = {
                "Campaign": entry.get('campaign'),
                "Ad": entry.get('ad'),
                "Impressions": entry.get('impressions'),
                "Clicks": entry.get('clicks'),
                "Revenue": entry.get('revenue')
            }
            rows.append(row)
        
        # Convert to DataFrame
        return pd.DataFrame(rows)
    return pd.DataFrame()

# Streamlit UI components
st.title("Taboola Ads Data Viewer")
st.write("This app fetches Taboola ads data and allows you to download it as a CSV.")

# Fetch data button
if st.button("Fetch Taboola Data"):
    # Step 1: Obtain OAuth token using Client ID and Client Secret
    access_token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)
    
    if access_token:
        # Step 2: Fetch Taboola ads data using the access token
        data = fetch_taboola_data(access_token)
        
        if data:
            # Process and display the data
            df = process_data_to_dataframe(data)
            
            if not df.empty:
                st.write(df)  # Show the fetched data in Streamlit
                
                # Provide download link for CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="taboola_ads_data.csv",
                    mime="text/csv"
                )
            else:
                st.write("No data available.")
        else:
            st.write("Failed to fetch Taboola data.")
    else:
        st.write("Failed to authenticate with the Taboola API.")
