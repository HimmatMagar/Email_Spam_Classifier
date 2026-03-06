import joblib
from pathlib import Path


class PredictionPipeline:
      def __init__(self):
            """Initialize the prediction pipeline by loading trained model and vectorizer."""
            try:
                  self.model = joblib.load(Path('artifact/build_model/model.pkl'))
                  self.vectorizer = joblib.load(Path('artifact/data_transformation/vectorizer.pkl'))
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