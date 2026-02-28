import joblib
from pathlib import Path
from box.config_box import ConfigBox
from src.emailClassifier import loger
from src.emailClassifier.utils import *
from sklearn.metrics import classification_report
from src.emailClassifier.entity import ModelEvalConfig



class ModelEval:
      def __init__(self, config: ModelEvalConfig):
            self.config = config


      def metrics(self, actual, pred) -> ConfigBox:
            data = classification_report(actual, pred, output_dict=True)
            return ConfigBox(data)
      
      
      def eval_model(self) -> None:
            x_val = load_file(Path(self.config.xval_file))
            y_val = load_file(Path(self.config.yval_file))
            model = joblib.load(self.config.model)

            y_pred = model.predict(x_val)
            evaluation = self.metrics(y_val, y_pred)

            Model_Performance = {
                  'Class_0': {
                        'precision': evaluation['0']['precision'],
                        'recall': evaluation['0']['recall'],
                        'f1-score': evaluation['0']['f1-score'],
                        'support': evaluation['0']['support']
                  },
                  'Class_1': {
                        'precision': evaluation['1']['precision'],
                        'recall': evaluation['1']['recall'],
                        'f1-score': evaluation['1']['f1-score'],
                        'support': evaluation['1']['support']
                  },
                  'accuracy': evaluation['accuracy']
            }

            save_file(Path(self.config.metric), Model_Performance)
            loger.info(f"Model evaluation completed and report saved on {self.config.metric}")
