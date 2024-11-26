#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

app = FastAPI()

with open('family.pickle', 'rb') as file:
    loaded_model = pickle.load(file)

class InputData(BaseModel):
    c: str
    a: float
    i: float
    s: float
    me: float
    lp: float
    ccs: float
    d: int

@app.post("/predict")
async def predict(data: InputData):
    try:
        X = pd.read_csv('X.csv')
        new_row = {
            'Category': data.c,
            'Amount': data.a,
            'Income': data.i,
            'Savings': data.s,
            'Monthly Expenses': data.me,
            'Loan Payments': data.lp,
            'Credit Card Spending': data.ccs,
            'Dependents': data.d
        }
        input_df = pd.concat([X, pd.DataFrame([new_row])], ignore_index=True)
        preprocessor = ColumnTransformer(
            transformers=[('Category', OneHotEncoder(), [0])],
            remainder='passthrough'
        )
        input_df_pre = preprocessor.fit_transform(input_df)
        scaler = StandardScaler()
        input_scaled = scaler.fit_transform(input_df_pre)
        last_row_transformed = input_scaled[-1].reshape(1, -1)
        prediction = loaded_model.predict(last_row_transformed)
        return {"prediction": prediction.tolist()}

    except Exception as e:
        return {"error": str(e)}
