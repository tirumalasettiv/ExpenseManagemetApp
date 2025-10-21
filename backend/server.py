from fastapi import FastAPI
import pandas as pd
import db_connect
from datetime import date
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    #expense_date : date
    amount : float
    category : str
    notes : str

app = FastAPI()

@app.get("/expenses/{expoense_date}",response_model = List[Expense])
def get_expenses(expoense_date: date):
    expenses = db_connect.fetch_expenses_for_date(expoense_date)
    return expenses




@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date, expenses:List[Expense]):
    db_connect.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_connect.insert_expense(
            expense_date= expense_date,
            amount= expense.amount,
            category= expense.category,
            notes= expense.notes            
        )
    
    return {"message":"Expenses added/updated successfully"}

@app.get("/expense_category/{start_date},{end_date}")
def get_expense_category(start_date:date, end_date:date):
    result = db_connect.get_spend_by_category(start_date, end_date)
    df = pd.DataFrame(result)
    total = df['total_amount'].sum()
    df['expense %'] = round((df['total_amount'] / total) * 100,2)
    df.sort_values(by='total_amount', ascending=False, inplace=True)
    return df.to_dict('records')


@app.get("/expense_month/{start_date},{end_date}")
def get_expense_month(start_date:date, end_date:date):
    result = db_connect.get_spend_by_month(start_date, end_date)
    df = pd.DataFrame(result)
    df.sort_values(by='expense', ascending=False, inplace=True)
    return df.to_dict('records')

