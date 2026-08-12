import requests
import streamlit as st

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

# Get input and clean it up (takes only the first word, e.g., "VOO" from "VOO Vanguard")
raw_input = st.text_input("ETF Ticker", "VOO").strip()
ticker = raw_input.split()[0].upper() if raw_input else "VOO"

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
                st.markdown(
                    f"### 📄 [Click here to open Fact Sheet PDF]({best_match['link']})"
                )
                st.caption(f"Source: {best_match['displayLink']}")
            else:
                st.warning(
                    f"Could not find a PDF fact sheet for '{ticker}'. Try a different ticker symbol."
                )
        except Exception as e:
            st.error(f"An error occurred while searching: {e}")
