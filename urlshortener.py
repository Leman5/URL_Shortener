import streamlit as st
import requests

API_ENDPOINT = "http://localhost:8000/shorten"

st.header("BESTest URL Shortener")

url = st.text_input("Enter the URL to shorten:", placeholder="https://example.com")

if st.button("Submit"):
    if url:
        try:
            response = requests.post(API_ENDPOINT, json={"url": url})
            if response.status_code == 200:
                short_url = response.json().get("short_url")
                st.success(f"Shortened URL: {short_url}")
            else:
                st.error("Failed to shorten URL.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid URL.")
