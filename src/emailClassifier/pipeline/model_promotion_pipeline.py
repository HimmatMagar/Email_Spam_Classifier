import mlflow
from emailClassifier import loger
from emailClassifier.config import ConfigurationManager
from emailClassifier.components.model_promotion import ModelPromotion

STAGE_NAME = "Model Promotion Stage"

class ModelEvalPipeline:
      def __init__(self):
            pass

      def main(self):
            chall_name = ""
            champ_name = "EmailClassifierSVC"
            chall_alias = "Challenger"
            champ_alias = "Champion"

            config = ConfigurationManager()
            model_promote_config = config.get_model_promote_config()

            model_promotion = ModelPromotion(
                  chall_name=chall_name,
                  champ_name=champ_name,
                  chall_alias=chall_alias,
                  champ_alias=champ_alias,
                  config=model_promote_config
            )
            model_promotion._select_champion_model()
            loger.info("Model Promotion stage complete")

if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = ModelEvalPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 