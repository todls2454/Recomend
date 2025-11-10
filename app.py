# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# 이 줄이 있으면 피클이 클래스를 찾기 쉬움
import recommender  # noqa: F401

app = FastAPI()

model = joblib.load("model.pkl")

class UserInput(BaseModel):
    user_id: str
    k: int = 5

@app.post("/recommend")
def recommend(data: UserInput):
    recs = model.recommend(data.user_id, k=data.k)
    return {"user_id": data.user_id, "recommendations": recs}