from duckduckgo_search import DDGS
import streamlit as st

# Set page config
st.set_page_config(page_title="ETF Fact Sheet Finder", page_icon="📄")

st.title("ETF Fact Sheet Finder")
st.write(
    "Enter any ETF ticker symbol to search the web for its official fact sheet."
)

# Get input and clean it up
raw_input = st.text_input("ETF Ticker", "VOO").strip()
ticker = raw_input.split()[0].upper() if raw_input else "VOO"

if st.button("Search for Fact Sheet"):
  # Search query targeting fact sheet PDFs and official pages
  query = f"{ticker} ETF fact sheet pdf"

  with st.spinner(f"Searching the web for {ticker} fact sheet..."):
    try:
      results = []
      with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

      if results:
        st.success(f"Top results for {ticker}:")
        for i, item in enumerate(results, 1):
          title = item.get("title", "No Title")
          link = item.get("href", "#")
          body = item.get("body", "")

          st.markdown(f"### {i}. [{title}]({link})")
          if body:
            st.caption(body)
          st.markdown("---")
      else:
        st.warning(
            f"No results found for '{ticker}'. Try another ticker symbol."
        )
    except Exception as e:
      st.error(f"An error occurred while searching: {e}")
