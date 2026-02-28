from src.emailClassifier import loger
from src.emailClassifier.config import ConfigurationManager
from src.emailClassifier.components.mode_eval import ModelEval

STAGE_NAME = "Model Eval Stage"

class ModelEvalPipeline:
      def __init__(self):
            pass

      def main(self):
            config = ConfigurationManager()
            model_eval_config = config.get_model_eval_config()
            model_eval = ModelEval(model_eval_config)
            model_eval.eval_model()


if __name__ == "__main__":
      try:
            loger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
            obj = ModelEvalPipeline()
            obj.main()
            loger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
      except Exception as e:
            loger.exception(e)
            raise e 