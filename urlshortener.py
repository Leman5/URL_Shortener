# import streamlit as st
# import requests

# st.header("BESTest URL Shortener")

# def shorten_url(url):
#     return url



# url = st.text_input("Enter the URL to shorten:",placeholder="https://example.com")
# url_json = {"url": url}
# if st.button("Submit"):
#     if url:
#         # Here you would call the API to shorten the URL
#         r = requests.post("http://localhost:8000/shorten", json=url_json)
#         short_url = shorten_url(url)
#         st.success(f"Shortened URL: {short_url}")
#     else:
#         st.error("Please enter a valid URL.")

import pyperclip




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
                st.success(f"Shortened URL: [{short_url}]({short_url})", icon="🔗")
                if st.button("Copy"):
                    pyperclip.copy(short_url)
                    st.toast("Copied!")
            else:
                st.error("Failed to shorten URL.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid URL.")