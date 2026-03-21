import os
import mlflow
import mlflow.sklearn
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.model_build import BuildModel
from emailClassifier.utils.mlflow_manager import configure_mlflow, save_run_id

STAGE_NAME = "Model Building Stage"

class BuildModelPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            model_build_config = config.get_model_building_config()

            configure_mlflow(experiment_name="Email-Spam")

            with mlflow.start_run(run_name="SVM-Model") as run:
                  try:
                        mlflow.log_params({
                              "C": model_build_config.C,
                              "kernel": model_build_config.kernel,
                              "gamma": model_build_config.gamma
                        })
                        model = BuildModel(model_build_config)
                        model_svc = model.build_model_architecture()
                        print(f"model built: {model_svc}")
                        
                        logged_model = mlflow.sklearn.log_model(
                              sk_model=model_svc,
                              artifact_path="model"
                        )
                        with open("artifact/model_id.txt", "w") as f:
                              f.write(logged_model.model_id)
                        loger.info(f"Model logged successfully and id saved in artifact/model_id")

                        vecPath = "artifact/data_transformation/vectorizer.pkl"
                        print(f"vectorizer exists: {os.path.exists(vecPath)}")
                        mlflow.log_artifact(
                              local_path    = vecPath,
                              artifact_path = "vectorizer"
                        )

                        save_run_id(run.info.run_id)
                  except Exception as e:
                        print(f"Training Failed {e}")
                        raise e




if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = BuildModelPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 