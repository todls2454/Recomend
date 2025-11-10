# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# 여기서 우리가 만든 SimpleRecommender 객체를 읽어온다
model = joblib.load("model.pkl")

class UserInput(BaseModel):
    user_id: str
    k: int = 5  # 몇 개 추천받을지

@app.post("/recommend")
def recommend(data: UserInput):
    recs = model.recommend(data.user_id, k=data.k)
    return {"user_id": data.user_id, "recommendations": recs}