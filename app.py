import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(
    page_title="Equita — Stock Screener",
    page_icon="📈",
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
    --green:   #2d6a4f;
    --red:     #c0392b;
    --radius:  14px;
    --shadow:  0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
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
    font-size: 0.95rem;
    font-weight: 700;
    color: #b8935a !important;
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

.stSlider > div > div > div > div { background: var(--ink) !important; }
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
    background: var(--white) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stNumberInput [data-baseweb="input"] {
    background: var(--white) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
}
.stNumberInput button {
    background: var(--snow) !important;
    border-color: var(--border) !important;
    color: var(--ink) !important;
}

.stButton > button {
    background: #e8e6df !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--ink) !important;
    color: white !important;
    border-color: var(--ink) !important;
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
    color: #1a1917 !important;
    -webkit-text-fill-color: #1a1917 !important;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.page-title em {
    font-style: italic;
    color: #b8935a !important;
    -webkit-text-fill-color: #b8935a !important;
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
    "ICICIBANK": "Banking", "HINDUNILVR":

                    
