from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import joblib
from pydantic import BaseModel
import pandas as pd
import uvicorn
import os

model_path = os.path.join(os.path.dirname(__file__), "titanic_model.pkl")
model = joblib.load(model_path)

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_methods=['*'],  # Allow all HTTP methods
    allow_headers=['*']  # Allow all headers
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("frontend/index.html", "r") as f:
        return f.read()

class Input(BaseModel):
    sex:str
    age:int
    pclass:int

@app.get("/status")
def status():
    return {"status":"sab thik chal raha hai ✅"}

@app.post("/predict")
def predict(data: Input):
    val = pd.DataFrame([[data.sex, int(data.age), int(data.pclass)]], columns=["Sex", "Age", "Pclass"])
    prediction = out = model.predict(val)
    return {"prediction": str("Survived" if prediction[0] else "Died")}
