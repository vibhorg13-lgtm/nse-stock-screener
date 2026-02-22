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
    --red:     #c0392
