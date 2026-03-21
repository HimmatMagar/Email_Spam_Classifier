import mlflow
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.mode_eval import ModelEval
from emailClassifier.utils.mlflow_manager import configure_mlflow, load_run_id

STAGE_NAME = "Model Eval Stage"

class ModelEvalPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            model_eval_config = config.get_model_eval_config()

            run_id = load_run_id()

            try:
                  with open("artifact/model_id.txt", 'r') as f:
                        model_id = f.read()
            except FileNotFoundError as e:
                  raise

            configure_mlflow(experiment_name="Email-Spam")
            with mlflow.start_run(run_id=run_id):
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

                  ACCURACY_THRESHOLD = 0.92
                  if metrics["accuracy"] >= ACCURACY_THRESHOLD:
                        model = mlflow.register_model(
                              model_uri=f"models:/{model_id}",
                              name = "SpamClassifierSVC"
                        )
                        loger.info(f"Registered — accuracy: {metrics['accuracy']}")

                        client = mlflow.tracking.MlflowClient()
                        client.transition_model_version_stage(
                              name="SpamClassifierSVC",
                              version=model.version,
                              stage="Staging"
                        )
                  else:
                        loger.warning(f"Not registered — accuracy: {metrics['accuracy']} below threshold")
                  

if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = ModelEvalPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 