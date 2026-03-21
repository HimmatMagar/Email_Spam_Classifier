import mlflow
import joblib
from pathlib import Path
from src.emailClassifier.utils.mlflow_manager import configure_mlflow, load_run_id


class PredictionPipeline:
      def __init__(self):
            """Initialize the prediction pipeline by loading trained model and vectorizer."""
            try:
                  self.model = mlflow.pyfunc.load_model("models:/SpamClassifierSVC/production")
                  configure_mlflow(experiment_name="spam-classifier")
                  local_path = mlflow.artifacts.download_artifacts(
                        run_id=load_run_id(),
                        artifact_path="vectorizer.pkl"
                  )
                  with open(local_path, 'r') as f:
                        self.vectorizer = joblib.load(f)
            except FileNotFoundError as e:
                  raise FileNotFoundError(f"Model or vectorizer file not found: {e}")
            except Exception as e:
                  raise Exception(f"Error loading model: {e}")

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