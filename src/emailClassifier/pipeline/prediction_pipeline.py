import mlflow
import joblib
from pathlib import Path
from emailClassifier import loger
from emailClassifier.utils.mlflow_manager import configure_mlflow, load_run_id


class PredictionPipeline:
      def __init__(self):
            """Initialize the prediction pipeline by loading trained model and vectorizer."""
            try:
                  self.model = mlflow.pyfunc.load_model(
                        "models:/SpamClassifierSVC/Production"
                  )

                  artifact_path = mlflow.artifacts.download_artifacts(
                        run_id=load_run_id(),
                        artifact_path="vectorizer/vectorizer.pkl"
                  )

                  with open(artifact_path, "rb") as f:
                        self.vectorizer = joblib.load(f)
                  loger.info("Model and vectorizer loaded successfully")

            except FileNotFoundError as e:
                  loger.error(f"Error loading model: {e}")
                  raise

      def predict_spam(self, data):
            """
            Predict if email text is spam or not.
            
            Args:
                data (str): Raw email text to classify
                
            Returns:
                int: 0 for legitimate email, 1 for spam
                
            Raises:
                ValueError: If input data is not a string
            """
            if not isinstance(data, str):
                  raise ValueError("Input data must be a string")
            
            if not data or not data.strip():
                  raise ValueError("Input data cannot be empty")
            
            try:
                  # Vectorizer pipeline handles both cleaning and vectorization
                  x_data = self.vectorizer.transform([data])
                  
                  # Make prediction
                  prediction = self.model.predict(x_data)
                  
                  return int(prediction[0])
            except Exception as e:
                  raise Exception(f"Error during prediction: {e}")