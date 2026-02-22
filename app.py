import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(
    page_title="Equita — Stock Screener",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --white:   #ffffff;
    --off:     #f7f6f3;
    --snow:    #f0efe9;
    --border:  #e8e6df;
    --muted:   #9e9b93;
    --ink:     #1a1917;
    --ink2:    #3d3b36;
    --gold:    #b8935a;
    --gold2:   #d4a96a;
    --green:   #2d6a4f;
    --red:     #c0392b;
    --radius:  14px;
    --shadow:  0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    --shadow2: 0 2px 8px rgba(0,0,0,0.08), 0 12px 40px rgba(0,0,0,0.06);
}

html, body, [class*="css"], .main {
    background-color: var(--off) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 3rem 3rem !important;
    max-width: 1400px !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 2.5rem 1.8rem !important;
}
[data-testid="stSidebar"] * {
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-logo {
    width: 32px;
    height: 32px;
    background: var(--ink);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--gold) !important;
    font-size: 1rem;
    font-family: 'DM Serif Display', serif !important;
    flex-shrink: 0;
}
.sidebar-name {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.15rem;
    color: var(--ink) !important;
    letter-spacing: 0.3px;
}
.sidebar-tagline {
    font-size: 0.7rem;
    color: var(--muted) !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 1px;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted) !important;
    font-weight: 600;
    margin: 1.8rem 0 0.8rem 0;
}

.stSlider > div > div > div > div {
    background: var(--ink) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--ink) !important;
    border-color: var(--ink) !important;
}
div[data-baseweb="checkbox"] svg { fill: var(--ink) !important; }
div[data-baseweb="checkbox"] { gap: 8px; }

.stMultiSelect [data-baseweb="tag"] {
    background: var(--ink) !important;
    border-radius: 4px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: white !important; }

.stNumberInput input, div[data-baseweb="input"] input {
    background: var(--off) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    background: var(--ink) !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--ink2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
}

.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: var(--ink);
    line-height: 1.1;
    letter-spacing: -0.5px;
}
.page-title em {
    font-style: italic;
    color: var(--gold);
}
.page-date {
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.5px;
    text-align: right;
}

.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow);
}
.metric-card-label {
    font-size: 0.7rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.metric-card-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: var(--ink);
    line-height: 1;
}
.metric-card-sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

.notice {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 8px;
    padding: 0.75rem 1.1rem;
    font-size: 0.8rem;
    color: var(--ink2);
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.results-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.results-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: var(--ink);
}
.results-count {
    background: var(--ink);
    color: white !important;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}

[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}
.empty-state-symbol {
    font-family: 'DM Serif Display', serif;
    font-size: 3.5rem;
    color: var(--border);
    margin-bottom: 1rem;
}
.empty-state-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--ink);
    margin-bottom: 0.5rem;
}
.empty-state-sub {
    font-size: 0.85rem;
    color: var(--muted);
    max-width: 360px;
    margin: 0 auto;
    line-height: 1.6;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--ink);
    margin-bottom: 1rem;
}

