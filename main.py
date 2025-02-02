# backend/main.py (FastAPI Backend for Expense Tracker)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Replace with your Firebase service account JSON
initialize_app(cred)
db = firestore.client()
expenses_ref = db.collection("expenses")

app = FastAPI()

# Expense Model
class Expense(BaseModel):
    amount: float
    category: str
    date: str  # YYYY-MM-DD
    notes: str

# API: Add an Expense
@app.post("/add_expense/")
def add_expense(expense: Expense):
    try:
        expense_data = expense.dict()
        expenses_ref.add(expense_data)
        return {"message": "Expense added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API: Get All Expenses
@app.get("/expenses/")
def get_expenses():
    try:
        expenses = [doc.to_dict() for doc in expenses_ref.stream()]
        return {"expenses": expenses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API: Delete Expense (by ID)
@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: str):
    try:
        expenses_ref.document(expense_id).delete()
        return {"message": "Expense deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

