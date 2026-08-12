import streamlit as st
import yfinance as yf

# Set page config
st.set_page_config(page_title="ETF Fact Sheet Finder", page_icon="📄")

# Curated lookup map for instant direct PDF/resource links
DIRECT_PDF_MAP = {
    "JEPQ": (
        "JPMorgan Nasdaq Equity Premium Income ETF",
        "https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/fact-sheet/etfs/FS-JEPQ.PDF",
    ),
    "JEPI": (
        "JPMorgan Equity Income ETF",
        "https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/fact-sheet/etfs/FS-JEPI.PDF",
    ),
    "QQQM": (
        "Invesco NASDAQ 100 ETF",
        "https://www.invesco.com/us/en/insights/qqqm-innovation-long-term.html",
    ),
    "VOO": (
        "Vanguard S&P 500 ETF",
        "https://investor.vanguard.com/investment-products/etfs/profile/voo#literature",
    ),
    "SPY": (
        "SPDR S&P 500 ETF Trust",
        "https://www.ssga.com/us/en/intermediary/etfs/funds/spdr-sp-500-etf-trust-spy",
    ),
}

st.title("ETF Fact Sheet PDF Finder")
st.write(
    "Enter an ETF ticker symbol to instantly access its official fact sheet"
    " and download links."
)

raw_input = st.text_input("ETF Ticker Symbol", value="JEPQ").strip()
ticker = raw_input.split()[0].upper() if raw_input else "JEPQ"

if st.button("Get Fact Sheet", type="primary"):
  with st.spinner(f"Retrieving fact sheet for {ticker}..."):
    # Fetch fund name via yfinance for clean display
    fund_name = ticker
    try:
      tk = yf.Ticker(ticker)
      info = tk.info
      fund_name = info.get("longName", info.get("shortName", ticker))
    except Exception:
      pass

    st.markdown("---")
    st.subheader(f"{fund_name} ({ticker})")

    # Check if we have a direct verified link in our map
    if ticker in DIRECT_PDF_MAP:
      name, link = DIRECT_PDF_MAP[ticker]
      st.success(f"Official Fact Sheet Resource for {ticker}:")
      st.markdown(f"### 📄 **[Open Official Fact Sheet / PDF Page]({link})**")
    else:
      # Fallback for any other ticker: Direct pre-filtered Google search link for PDFs
      pdf_search_url = (
          f"https://www.google.com/search?q={ticker}+ETF+fact+sheet+filetype:pdf"
      )
      yahoo_url = f"https://finance.yahoo.com/quote/{ticker}"

      st.info(
          f"Generated direct search shortcuts for **{ticker}**:"
      )
      st.markdown(
          f"### 📄 **[Click here to search Google for {ticker} PDF Fact"
          f" Sheet]({pdf_search_url})**"
      )
      st.markdown(f"📈 **[View {ticker} on Yahoo Finance]({yahoo_url})**")
