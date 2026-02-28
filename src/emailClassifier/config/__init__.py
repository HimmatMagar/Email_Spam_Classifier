from src.emailClassifier.utils import *
from src.emailClassifier.constants import *
from src.emailClassifier.entity import *


class ConfigurationManager:
      def __init__(self, config=CONFIG_PATH, params=PARAMS_PATH, schema=SCHEMA_PATH):
            self.config = read_yaml(config)
            self.params = read_yaml(params)
            self.schema = read_yaml(schema)

            create_dir([self.config.artifact_root])
      

      def get_data_ingestion_config(self) -> DataIngestionConfig:
            config = self.config.data_ingestion
            create_dir([config.root_dir])

            data_ingestion_config = DataIngestionConfig(
                  root_dir=config.root_dir,
                  data_path=config.data_path,
                  zip_file=config.zip_file,
                  unzip_file=config.unzip_file
            )

            return data_ingestion_config
      

      def get_data_validation_config(self) -> DataValidationConfig:
            config = self.config.data_validation
            create_dir([config.root_dir])

            schema = self.schema.COLUMN

            data_validation_config = DataValidationConfig(
                  root_dir= config.root_dir,
                  data_path=config.data_path,
                  status_file=config.status_file,
                  schema=schema
            )

            return data_validation_config
      

      def get_data_transformation_config(self) -> DataTransformationConfig:
            config = self.config.data_transformation
            create_dir([config.root_dir])

            data_transformation_config = DataTransformationConfig(
                  root_dir=config.root_dir,
                  data_path=config.data_path
            )

            return data_transformation_config

      def get_model_building_config(self) -> ModelBuilingConfig:
            config = self.config.model_building

            create_dir([config.root_dir])
            params = self.params.SVC

            model_building_config = ModelBuilingConfig(
                  root_dir = config.root_dir,
                  xtrain_data = config.xtrain_data,
                  ytrain_data = config.ytrain_data,
                  model = config.model,
                  C = params.C,
                  kernel = params.kernel,
                  gamma = params.gamma
            )

            return model_building_config