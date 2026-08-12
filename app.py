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
st.write("Enter an ETF ticker to find its latest official fact sheet.")

# Get input and clean it up
raw_input = st.text_input("ETF Ticker", "VOO").strip()
ticker = raw_input.split()[0].upper() if raw_input else "VOO"

if st.button("Search for Fact Sheet"):
    # Broader query to capture both PDFs and official landing pages
    query = f"{ticker} ETF fact sheet"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"

    with st.spinner(f"Searching for {ticker} fact sheet..."):
        try:
            response = requests.get(url).json()
            items = response.get("items", [])

            if items:
                st.success(f"Top results for {ticker}:")
                # Display the top 3 matches so you can easily pick the right one
                for i, item in enumerate(items[:3], 1):
                    st.markdown(f"### {i}. [{item['title']}]({item['link']})")
                    st.caption(f"Source: {item['displayLink']}")
                    st.write("")
            else:
                st.warning(
                    f"No results found for '{ticker}'. \n\n"
                    "**Quick Checklist:**\n"
                    "1. Go to your [Google Programmable Search Engine Control Panel](https://programmablesearchengine.google.com/).\n"
                    "2. Select your search engine and make sure **'Search the entire web'** is toggled **ON**."
                )
        except Exception as e:
            st.error(f"An error occurred while searching: {e}")
