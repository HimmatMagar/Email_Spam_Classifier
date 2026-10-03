import pytest
from emailClassifier.pipeline.prediction_pipeline import PredictionPipeline

model = PredictionPipeline()

def test_predicts_valid_labels(model):
    preds = model.predict_spam(["hello friend", "WIN a free prize now"])
    assert set(preds) <= {"spam", "ham"}


@pytest.mark.parametrize("text", [
    "Congratulations! You won a $1000 gift card. Click here to claim now!!!",
    "FREE viagra, limited offer, act now",
])
def test_obvious_spam(model, text):
    assert model.predict_spam([text])[0] == "spam"


@pytest.mark.parametrize("text", [
    "Hi John, the meeting is moved to 3pm tomorrow.",
    "Can you send me the report by Friday? Thanks.",
])
def test_obvious_ham(model, text):
    assert model.predict_spam([text])[0] == "ham"


def test_invariant_to_case_and_whitespace(model):
    a = model.predict_spam(["Win a FREE prize now"])[0]
    b = model.predict_spam(["  win a free prize now  "])[0]
    assert a == b