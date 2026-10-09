import mlflow
from mlflow.client import MlflowClient
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.mode_eval import ModelEval
from emailClassifier.utils.mlflow_manager import configure_mlflow, load_run_id

STAGE_NAME = "Model Eval Stage"

class ModelEvalPipeline:
      def __init__(self):
            pass

      def main(self):
            client = MlflowClient()
            config = ConfigurationManager()
            model_eval_config = config.get_model_eval_config()

            run_id = load_run_id()

            configure_mlflow(experiment_name="Email-Spam")
            with mlflow.start_run(run_id=run_id):
                  model_eval = ModelEval(model_eval_config)
                  metrics = model_eval.eval_model()

                  mlflow.log_metrics(metrics)

                  versions = client.search_model_versions(f"run_id='{run_id}'")
                  latest_version = max(versions, key=lambda mv: int(mv.version)).version
                  model_name = versions[-1].name
                  client.set_registered_model_alias(model_name, "challenger", latest_version)
                  

if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = ModelEvalPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 