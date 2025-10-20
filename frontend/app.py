import os
import streamlit as st
import pandas as pd
from datetime import datetime
import requests 
from expenses import maintain_expenses
from analytics import view_analytics

# Load and apply CSS styles
'''st.write(os.getcwd())
css_file_path = os.path.join(os.getcwd(), "style.css")
if os.path.exists(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("CSS file not found. Please ensure 'style.css' exists in the current directory.")
'''
api_url = "http://127.0.0.1:8000"

st.title("Expense Management App")

tab1, tab2 = st.tabs(["Add/Update Expenses", "View Analytics"])

with tab1:
    maintain_expenses(api_url)
with tab2:
    view_analytics(api_url)