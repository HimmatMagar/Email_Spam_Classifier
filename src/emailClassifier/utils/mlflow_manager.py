import os
import mlflow
import dagshub
from emailClassifier import logger

class MLflowManager:
    def __init__(self, tracking_uri, experiment_name):
        # Initialize dagshub
        dagshub.init(
            repo_owner=os.getenv("DAGSHUB_USERNAME"),
            repo_name=os.getenv("DAGSHUB_REPO"),
            mlflow=True
        )
        
        # Set tracking URI
        mlflow.set_tracking_uri(tracking_uri)
        
        # Set experiment
        mlflow.set_experiment(experiment_name)
        logger.info(f"MLflow tracking URI: {tracking_uri}")
        logger.info(f"Experiment: {experiment_name}")

    def start_run(self, run_name=None):
        return mlflow.start_run(run_name=run_name)

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict):
        mlflow.log_metrics(metrics)

    def log_model(self, model, model_name):
        mlflow.sklearn.log_model(model, model_name)

    def end_run(self):
        mlflow.end_run()