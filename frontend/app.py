import os
import streamlit as st
from expenses import maintain_expenses
from analytics import view_analytics

# api_url = "https://expensetracking.streamlit.app"

api_url = 'http://127.0.0.1:8000' 

st.title("Expense Management App")

tab1, tab2 = st.tabs(["Add/Update Expenses", "View Analytics"])

with tab1:
    maintain_expenses(api_url)
with tab2:
    view_analytics(api_url)