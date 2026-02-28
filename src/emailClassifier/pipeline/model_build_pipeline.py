from src.emailClassifier import loger
from src.emailClassifier.config import ConfigurationManager
from src.emailClassifier.components.model_build import BuildModel

STAGE_NAME = "Model Building Stage"

class BuildModelPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            model_build_config = config.get_model_building_config()
            model = BuildModel(model_build_config)
            model.build_model_architecture()


if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = BuildModelPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 