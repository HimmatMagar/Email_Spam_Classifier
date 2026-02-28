from src.emailClassifier import loger
from src.emailClassifier.pipeline.model_eval_pipeline import ModelEvalPipeline
from src.emailClassifier.pipeline.model_build_pipeline import BuildModelPipeline
from src.emailClassifier.pipeline.data_transform_pipeline import DataTransformPipeline
from src.emailClassifier.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.emailClassifier.pipeline.data_validation_pipeline import DataValidationPipeline



STAGE_NAME = "Data Ingestion Stage"
try:
      loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
      obj = DataIngestionPipeline()
      obj.main()
      loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
except Exception as e:
      loger.exception(e)
      raise e

STAGE_NAME = "Data Validation Stage"
try:
      loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
      obj = DataValidationPipeline()
      obj.main()
      loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
except Exception as e:
      loger.exception(e)
      raise e


STAGE_NAME = "Data Transformation Stage"
try:
      loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
      obj = DataTransformPipeline()
      obj.main()
      loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
except Exception as e:
      loger.exception(e)
      raise e


STAGE_NAME = "Model Building Stage"
try:
      loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
      obj = BuildModelPipeline()
      obj.main()
      loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
except Exception as e:
      loger.exception(e)
      raise e



STAGE_NAME = "Model Eval Stage"
try:
      loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
      obj = ModelEvalPipeline()
      obj.main()
      loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
except Exception as e:
      loger.exception(e)
      raise e