.stDownloadButton > button {
    background: transparent !important;
    color: var(--ink) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: var(--ink) !important;
    color: white !important;
    border-color: var(--ink) !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--off); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""", unsafe_allow_html=True)

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
    "RELIANCE": "Energy", "TCS": "Technology", "HDFCBANK": "Banking", "INFY": "Technology",
    "ICICIBANK": "Banking", "HINDUNILVR": "FMCG", "ITC": "FMCG", "SBIN": "Banking",
    "BHARTIARTL": "Telecom", "KOTAKBANK": "Banking", "WIPRO": "Technology", "AXISBANK": "Banking",
    "LT": "Infrastructure", "ASIANPAINT": "Paints", "MARUTI": "Automobile",
    "SUNPHARMA": "Pharma", "TITAN": "Consumer", "ULTRACEMCO": "Cement",
    "BAJFINANCE": "NBFC", "NESTLEIND": "FMCG", "TECHM": "Technology",
    "POWERGRID": "Utilities", "NTPC": "Utilities", "ONGC": "Energy",
    "JSWSTEEL": "Steel", "TATAMOTORS": "Automobile", "HCLTECH": "Technology",
    "ADANIENT": "Conglomerate", "BAJAJFINSV": "NBFC", "DRREDDY": "Pharma",
}

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
            "Symbol":             ticker_symbol,
            "Company":            NSE_STOCKS.get(ticker_symbol, ticker_symbol),
            "Sector":             SECTORS.get(ticker_symbol, "Other"),
            "Price (₹)":          info.get("currentPrice") or info.get("regularMarketPrice"),
            "Market Cap (₹ Cr)":  round(info.get("marketCap", 0) / 1e7, 0) if info.get("marketCap") else None,
            "P/E Ratio":          round(info.get("trailingPE"), 1) if info.get("trailingPE") else None,
            "ROE (%)":            round(info.get("returnOnEquity", 0) * 100, 1) if info.get("returnOnEquity") else None,
            "Sales Growth (%)":   revenue_growth,
            "Profit Growth (%)":  profit_growth,
        }
    except Exception:
        return None


def load_all_stocks(symbols):
    results = []
    bar = st.progress(0, text="Retrieving market data…")
    for i, sym in enumerate(symbols):
        data = fetch_stock_data(sym)
        if data:
            results.append(data)
        bar.progress((i + 1) / len(symbols), text=f"Fetching {sym}  ·  {i+1} of {len(symbols)}")
        time.sleep(0.08)
    bar.empty()
    return pd.DataFrame(results)


with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">◈</div>
        <div>
            <div class="sidebar-name">Equita</div>
            <div class="sidebar-tagline">NSE Screener</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Universe</p>', unsafe_allow_html=True)
    selected_stocks = st.multiselect(
        "Stocks",
        options=list(NSE_STOCKS.keys()),
        default=list(NSE_STOCKS.keys()),
        format_func=lambda x: f"{x}  —  {NSE_STOCKS[x]}",
        label_visibility="collapsed"
    )

    all_sectors = sorted(set(SECTORS.values()))
    selected_sectors = st.multiselect(
        "Sectors",
        options=all_sectors,
        default=all_sectors,
        label_visibility="collapsed",
        placeholder="Filter by sector…"
    )

    st.markdown('<p class="section-label">Valuation</p>', unsafe_allow_html=True)
    pe_enabled = st.checkbox("P/E Ratio filter", value=True)
    pe_min, pe_max = st.slider("P/E Range", 0, 150, (0, 40),
                                disabled=not pe_enabled, label_visibility="collapsed")
    if pe_enabled:
        st.caption(f"P/E between {pe_min} – {pe_max}")

    mcap_enabled = st.checkbox("Min Market Cap", value=False)
    mcap_min = st.number_input("Min Market Cap (₹ Cr)", value=10000, step=5000,
                                disabled=not mcap_enabled, label_visibility="collapsed")
    if mcap_enabled:
        st.caption(f"Market Cap ≥ ₹{mcap_min:,} Cr")

    st.markdown('<p class="section-label">Quality</p>', unsafe_allow_html=True)
    roe_enabled = st.checkbox("Min ROE (%)", value=True)
    roe_min = st.slider("ROE", 0, 50, 15, disabled=not roe_enabled, label_visibility="collapsed")
    if roe_enabled:
        st.caption(f"ROE ≥ {roe_min}%")

    st.markdown('<p class="section-label">Growth</p>', unsafe_allow_html=True)
    rev_enabled = st.checkbox("Min Sales Growth (%)", value=True)
    rev_min = st.slider("Sales Growth", -20, 100, 10, disabled=not rev_enabled, label_visibility="collapsed")
    if rev_enabled:
        st.caption(f"Sales Growth ≥ {rev_min}%")

    profit_enabled = st.checkbox("Min Profit Growth (%)", value=True)
    profit_min = st.slider("Profit Growth", -20, 100, 10, disabled=not profit_enabled, label_visibility="collapsed")
    if profit_enabled:
        st.caption(f"Profit Growth ≥ {profit_min}%")

    st.markdown("<br>", unsafe_allow_html=True)
    run_screen = st.button("Run Screener →", use_container_width=True)


from datetime import datetime
today = datetime.now().strftime("%A, %d %B %Y")

st.markdown(f"""
<div class="page-header">
    <div class="page-title">NSE <em>Stock</em><br>Screener</div>
    <div class="page-date">
        <div style="color:#1a1917;font-weight:500;">NSE / BSE</div>
        <div>{today}</div>
        <div style="margin-top:4px;">Powered by Yahoo Finance</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
    ◈ &nbsp; Data sourced from Yahoo Finance · Financials reflect latest annual report · Growth figures are year-on-year
