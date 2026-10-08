from emailClassifier import loger
from fastapi import FastAPI, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from emailClassifier.pipeline.prediction_pipeline import PredictionPipeline


predict_pipe = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global predict_pipe
    loger.info("Loading prediction model....")
    predict_pipe = PredictionPipeline()
    loger.info("Model loaded successfully....")
    yield

app = FastAPI(title="Email Spam Classifier", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Input(BaseModel):
      text: Annotated[str, Field(..., description=("Give the email text to classify the email"))]

class ResponseModel(BaseModel):
      prediction: int
      label: str      


@app.get("/")
async def home():
      return {'message': "Welcome to email spam classifier"}


@app.get("/health")
async def health():
      model = PredictionPipeline is not None
      status = 'Ok' if model else "Degraded"
      code = 200 if model else 503
      return JSONResponse(
            status_code=code,
            content={
                  "status": status,
                  "model_loaded": model
            }
      )

@app.post("/predict", response_model=ResponseModel)
async def predict_spam_email(UserInput: Input):
      if predict_pipe is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
      
      prediction = predict_pipe.predict_spam(UserInput.text)

      return ResponseModel(
            prediction = prediction,
            label = "spam" if prediction == 1 else "ham",
      )
