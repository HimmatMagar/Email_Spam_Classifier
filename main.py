from src.emailClassifier import loger
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