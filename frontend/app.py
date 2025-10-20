import os
import streamlit as st
import pandas as pd
from datetime import datetime
import requests 
from expenses import maintain_expenses
from analytics import view_analytics

# Load and apply CSS styles

api_url = "https://expensetracking.streamlit.app"

st.title("Expense Management App")

tab1, tab2 = st.tabs(["Add/Update Expenses", "View Analytics"])

with tab1:
    maintain_expenses(api_url)
with tab2:
    view_analytics(api_url)