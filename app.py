import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="Equita — Stock Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    --gold:    #b8935a;
    --green:   #2d6a4f;
    --red:     #c0392b;
    --radius:  14px;
    --shadow:  0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
}

html, body, [class*="css"], .main, .stApp,
[data-testid="stAppViewContainer"], [data-testid="block-container"] {
    background-color: #f7f6f3 !important;
    color: #1a1917 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp, [data-testid="stAppViewContainer"] { background-color: #f7f6f3 !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }

.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1300px !important;
}

.page-header {
    display: flex; align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid #e8e6df;
}
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem; line-height: 1.1; letter-spacing: -0.5px;
}

.filter-panel {
    background: #ffffff;
    border: 1px solid #e8e6df;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.filter-panel-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; color: #1a1917;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #e8e6df;
}
.filter-group-label {
    font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase;
    color: #9e9b93; font-weight: 600; margin-bottom: 0.6rem; margin-top: 0.2rem;
}

div[data-baseweb="checkbox"] svg { fill: #1a1917 !important; }
.stMultiSelect [data-baseweb="tag"] {
    background: #1a1917 !important; border-radius: 4px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: white !important; }
.stSlider > div > div > div > div { background: #1a1917 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #1a1917 !important; border-color: #1a1917 !important;
}
.stNumberInput input {
    background: #ffffff !important; border-color: #e8e6df !important;
    border-radius: 8px !important; color: #1a1917 !important;
}
.stNumberInput button {
    background: #f0efe9 !important; border-color: #e8e6df !important;
    color: #1a1917 !important;
}

.stButton > button {
    background: #1a1917 !important; color: white !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 1rem !important; border: none !important;
    border-radius: 10px !important; padding: 0.7rem 2.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #b8935a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
}

.metrics-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin-bottom: 2rem;
}
.metric-card {
    background: #ffffff; border: 1px solid #e8e6df;
    border-radius: 14px; padding: 1.3rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.metric-card-label {
    font-size: 0.65rem; letter-spacing: 1.5px; text-transform: uppercase;
    color: #9e9b93; font-weight: 500; margin-bottom: 0.4rem;
}
.metric-card-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem; color: #1a1917; line-height: 1;
}
.metric-card-sub { font-size: 0.72rem; color: #9e9b93; margin-top: 0.3rem; }

.results-header {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 1rem;
}
.results-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem; color: #1a1917;
}
.results-count {
    background: #1a1917; color: white !important;
    font-size: 0.75rem; font-weight: 600;
    padding: 3px 12px; border-radius: 20px;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; color: #1a1917; margin-bottom: 0.8rem;
}

[data-testid="stDataFrame"] {
    border-radius: 12px !important; border: 1px solid #e8e6df !important;
    overflow: hidden !important;
}

.empty-state {
    text-align: center; padding: 4rem 2rem;
    background: #ffffff; border: 1px solid #e8e6df; border-radius: 14px;
}
.empty-state-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem; color: #1a1917; margin-bottom: 0.5rem;
}
.empty-state-sub {
    font-size: 0.85rem; color: #9e9b93;
    max-width: 360px; margin: 0 auto; line-height: 1.6;
}

.stDownloadButton > button {
    background: transparent !important; color: #1a1917 !important;
    border: 1px solid #e8e6df !important; border-radius: 8px !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
}
.stDownloadButton > button:hover {
    background: #1a1917 !important; color: white !important;
}

