from src.emailClassifier import loger
from src.emailClassifier.config import ConfigurationManager
from src.emailClassifier.components.data_transformation import DataTransform

STAGE_NAME = "Data Transformation Config"

class DataTransformPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            data_transform_config = config.get_data_transformation_config()
            data_transform = DataTransform(data_transform_config)
            data_transform.split_data()

if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = DataTransformPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 