#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import json

with open('columns.json', 'r') as file:
    data = json.load(file)
    category_options = data['category_columns']

def make_prediction(data):
    url = "http://localhost:8501/predict"  # Ensure FastAPI server is running at this URL
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error if the response status code is not 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error making prediction: {e}")
        return None

st.title("Prediction App")

category = st.selectbox("Category", category_options)
amount = st.number_input("Amount", value=0.0, format="%.2f")
income = st.number_input("Income", value=0.0, format="%.2f")
savings = st.number_input("Savings", value=0.0, format="%.2f")
monthly_expenses = st.number_input("Monthly Expenses", value=0.0, format="%.2f")
loan_payments = st.number_input("Loan Payments", value=0.0, format="%.2f")
credit_card_spending = st.number_input("Credit Card Spending", value=0.0, format="%.2f")
dependents = st.number_input("Dependents", value=0, step=1, format="%d")

if st.button("Predict"):
    data = {
        "c": category,
        "a": float(amount),
        "i": float(income),
        "s": float(savings),
        "me": float(monthly_expenses),
        "lp": float(loan_payments),
        "ccs": float(credit_card_spending),
        "d": int(dependents),
    }
    prediction = make_prediction(data)
    if prediction and "prediction" in prediction:
        st.write("Prediction:", prediction["prediction"])
    else:
        st.write("Error: No prediction received.")
