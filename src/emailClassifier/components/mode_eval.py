import joblib
from pathlib import Path
from box.config_box import ConfigBox
from emailClassifier import loger
from emailClassifier.utils import *
from emailClassifier.entity import ModelEvalConfig
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score



class ModelEval:
      def __init__(self, config: ModelEvalConfig):
            self.config = config

      
      def eval_model(self) -> None:
            xVal = load_file(Path(self.config.xval_file))
            yVal = load_file(Path(self.config.yval_file))
            model = joblib.load(self.config.model)

            yPred = model.predict(xVal)

            Model_Performance = {
                  "accuracy": accuracy_score(yVal, yPred),
                  "precision": precision_score(yVal, yPred, zero_division=0),
                  "recall": recall_score(yVal, yPred, zero_division=0),
                  "f1": f1_score(yVal, yPred, zero_division=0)
            }

            save_file(Path(self.config.metric), Model_Performance)
            loger.info(f"Model evaluation completed and report saved on {self.config.metric}")

            return Model_Performance
