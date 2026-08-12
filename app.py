import streamlit as st
import yfinance as yf

# Set page config
st.set_page_config(page_title="ETF Fact Sheet Finder", page_icon="📄")

st.title("ETF Fact Sheet & Info Finder")
st.write(
    "Enter an ETF ticker symbol to instantly access its official resources,"
    " fact sheets, and fund details."
)

# Get input and clean it up
raw_input = st.text_input("ETF Ticker Symbol", "QQQM").strip()
ticker = raw_input.split()[0].upper() if raw_input else "QQQM"

if st.button("Find ETF Resources", type="primary"):
  with st.spinner(f"Gathering resources for {ticker}..."):
    # Fetch fund name using yfinance for context
    fund_name = ticker
    try:
      tk = yf.Ticker(ticker)
      info = tk.info
      fund_name = info.get("longName", info.get("shortName", ticker))
    except Exception:
      pass

    # Construct direct search URLs
    google_fact_sheet_url = (
        f"https://www.google.com/search?q={ticker}+ETF+fact+sheet+pdf"
    )
    yahoo_url = f"https://finance.yahoo.com/quote/{ticker}"
    sec_edgar_url = "https://www.sec.gov/edgar/searchedgar/companysearch"

    # --- DISPLAY RESULTS ---
    st.markdown("---")
    st.subheader(f"{fund_name} ({ticker})")

    st.markdown("### 🔗 Instant Access Links")
    st.markdown(
        f"📄 **[Click here to search Google for the official {ticker} Fact Sheet"
        f" PDF]({google_fact_sheet_url})**"
    )
    st.markdown(f"📈 **[View {ticker} on Yahoo Finance]({yahoo_url})**")
    st.markdown(f"📂 **[Search SEC EDGAR Filings]({sec_edgar_url})**")

    st.success(
        f"Successfully generated resource shortcuts for **{ticker}**!"
    )
