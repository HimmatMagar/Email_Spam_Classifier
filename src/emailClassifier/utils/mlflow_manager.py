import os
import mlflow
import dagshub
from dotenv import load_dotenv

# load .env file
load_dotenv()

def configure_mlflow():
    dagshub.init(
        repo_owner='HimmatMagar',
        repo_name='Email_Spam_Classifier',
        mlflow=True
    )
    
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))