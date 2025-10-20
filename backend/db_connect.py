
import mysql.connector
from contextlib import contextmanager
import pandas as pd


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host = '34.162.64.142',
        port = '3306',
        database = 'expense_manager',
        user = 'atirumv',
        password = 'Jhansi007$'  
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        return expenses


def fetch_expenses_for_date(expense_date):
    with get_db_cursor() as cursor:
        query = 'SELECT * FROM expenses WHERE expense_date = %s'
        value = (expense_date,)
        cursor.execute(query, value)
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        query = 'INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)'
        value = (expense_date, amount, category, notes)
        cursor.execute(query, value)
      

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        query = 'DELETE FROM expenses WHERE expense_date = %s'
        value = (expense_date,)
        cursor.execute(query, value)
        
        
def get_analytics(from_date, to_date):
    with get_db_cursor() as cursor:
        query = ''' 
        SELECT 
            category, SUM(amount) AS total_amount 
        FROM expenses
        WHERE expense_date BETWEEN %s AND %s
        GROUP BY category;          
        '''
        filter = (from_date, to_date)
        cursor.execute(query, filter)      
        analytics = cursor.fetchall() 
        return analytics

if __name__ == "__main__":
    
    data = get_analytics("2024-08-01", "2024-08-20")
    #insert_expense("2024-08-20", 300, "Food", "Panipuri")
    #delete_expenses_for_date("2024-08-20")
    #fetch_expenses_for_date("2024-08-20")
    #data = fetch_all_records()
    data = pd.DataFrame(data)
    print(data)