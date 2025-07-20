from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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
    return {"satatus":"running"}

@app.post("/predict")
def predict(data: Input):
    val = pd.DataFrame([[data.sex, int(data.age), int(data.pclass)]], columns=["Sex", "Age", "Pclass"])
    prediction = out = model.predict(val)
    return {"prediction": str("Survived" if prediction[0] else "Died")}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)