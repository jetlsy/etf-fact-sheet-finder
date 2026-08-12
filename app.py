import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="ETF Fact Sheet Finder", page_icon="📄")

# Accessing keys from Streamlit Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    SEARCH_ENGINE_ID = st.secrets["SEARCH_ENGINE_ID"]
except Exception as e:
    st.error("API keys not found. Please set them in Streamlit Secrets.")
    st.stop()

st.title("ETF Fact Sheet Finder")
st.write("Enter an ETF ticker to find its latest official fact sheet PDF.")

ticker = st.text_input("ETF Ticker", "VOO").upper()

if st.button("Search for Fact Sheet"):
    # Google Custom Search API request
    query = f"{ticker} ETF fact sheet filetype:pdf"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    
    with st.spinner(f"Searching for {ticker} fact sheet..."):
        try:
            response = requests.get(url).json()
            items = response.get("items", [])
            
            if items:
                # Get the first result
                best_match = items[0]
                st.success(f"Found match: {best_match['title']}")
                st.markdown(f"### 📄 [Click here to open Fact Sheet PDF]({best_match['link']})")
                st.caption(f"Source: {best_match['displayLink']}")
            else:
                st.warning(f"Could not find a PDF fact sheet for '{ticker}'. Try adding the provider name (e.g., '{ticker} Vanguard').")
        except Exception as e:
            st.error(f"An error occurred while searching: {e}")
