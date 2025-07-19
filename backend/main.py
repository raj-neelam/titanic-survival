from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel
import pandas as pd
import uvicorn
import os

model = joblib.load("backend/titanic_model.pkl")

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_methods=['*'],  # Allow all HTTP methods
    allow_headers=['*']  # Allow all headers
)


class Input(BaseModel):
    sex:str
    age:int
    pclass:int

@app.post("/predict")
def predict(data: Input):
    val = pd.DataFrame([[data.sex, int(data.age), int(data.pclass)]], columns=["Sex", "Age", "Pclass"])
    prediction = out = model.predict(val)
    return {"prediction": str("Survived" if prediction[0] else "Died")}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)