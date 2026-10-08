import numpy as np
from src.emailClassifier.pipeline.prediction_pipeline import PredictionPipeline


def test_pipeline_load():
    pipe = PredictionPipeline()
    assert pipe is not None


def test_pipeline_returns_int_like():
    pipe = PredictionPipeline()
    pred = pipe.predict_spam("win a free prize now")
    assert int(pred) in (0, 1)


def test_pipeline_deterministic():
    pipe = PredictionPipeline()
    text = "limited time offer, act now"
    a = int(pipe.predict_spam(text))
    b = int(pipe.predict_spam(text))
    assert a == b 