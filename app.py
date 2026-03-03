import pandas as pd
from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from src.emailClassifier.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI(title="Email Spam Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
      text: Annotated[str, Field(..., description=("Give the email text to classify the email"))]

predict_pipe = PredictionPipeline()

@app.get("/")
async def home():
      return {'message': "Welcome to email spam classifier"}

@app.get("/train")
async def train_model():
      pass

@app.post("/predict")
async def predict_spam_email(UserInput: Input):
      data = pd.DataFrame([{
            'text': UserInput.text
      }])

      transformed_data = predict_pipe.transform_user_data(data)

      vectorized_data = predict_pipe.vectorize_data(transformed_data)

      prediction = predict_pipe.predict_spam(vectorized_data)

      return {
            "prediction": prediction,
            "label": "spam" if prediction == 1 else "not spam",
            "status": 200
      }
