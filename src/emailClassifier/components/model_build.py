import os
import joblib
from pathlib import Path
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from emailClassifier.utils import *
from emailClassifier import loger
from emailClassifier.entity import ModelBuilingConfig


class BuildModel:
      def __init__(self, config: ModelBuilingConfig):
            self.config = config

      
      def build_model_architecture(self):
            xtrain = load_file(Path(self.config.xtrain_data))
            ytrain = load_file(Path(self.config.ytrain_data))

            rfc_model = RandomForestClassifier(
                  n_estimators=self.config.n_estimators,
                  min_samples_split=self.config.min_samples_split,
                  min_samples_leaf=self.config.min_samples_leaf
            )

            rfc_model.fit(xtrain, ytrain)

            model_path = os.path.join(self.config.root_dir, self.config.model)
            with open(model_path, "wb") as f:
                  joblib.dump(rfc_model, f)
            
            loger.info(f"Model building successfully in: {model_path}")
            return rfc_model