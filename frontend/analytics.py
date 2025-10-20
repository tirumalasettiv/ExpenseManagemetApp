import streamlit as st
import pandas as pd
from datetime import datetime
import requests 

def view_analytics(api_url):

    # Select a date range
    col1, col2 = st.columns(2)
    
    # display date inputs side by side    
    with col1:
        start_date = st.date_input('Start Date', datetime(2024, 8, 1), key='start_date')
    with col2:
        end_date = st.date_input('End Date', datetime(2024, 8, 31), key='end_date')

    if start_date > end_date:
        st.error("Start date must be before end date")
        return
    
    # Button to fetch analytics data
    if st.button('Get Analytics'):
        
        # Convert dates to string format 'YYYY-MM-DD'        
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
        # Fetch analytics data from the backend
   
        response = requests.get(f"{api_url}/expense_sumamry/{start_date},{end_date}")
        if response.status_code == 200:
            analytics_data = response.json()
        else:
            st.error("Failed to fetch analytics data")
            return

        # Display analytics data
        if analytics_data:
            df = pd.DataFrame(analytics_data)
       
            
            st.markdown("**Expense by Category**")
            st.bar_chart(data=df, 
                         x='category',
                         y='total_amount',
                         sort='total_amount'                                              
                         )
            
            st.markdown("**Expense Summary**")
            st.dataframe(df)
            
            
            
        else:
            st.info("No analytics data available for the selected date range")

        