.notice {
    background: white; border: 1px solid #e8e6df;
    border-left: 3px solid #b8935a; border-radius: 8px;
    padding: 0.7rem 1rem; font-size: 0.78rem;
    color: #3d3b36; margin-bottom: 1.5rem;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f7f6f3; }
::-webkit-scrollbar-thumb { background: #e8e6df; border-radius: 3px; }
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
        growth_period = None

        if financials is not None and not financials.empty and financials.shape[1] >= 2:
            cols = financials.columns.tolist()
            try:
                yr_new = pd.to_datetime(cols[0]).year
                yr_old = pd.to_datetime(cols[1]).year
                growth_period = f"FY{yr_old}-FY{yr_new}"
            except Exception:
                growth_period = "YoY"

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
            "Price (Rs)":         info.get("currentPrice") or info.get("regularMarketPrice"),
            "Market Cap (Cr)":    round(info.get("marketCap", 0) / 1e7, 0) if info.get("marketCap") else None,
            "P/E Ratio":          round(info.get("trailingPE"), 1) if info.get("trailingPE") else None,
            "ROE (%)":            round(info.get("returnOnEquity", 0) * 100, 1) if info.get("returnOnEquity") else None,
            "Sales Growth (%)":   revenue_growth,
            "Profit Growth (%)":  profit_growth,
            "_growth_period":     growth_period,
        }
    except Exception:
        return None


def load_all_stocks(symbols):
    results = []
    bar = st.progress(0, text="Retrieving market data...")
    for i, sym in enumerate(symbols):
        data = fetch_stock_data(sym)
        if data:
            results.append(data)
        bar.progress((i + 1) / len(symbols), text=f"Fetching {sym}  -  {i+1} of {len(symbols)}")
        time.sleep(0.08)
    bar.empty()
    return pd.DataFrame(results)


today = datetime.now().strftime("%A, %d %B %Y")

st.markdown(f"""
<div class="page-header">
    <div class="page-title">
        <span style="color:#1a1917; -webkit-text-fill-color:#1a1917;">NSE </span>
        <em style="color:#b8935a; -webkit-text-fill-color:#b8935a; font-style:italic;">Stock </em>
        <span style="color:#1a1917; -webkit-text-fill-color:#1a1917;">Screener</span>
    </div>
    <div style="font-size:0.78rem; color:#9e9b93; text-align:right; line-height:1.8;">
        <div style="color:#1a1917; font-weight:500;">NSE / BSE</div>
        <div>{today}</div>
        <div>Powered by Yahoo Finance</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="filter-panel"><div class="filter-panel-title">Filters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="filter-group-label">Stock Universe</p>', unsafe_allow_html=True)
    selected_stocks = st.multiselect(
        "Stocks", options=list(NSE_STOCKS.keys()), default=list(NSE_STOCKS.keys()),
        format_func=lambda x: f"{x}  -  {NSE_STOCKS[x]}", label_visibility="collapsed"
    )
with col2:
    st.markdown('<p class="filter-group-label">Sector</p>', unsafe_allow_html=True)
    all_sectors = sorted(set(SECTORS.values()))
    selected_sectors = st.multiselect(
        "Sectors", options=all_sectors, default=all_sectors,
        label_visibility="collapsed", placeholder="All sectors"
    )

st.markdown("<br>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    st.markdown('<p class="filter-group-label">P/E Ratio</p>', unsafe_allow_html=True)
    pe_enabled = st.checkbox("Enable P/E filter", value=True, key="pe_chk")
    pe_min, pe_max = st.slider("P/E Range", 0, 150, (0, 40),
                                disabled=not pe_enabled, label_visibility="collapsed")
    if pe_enabled:
        st.caption(f"Between {pe_min} and {pe_max}")

with col4:
    st.markdown('<p class="filter-group-label">Return on Equity (ROE)</p>', unsafe_allow_html=True)
    roe_enabled = st.checkbox("Enable ROE filter", value=True, key="roe_chk")
    roe_min = st.slider("Min ROE %", 0, 50, 15,
                         disabled=not roe_enabled, label_visibility="collapsed")
    if roe_enabled:
        st.caption(f"ROE >= {roe_min}%")

with col5:
    st.markdown('<p class="filter-group-label">Market Cap (Rs Cr)</p>', unsafe_allow_html=True)
    mcap_enabled = st.checkbox("Enable Market Cap filter", value=False, key="mcap_chk")
    if mcap_enabled:
        mcap_min = st.number_input("Min Market Cap", value=10000, step=5000,
                                    min_value=0, label_visibility="collapsed")
        st.caption(f"Min Rs {mcap_min:,} Cr  (steps of Rs 5,000 Cr)")
    else:
        mcap_min = 0
        st.caption("Not applied")

st.markdown("<br>", unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    st.markdown('<p class="filter-group-label">Min Sales Growth % (Year-on-Year)</p>', unsafe_allow_html=True)
    rev_enabled = st.checkbox("Enable Sales Growth filter", value=True, key="rev_chk")
    rev_min = st.slider("Min Sales Growth", -20, 100, 10,
                         disabled=not rev_enabled, label_visibility="collapsed")
    if rev_enabled:
        st.caption(f"Sales Growth >= {rev_min}% YoY")

with col7:
    st.markdown('<p class="filter-group-label">Min Profit Growth % (Year-on-Year)</p>', unsafe_allow_html=True)
    profit_enabled = st.checkbox("Enable Profit Growth filter", value=True, key="profit_chk")
    profit_min = st.slider("Min Profit Growth", -20, 100, 10,
                            disabled=not profit_enabled, label_visibility="collapsed")
    if profit_enabled:
        st.caption(f"Profit Growth >= {profit_min}% YoY")

st.markdown("</div>", unsafe_allow_html=True)

run_screen = st.button("Run Screener")

st.markdown('<div class="notice">Data sourced from Yahoo Finance &nbsp;&middot;&nbsp; Financials reflect latest annual report &nbsp;&middot;&nbsp; Growth figures are year-on-year</div>', unsafe_allow_html=True)

if run_screen:
    if not selected_stocks:
        st.warning("Please select at least one stock.")
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
                mask &= df["Market Cap (Cr)"].notna() & (df["Market Cap (Cr)"] >= mcap_min)
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

            growth_period = "YoY"
            if "_growth_period" in df.columns:
                periods = df["_growth_period"].dropna().unique()
                if len(periods) > 0:
                    growth_period = periods[0]

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
                    <div class="metric-card-value">{"&mdash;" if pd.isna(avg_pe) else f"{avg_pe:.1f}x"}</div>
                    <div class="metric-card-sub">Qualified stocks</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if filtered.empty:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-title">No stocks matched</div>
                    <div class="empty-state-sub">Try relaxing your filter thresholds above.</div>
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
                    return "color: #2d6a4f; font-weight:500" if val >= 0 else "color: #c0392b; font-weight:500"

                display_cols = ["Symbol", "Company", "Sector", "Price (Rs)",
                                "P/E Ratio", "Market Cap (Cr)", "ROE (%)",
                                "Sales Growth (%)", "Profit Growth (%)"]
                display_df = filtered[display_cols].copy()
                display_df = display_df.rename(columns={
                    "Sales Growth (%)":  f"Sales Growth ({growth_period})",
                    "Profit Growth (%)": f"Profit Growth ({growth_period})",
                })
                sales_col  = f"Sales Growth ({growth_period})"
                profit_col = f"Profit Growth ({growth_period})"

                styled = display_df.style \
                    .applymap(style_growth, subset=[sales_col, profit_col]) \
                    .format({
                        "Price (Rs)":      "Rs {:.1f}",
                        "P/E Ratio":       "{:.1f}x",
                        "Market Cap (Cr)": "Rs {:,.0f}",
                        "ROE (%)":         "{:.1f}%",
                        sales_col:         "{:+.1f}%",
                        profit_col:        "{:+.1f}%",
                    }, na_rep="—") \
                    .set_properties(**{
                        "background-color": "#ffffff",
                        "color": "#1a1917",
                        "font-family": "DM Sans, sans-serif",
                        "font-size": "0.85rem",
                    })

                st.dataframe(
                    styled, use_container_width=True,
                    height=min(420, 60 + len(filtered) * 38),
                    hide_index=True,
                    column_config={
                        "Company":         st.column_config.TextColumn(width="large"),
                        "Sector":          st.column_config.TextColumn(width="medium"),
                        "Symbol":          st.column_config.TextColumn(width="small"),
                        "Price (Rs)":      st.column_config.NumberColumn(width="small"),
                        "P/E Ratio":       st.column_config.NumberColumn(width="small"),
                        "Market Cap (Cr)": st.column_config.NumberColumn(width="medium"),
                        "ROE (%)":         st.column_config.NumberColumn(width="small"),
                    }
                )

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">Growth vs Industry Average</div>', unsafe_allow_html=True)

                sector_avg = df.groupby("Sector")[["Sales Growth (%)", "Profit Growth (%)"]].mean().round(1)
                cmp = filtered.copy()
                cmp["Industry Sales Avg (%)"]  = cmp["Sector"].map(sector_avg["Sales Growth (%)"])
                cmp["Industry Profit Avg (%)"] = cmp["Sector"].map(sector_avg["Profit Growth (%)"])
                cmp["Beats Sales Avg"]         = cmp["Sales Growth (%)"] > cmp["Industry Sales Avg (%)"]
                cmp["Beats Profit Avg"]        = cmp["Profit Growth (%)"] > cmp["Industry Profit Avg (%)"]

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

                st.dataframe(ind_styled, use_container_width=True, hide_index=True)

                st.markdown("<br>", unsafe_allow_html=True)
                export_df = filtered[[c for c in filtered.columns if not c.startswith("_")]].copy()
                csv = export_df.to_csv(index=False).encode("utf-8")
                st.download_button("Export Results as CSV", csv, "equita_screener_results.csv", "text/csv")

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-title">Ready to screen</div>
        <div class="empty-state-sub">
            Set your filters above and press <strong>Run Screener</strong>
            to discover qualifying companies.
        </div>
    </div>
    """, unsafe_allow_html=True)

                    