</div>
""", unsafe_allow_html=True)

if run_screen:
    if not selected_stocks:
        st.warning("Please select at least one stock from the sidebar.")
    else:
        with st.spinner(""):
            df = load_all_stocks(selected_stocks)

        if df.empty:
            st.error("Unable to retrieve data. Please check your connection.")
        else:
            mask = pd.Series([True] * len(df))
            if pe_enabled:
                mask &= df["P/E Ratio"].notna() & df["P/E Ratio"].between(pe_min, pe_max)
            if mcap_enabled:
                mask &= df["Market Cap (₹ Cr)"].notna() & (df["Market Cap (₹ Cr)"] >= mcap_min)
            if roe_enabled:
                mask &= df["ROE (%)"].notna() & (df["ROE (%)"] >= roe_min)
            if rev_enabled:
                mask &= df["Sales Growth (%)"].notna() & (df["Sales Growth (%)"] >= rev_min)
            if profit_enabled:
                mask &= df["Profit Growth (%)"].notna() & (df["Profit Growth (%)"] >= profit_min)
            if selected_sectors:
                mask &= df["Sector"].isin(selected_sectors)

            filtered = df[mask].reset_index(drop=True)
            pass_rate = round(len(filtered) / len(df) * 100) if len(df) > 0 else 0
            avg_pe = filtered["P/E Ratio"].mean()

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="metric-card-label">Screened</div>
                    <div class="metric-card-value">{len(df)}</div>
                    <div class="metric-card-sub">Total stocks analysed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-card-label">Qualified</div>
                    <div class="metric-card-value">{len(filtered)}</div>
                    <div class="metric-card-sub">Passed all filters</div>
                </div>
                <div class="metric-card">
                    <div class="metric-card-label">Pass Rate</div>
                    <div class="metric-card-value">{pass_rate}%</div>
                    <div class="metric-card-sub">Of screened universe</div>
                </div>
                <div class="metric-card">
                    <div class="metric-card-label">Avg P/E</div>
                    <div class="metric-card-value">{"—" if pd.isna(avg_pe) else f"{avg_pe:.1f}x"}</div>
                    <div class="metric-card-sub">Qualified stocks</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if filtered.empty:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-symbol">◈</div>
                    <div class="empty-state-title">No stocks matched</div>
                    <div class="empty-state-sub">
                        Try relaxing your filter thresholds — lower the minimum
                        growth requirements or widen the P/E range.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="results-header">
                    <div class="results-title">Qualified Companies</div>
                    <span class="results-count">{len(filtered)} results</span>
                </div>
                """, unsafe_allow_html=True)

                def style_growth(val):
                    if pd.isna(val): return "color: #9e9b93"
                    return "color: #2d6a4f; font-weight: 500" if val >= 0 else "color: #c0392b; font-weight: 500"

                display_cols = ["Symbol", "Company", "Sector", "Price (₹)",
                                "P/E Ratio", "Market Cap (₹ Cr)", "ROE (%)",
                                "Sales Growth (%)", "Profit Growth (%)"]

                styled = filtered[display_cols].style \
                    .applymap(style_growth, subset=["Sales Growth (%)", "Profit Growth (%)"]) \
                    .format({
                        "Price (₹)":         "₹{:.1f}",
                        "P/E Ratio":         "{:.1f}x",
                        "Market Cap (₹ Cr)": "₹{:,.0f}",
                        "ROE (%)":           "{:.1f}%",
                        "Sales Growth (%)":  "{:+.1f}%",
                        "Profit Growth (%)": "{:+.1f}%",
                    }, na_rep="—") \
                    .set_properties(**{
                        "background-color": "#ffffff",
                        "color": "#1a1917",
                        "font-family": "DM Sans, sans-serif",
                        "font-size": "0.85rem",
                    })

                st.dataframe(styled, use_container_width=True, height=min(400, 60 + len(filtered) * 38))

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Growth vs Industry Average</div>', unsafe_allow_html=True)

                sector_avg = df.groupby("Sector")[["Sales Growth (%)", "Profit Growth (%)"]].mean().round(1)
                cmp = filtered.copy()
                cmp["Industry Sales Avg (%)"] = cmp["Sector"].map(sector_avg["Sales Growth (%)"])
                cmp["Industry Profit Avg (%)"] = cmp["Sector"].map(sector_avg["Profit Growth (%)"])
                cmp["Beats Sales Avg"] = cmp["Sales Growth (%)"] > cmp["Industry Sales Avg (%)"]
                cmp["Beats Profit Avg"] = cmp["Profit Growth (%)"] > cmp["Industry Profit Avg (%)"]

                ind_cols = ["Symbol", "Sector",
                            "Sales Growth (%)", "Industry Sales Avg (%)", "Beats Sales Avg",
                            "Profit Growth (%)", "Industry Profit Avg (%)", "Beats Profit Avg"]

                ind_styled = cmp[ind_cols].style \
                    .applymap(style_growth, subset=["Sales Growth (%)", "Profit Growth (%)",
                                                     "Industry Sales Avg (%)", "Industry Profit Avg (%)"]) \
                    .format({
                        "Sales Growth (%)":        "{:+.1f}%",
                        "Industry Sales Avg (%)":  "{:+.1f}%",
                        "Profit Growth (%)":        "{:+.1f}%",
                        "Industry Profit Avg (%)": "{:+.1f}%",
                    }, na_rep="—") \
                    .set_properties(**{
                        "background-color": "#ffffff",
                        "color": "#1a1917",
                        "font-family": "DM Sans, sans-serif",
                        "font-size": "0.85rem",
                    })

                st.dataframe(ind_styled, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)
                csv = filtered.to_csv(index=False).encode("utf-8")
                st.download_button("↓  Export Results as CSV", csv, "equita_screener_results.csv", "text/csv")

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-symbol">◈</div>
        <div class="empty-state-title">Ready to screen</div>
        <div class="empty-state-sub">
            Configure your filters in the sidebar — valuation, quality, and growth thresholds —
            then press <strong>Run Screener</strong> to discover qualifying companies.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("How to use Equita"):
        st.markdown("""
        **1. Select your universe** — choose which NSE stocks to include and filter by sector.

        **2. Set valuation filters** — P/E ratio range tells you how expensive a stock is relative to earnings.

        **3. Set quality filters** — ROE (Return on Equity) measures how efficiently a company uses shareholder money.

        **4. Set growth filters** — Sales and Profit Growth show if the business is expanding year-on-year.

        **5. Run & compare** — the Industry Comparison table shows which stocks outperform their sector peers.

        **Tip:** Start with relaxed filters to see what data is available, then tighten gradually.
        """)
