from pathlib import Path
import sys

# Add the backend folder to sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

import db_connect

def test_expense_for_date():
    expenses = db_connect.fetch_expenses_for_date('2024-08-15')
    assert len(expenses) == 1 
    expenses[0]['amount'] == 10.0