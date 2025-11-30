"""
Minimal test app for Streamlit Cloud deployment
"""
import streamlit as st

st.set_page_config(page_title="WDI Test", page_icon="📊", layout="wide")

st.title("🎉 WDI Dashboard - Test")
st.write("If you see this, the app is working!")

st.success("✅ Streamlit is running correctly!")
st.info("This is a minimal test version to verify deployment works.")

