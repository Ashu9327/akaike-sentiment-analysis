import streamlit as st
import requests
import json
import pyperclip

# Backend API URL
BASE_URL = "http://127.0.0.1:8001"

# Companies List
COMPANIES = ["Google", "Amazon", "Tesla", "Apple", "Microsoft"]

st.title("Company Sentiment Analysis")

# Clipboard for copying all data
def copy_all_data():
    all_data = {}
    for company in COMPANIES:
        sentiment = requests.get(f"{BASE_URL}/get_sentiment/{company}").json()
        all_data[company] = {"sentiment": sentiment}
    pyperclip.copy(json.dumps(all_data, indent=4))
    st.success("Copied all company data to clipboard!")

st.button("📋 Copy All Data", on_click=copy_all_data)

# Dropdown for selecting a company
selected_company = st.selectbox("Select a Company", COMPANIES)

if selected_company:
    sentiment_response = requests.get(f"{BASE_URL}/get_sentiment/{selected_company}")
    audio_url = f"{BASE_URL}/get_audio/{selected_company}"

    if sentiment_response.status_code == 200:
        sentiment_data = sentiment_response.json()
        
        st.subheader("📊 Sentiment Analysis")
        st.json(sentiment_data)
        
        # Clipboard for company sentiment data
        def copy_company_data():
            pyperclip.copy(json.dumps(sentiment_data, indent=4))
            st.success(f"Copied {selected_company} sentiment data!")
        
        st.button("📋 Copy Company Data", on_click=copy_company_data)
        
        # Play audio for sentiment summary
        st.audio(audio_url, format='audio/mp3')
    else:
        st.error("Failed to fetch data. Please check the backend.")
