from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel
import pandas as pd

model = joblib.load("titanic_model.pkl")

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