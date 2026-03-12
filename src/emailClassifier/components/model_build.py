import os
import joblib
from pathlib import Path
from sklearn.svm import SVC
from emailClassifier.utils import *
from emailClassifier import loger
from emailClassifier.entity import ModelBuilingConfig


class BuildModel:
      def __init__(self, config: ModelBuilingConfig):
            self.config = config

      
      def build_model_architecture(self):
            xtrain = load_file(Path(self.config.xtrain_data))
            ytrain = load_file(Path(self.config.ytrain_data))

            svc_model = SVC(
                  C = self.config.C,
                  kernel = self.config.kernel,
                  gamma = self.config.gamma
            )

            svc_model.fit(xtrain, ytrain)

            model_path = os.path.join(self.config.root_dir, self.config.model)
            with open(model_path, "wb") as f:
                  joblib.dump(svc_model, f)
            
            loger.info(f"Model building successfully in: {model_path}")
            return svc_model