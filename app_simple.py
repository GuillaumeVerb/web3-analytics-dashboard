"""
Ultra-simplified version for Streamlit Cloud testing
"""
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="WDI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 WDI – Web3 Analytics Dashboard")
st.write("Simplified version for testing")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} rows")
    st.dataframe(df.head(10))

