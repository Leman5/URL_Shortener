import streamlit as st

st.header("BESTest URL Shortener")

def shorten_url(url):
    return url

url = st.text_input("Enter the URL to shorten:",placeholder="https://example.com")
if st.button("Submit"):
    if url:
        short_url = shorten_url(url)
        st.success(f"Shortened URL: {short_url}")
    else:
        st.error("Please enter a valid URL.")


