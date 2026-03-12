import mlflow
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.mode_eval import ModelEval
from emailClassifier.utils.mlflow_manager import configure_mlflow

STAGE_NAME = "Model Eval Stage"

class ModelEvalPipeline:
      def __init__(self):
            pass

      def return_run_id(self):
            try:
                  with open("artifact/run_id.txt", "r") as f:
                        id = f.read()
                        return id
            except FileNotFoundError as e:
                  raise e
      
      def return_version(self):
            try:
                  with open("artifact/model_version.txt", "r") as f:
                        model_version = f.read().strip()
                        return model_version
            except FileNotFoundError as e:
                  raise e
      

      def main(self):
            config = ConfigurationManager()
            model_eval_config = config.get_model_eval_config()
            
            id = self.return_run_id()
            version = self.return_version()

            configure_mlflow()
            client = mlflow.tracking.MlflowClient()
            with mlflow.start_run(run_id=id):
                  model_eval = ModelEval(model_eval_config)
                  metrics = model_eval.eval_model()

                  mlflow.log_metrics({
                        "accuracy": metrics["accuracy"],
                        "class0_precision": metrics["Class_0"]["precision"],
                        "class0_recall":    metrics["Class_0"]["recall"],
                        "class0_f1":        metrics["Class_0"]["f1-score"],
                        "class1_precision": metrics["Class_1"]["precision"],
                        "class1_recall":    metrics["Class_1"]["recall"],
                        "class1_f1":        metrics["Class_1"]["f1-score"],
                  })

                  ACCURACY_THRESHOLD = 0.90
                  if metrics["accuracy"] >= ACCURACY_THRESHOLD:
                        current_production = client.get_latest_versions(
                              name="EmailClassifierSVC",
                              stages=["Production"]
                        )

                        for prod_model in current_production:
                              client.transition_model_version_stage(
                                    name="EmailClassifierSVC",
                                    version=prod_model.version,
                                    stage="Archived"             # ← archive old production
                              )
                              loger.info(f"Archived old version={prod_model.version}")

                        # promote staging to production
                        client.transition_model_version_stage(
                              name="EmailClassifierSVC",
                              version=version,
                              stage="Production"
                        )
                        loger.info("Model moved to production")
                  else:
                        client.transition_model_version_stage(
                              name="EmailClassifierSVC",
                              version=version,
                              stage="Archived"
                        )
                  

if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = ModelEvalPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 