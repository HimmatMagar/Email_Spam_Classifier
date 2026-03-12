import mlflow
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.model_build import BuildModel
from emailClassifier.utils.mlflow_manager import configure_mlflow

STAGE_NAME = "Model Building Stage"

class BuildModelPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            model_build_config = config.get_model_building_config()

            configure_mlflow()
            mlflow.set_experiment("Email-Classifier")

            with mlflow.start_run(run_name="SVC_Model") as run:
                  mlflow.log_params({
                        "C": model_build_config.C,
                        "kernel": model_build_config.kernel,
                        "gamma": model_build_config.gamma
                  })
                  model = BuildModel(model_build_config)
                  svc_model = model.build_model_architecture()

                  model_info = mlflow.sklearn.log_model(
                        sk_model=svc_model,
                        artifact_path="model",
                        registered_model_name="EmailClassifierSVC"
                  )
                  loger.info("Model registered")

                  client = mlflow.tracking.MlflowClient()
                  model_version = client.get_latest_versions(
                        name="EmailClassifierSVC",
                        stages=["None"]                             # ← newly registered = "None" stage
                  )[0].version

                  client.transition_model_version_stage(
                        name="EmailClassifierSVC",
                        version=model_version,
                        stage="Staging"
                  )

                  with open("artifact/run_id.txt", "w") as f:
                        f.write(run.info.run_id)

                  with open("artifact/model_version.txt", "w") as f:
                        f.write(model_version)


if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = BuildModelPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 