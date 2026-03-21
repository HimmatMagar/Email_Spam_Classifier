import os
import mlflow
import dagshub
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Initialize dagshub once at module level
_DAGSHUB_INITIALIZED = False

def _initialize_dagshub():
    global _DAGSHUB_INITIALIZED
    if not _DAGSHUB_INITIALIZED:
        dagshub.init(
            repo_owner='HimmatMagar',
            repo_name='Email_Spam_Classifier',
            mlflow=True
        )
        _DAGSHUB_INITIALIZED = True

def configure_mlflow(experiment_name: str) -> None:
    _initialize_dagshub()
    
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        raise ValueError("MLFLOW_TRACKING_URI environment variable is not set")
    
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name=experiment_name)
    print(f"Mlflow -> Dagshub | Experiment: {experiment_name}")


def save_run_id(run_id: str, path: str = "artifact/run_id.txt") -> None:
    try:
        with open(path, "w") as f:
            f.write(run_id)
    except Exception as e:
        raise e


def load_run_id(path: str = "artifact/run_id.txt") -> None:
    try:
        with open(path) as f:
            id = f.read().strip()
            return id
    except FileNotFoundError as e:
        raise e