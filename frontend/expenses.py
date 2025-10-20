
import streamlit as st
import pandas as pd
from datetime import datetime
import requests 


def maintain_expenses(api_url):
    categories = ['Rent', 'Food', 'Shopping', 'Entertainment', 'Other']

    # Select a date
    selected_date = st.date_input('Select a date', datetime(2024, 8, 1), label_visibility="collapsed")

    # Convert the selected date to a string in the format 'YYYY-MM-DD'
    formatted_date = selected_date.strftime('%Y-%m-%d')

    # Fetch expenses dynamically when the date changes
    if "existing_expenses" not in st.session_state or st.session_state.get("last_selected_date") != selected_date:
        response = requests.get(f"{api_url}/expenses/{formatted_date}")
        if response.status_code == 200:
            st.session_state.existing_expenses = response.json()
        else:
            st.error("Failed to fetch expenses")
            st.session_state.existing_expenses = []
        st.session_state.last_selected_date = selected_date

    # Ensure the grid reflects the updated data
    existing_expenses = st.session_state.existing_expenses

    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<p style='color: white; font-weight: heading;'>Amount</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<p style='color: white; font-weight: heading;'>Category</p>", unsafe_allow_html=True)
        with col3:
             st.markdown("<p style='color: white; font-weight: heading;'>Notes</p>", unsafe_allow_html=True)

        # Create a new list to hold updated expenses
        updated_expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = 'Rent'
                notes = ''

            # Dynamically update the grid with the fetched data
            with col1:
                amount_input = st.number_input(label='Amount', min_value=0.0, value=amount, step=1.0, key=f'amount_{i}_{selected_date}', label_visibility='collapsed')
            with col2:
                category_input = st.selectbox(label='Category', options=categories, index=categories.index(category), key=f'category_{i}_{selected_date}', label_visibility='collapsed')
            with col3:
                notes_input = st.text_input(label='Notes', value=notes, key=f'notes_{i}_{selected_date}', label_visibility='collapsed')

            # Add the updated expense to the new list
            updated_expenses.append(
                {'amount': amount_input,
                'category': category_input,
                'notes': notes_input}
            )

        submit_button = st.form_submit_button(label='Submit Expenses')
        if submit_button:
            # Filter out expenses with zero amounts
            filtered_expenses = [exp for exp in updated_expenses if exp['amount'] > 0]
            response = requests.post(
                f"{api_url}/expenses/{formatted_date}",
                json=filtered_expenses
            )
            if response.status_code == 200:
                st.success("Expenses submitted successfully!")
            else:
                st.error("Failed to submit expenses")