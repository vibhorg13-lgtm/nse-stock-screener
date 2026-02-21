import streamlit as st
import yfinance as yf
import pandas as pd
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NSE Stock Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --accent: #00e5a0;
    --accent2: #0066ff;
    --warn: #ff6b35;
    --text: #e8edf5;
    --muted: #5a6a80;
    --border: #1e2d42;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.screener-header {
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.screener-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.screener-subtitle {
    color: var(--muted);
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    margin-top: 0.3rem;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #00b37a 100%) !important;
    color: #0a0e1a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.info-box {
    background: rgba(0,102,255,0.1);
    border: 1px solid rgba(0,102,255,0.3);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #7ab3ff;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── NSE Stock Universe ────────────────────────────────────────────────────────
NSE_STOCKS = {
    "RELIANCE": "Reliance Industries", "TCS": "Tata Consultancy Services",
    "HDFCBANK": "HDFC Bank", "INFY": "Infosys", "ICICIBANK": "ICICI Bank",
    "HINDUNILVR": "Hindustan Unilever", "ITC": "ITC Limited", "SBIN": "State Bank of India",
    "BHARTIARTL": "Bharti Airtel", "KOTAKBANK": "Kotak Mahindra Bank",
    "WIPRO": "Wipro", "AXISBANK": "Axis Bank", "LT": "Larsen & Toubro",
    "ASIANPAINT": "Asian Paints", "MARUTI": "Maruti Suzuki",
    "SUNPHARMA": "Sun Pharmaceutical", "TITAN": "Titan Company",
    "ULTRACEMCO": "UltraTech Cement", "BAJFINANCE": "Bajaj Finance",
    "NESTLEIND": "Nestle India", "TECHM": "Tech Mahindra",
    "POWERGRID": "Power Grid Corp", "NTPC": "NTPC Limited",
    "ONGC": "ONGC", "JSWSTEEL": "JSW Steel",
    "TATAMOTORS": "Tata Motors", "HCLTECH": "HCL Technologies",
    "ADANIENT": "Adani Enterprises", "BAJAJFINSV": "Bajaj Finserv",
    "DRREDDY": "Dr. Reddy's Laboratories",
}

SECTORS = {
    "RELIANCE": "Energy", "TCS": "IT", "HDFCBANK": "Banking", "INFY": "IT",
    "ICICIBANK": "Banking", "HINDUNILVR": "FMCG", "ITC": "FMCG", "SBIN": "Banking",
    "BHARTIARTL": "Telecom", "KOTAKBANK": "Banking", "WIPRO": "IT", "AXISBANK": "Banking",
    "LT": "Infrastructure", "ASIANPAINT": "Paints", "MARUTI": "Auto",
    "SUNPHARMA": "Pharma", "TITAN": "Consumer", "ULTRACEMCO": "Cement",
    "BAJFINANCE": "NBFC", "NESTLEIND": "FMCG", "TECHM": "IT",
    "POWERGRID": "Utilities", "NTPC": "Utilities", "ONGC": "Energy",
    "JSWSTEEL": "Steel", "TATAMOTORS": "Auto", "HCLTECH": "IT",
    "ADANIENT": "Conglomerate", "BAJAJFINSV": "NBFC", "DRREDDY": "Pharma",
}

# ── Data Fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_data(ticker_symbol):
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.NS")
        info = ticker.info
        financials = ticker.financials
        revenue_growth = None
        profit_growth = None

        if financials is not None and not financials.empty and financials.shape[1] >= 2:
            for key in ["Total Revenue", "Revenue"]:
                if key in financials.index:
                    rev_row = financials.loc[key]
                    r_new, r_old = rev_row.iloc[0], rev_row.iloc[1]
                    if r_old and r_old != 0:
                        revenue_growth = round(((r_new - r_old) / abs(r_old)) * 100, 1)
                    break

            for key in ["Net Income", "Net Income Common Stockholders"]:
                if key in financials.index:
                    pi_row = financials.loc[key]
                    p_new, p_old = pi_row.iloc[0], pi_row.iloc[1]
                    if p_old and p_old != 0:
                        profit_growth = round(((p_new - p_old) / abs(p_old)) * 100, 1)
                    break

        return {
            "Symbol": ticker_symbol,
            "Company": NSE_STOCKS.get(ticker_symbol, ticker_symbol),
            "Sector": SECTORS.get(ticker_symbol, "Other"),
            "Market Cap (Cr)": round(info.get("marketCap", 0) / 1e7, 0) if info.get("marketCap") else None,
            "P/E Ratio": round(info.get("trailingPE", None), 2) if info.get("trailingPE") else None,
            "ROE (%)": round(info.get("returnOnEquity", 0) * 100, 1) if info.get("returnOnEquity") else None,
            "Revenue Growth (%)": revenue_growth,
            "Profit Growth (%)": profit_growth,
            "52W High": info.get("fiftyTwoWeekHigh"),
            "52W Low": info.get("fiftyTwoWeekLow"),
            "Current Price": info.get("currentPrice") or info.get("regularMarketPrice"),
        }
    except Exception:
        return None


def load_all_stocks(selected_symbols):
    results = []
    progress = st.progress(0, text="Fetching stock data from NSE...")
    total = len(selected_symbols)
    for i, sym in enumerate(selected_symbols):
        data = fetch_stock_data(sym)
        if data:
            results.append(data)
        progress.progress((i + 1) / total, text=f"Fetching {sym}... ({i+1}/{total})")
        time.sleep(0.1)
    progress.empty()
    return pd.DataFrame(results)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="screener-header">
    <p class="screener-title">NSE Stock Screener</p>
    <p class="screener-subtitle">// Filter. Discover. Invest smarter.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-label">Stock Universe</p>', unsafe_allow_html=True)
    selected_stocks = st.multiselect(
        "Select stocks to screen",
        options=list(NSE_STOCKS.keys()),
        default=list(NSE_STOCKS.keys()),
        format_func=lambda x: f"{x} — {NSE_STOCKS[x]}"
    )

    st.markdown('<p class="section-label" style="margin-top:1.5rem">Filters</p>', unsafe_allow_html=True)

    pe_enabled = st.checkbox("P/E Ratio", value=True)
    pe_min, pe_max = st.slider("P/E Range", 0, 150, (0, 40), disabled=not pe_enabled)

    mcap_enabled = st.checkbox("Market Cap (₹ Cr)", value=False)
    mcap_min = st.number_input("Min Market Cap (₹ Cr)", value=10000, step=5000, disabled=not mcap_enabled)

    roe_enabled = st.checkbox("Return on Equity (ROE %)", value=True)
    roe_min = st.slider("Min ROE (%)", 0, 50, 15, disabled=not roe_enabled)

    rev_enabled = st.checkbox("Sales Growth YoY (%)", value=True)
    rev_min = st.slider("Min Sales Growth (%)", -20, 100, 10, disabled=not rev_enabled)

    profit_enabled = st.checkbox("Profit Growth YoY (%)", value=True)
    profit_min = st.slider("Min Profit Growth (%)", -20, 100, 10, disabled=not profit_enabled)

    st.markdown('<p class="section-label" style="margin-top:1.5rem">Sector</p>', unsafe_allow_html=True)
    all_sectors = sorted(set(SECTORS.values()))
    selected_sectors = st.multiselect("Filter by Sector", options=all_sectors, default=all_sectors)

    st.markdown("---")
    run_screen = st.button("🔍 Run Screener", use_container_width=True)

# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="info-box">ℹ️ Data sourced from Yahoo Finance (yfinance). Growth figures are YoY based on latest annual financials.</div>', unsafe_allow_html=True)

if run_screen:
    if not selected_stocks:
        st.warning("Please select at least one stock.")
    else:
        with st.spinner(""):
            df = load_all_stocks(selected_stocks)

        if df.empty:
            st.error("Could not fetch data. Check your internet connection.")
        else:
            mask = pd.Series([True] * len(df))

            if pe_enabled:
                mask &= df["P/E Ratio"].notna() & df["P/E Ratio"].between(pe_min, pe_max)
            if mcap_enabled:
                mask &= df["Market Cap (Cr)"].notna() & (df["Market Cap (Cr)"] >= mcap_min)
            if roe_enabled:
                mask &= df["ROE (%)"].notna() & (df["ROE (%)"] >= roe_min)
            if rev_enabled:
                mask &= df["Revenue Growth (%)"].notna() & (df["Revenue Growth (%)"] >= rev_min)
            if profit_enabled:
                mask &= df["Profit Growth (%)"].notna() & (df["Profit Growth (%)"] >= profit_min)
            if selected_sectors:
                mask &= df["Sector"].isin(selected_sectors)

            filtered_df = df[mask].reset_index(drop=True)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Stocks Screened", len(df))
            col2.metric("Passed Filters", len(filtered_df))
            col3.metric("Pass Rate", f"{round(len(filtered_df)/len(df)*100)}%" if len(df) > 0 else "—")
            avg_pe = filtered_df["P/E Ratio"].mean()
            col4.metric("Avg P/E (results)", f"{avg_pe:.1f}" if not pd.isna(avg_pe) else "—")

            st.markdown("---")

            if filtered_df.empty:
                st.warning("No stocks matched your filters. Try relaxing the criteria.")
            else:
                st.markdown(f"### {len(filtered_df)} Stocks Passed")

                display_cols = ["Symbol", "Company", "Sector", "Current Price",
                                "P/E Ratio", "Market Cap (Cr)", "ROE (%)",
                                "Revenue Growth (%)", "Profit Growth (%)"]
                display_df = filtered_df[display_cols].copy()

                def color_growth(val):
                    if pd.isna(val): return "color: #5a6a80"
                    return "color: #00e5a0" if val > 0 else "color: #ff6b35"

                styled = display_df.style\
                    .applymap(color_growth, subset=["Revenue Growth (%)", "Profit Growth (%)"])\
                    .format({
                        "Current Price": "₹{:.1f}",
                        "P/E Ratio": "{:.1f}",
                        "Market Cap (Cr)": "₹{:,.0f}",
                        "ROE (%)": "{:.1f}%",
                        "Revenue Growth (%)": "{:.1f}%",
                        "Profit Growth (%)": "{:.1f}%",
                    }, na_rep="N/A")

                st.dataframe(styled, use_container_width=True, height=400)

                st.markdown("---")
                st.markdown("### Growth vs Industry Average")

                sector_avg = df.groupby("Sector")[["Revenue Growth (%)", "Profit Growth (%)"]].mean().round(1)
                filtered_with_sector = filtered_df.copy()
                filtered_with_sector["Industry Avg Rev Growth (%)"] = filtered_with_sector["Sector"].map(sector_avg["Revenue Growth (%)"])
                filtered_with_sector["Industry Avg Profit Growth (%)"] = filtered_with_sector["Sector"].map(sector_avg["Profit Growth (%)"])
                filtered_with_sector["Beats Industry Rev?"] = filtered_with_sector["Revenue Growth (%)"] > filtered_with_sector["Industry Avg Rev Growth (%)"]
                filtered_with_sector["Beats Industry Profit?"] = filtered_with_sector["Profit Growth (%)"] > filtered_with_sector["Industry Avg Profit Growth (%)"]

                industry_cols = ["Symbol", "Sector",
                                 "Revenue Growth (%)", "Industry Avg Rev Growth (%)", "Beats Industry Rev?",
                                 "Profit Growth (%)", "Industry Avg Profit Growth (%)", "Beats Industry Profit?"]
                st.dataframe(filtered_with_sector[industry_cols], use_container_width=True)

                csv = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download Results as CSV", csv, "screened_stocks.csv", "text/csv")

else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #5a6a80;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <div style="font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 600; color: #e8edf5; margin-bottom: 0.5rem;">
            Set your filters and run the screener
        </div>
        <div style="font-family: 'Space Mono', monospace; font-size: 0.8rem;">
            Configure filters in the sidebar → Hit "Run Screener"
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 How to use this screener"):
        st.markdown("""
        1. **Select stocks** from the universe in the sidebar (default = all 30 Nifty stocks)
        2. **Enable filters** using checkboxes and set your thresholds
        3. **Hit 'Run Screener'** — fetches live data from Yahoo Finance
        4. Review results including **Industry Comparison** table
        5. **Download** results as CSV for further analysis

        **Tip:** Start with relaxed filters to see how many stocks have data, then tighten gradually.
        """)

