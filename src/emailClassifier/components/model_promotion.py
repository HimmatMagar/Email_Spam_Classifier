import mlflow
from pathlib import Path
from emailClassifier import loger
from mlflow.client import MlflowClient
from emailClassifier.utils import load_file
from mlflow.exceptions import MlflowException
from emailClassifier.entity import ModelPromoteConfig
from sklearn.metrics import precision_score, f1_score, recall_score
from emailClassifier.utils.mlflow_manager import configure_mlflow, load_run_id



class ModelPromotion:
    def __init__(self, chall_name, champ_name, chall_alias, champ_alias, config: ModelPromoteConfig):
        self.chall_name = chall_name
        self.champ_name = champ_name
        self.chall_alias = chall_alias
        self.champ_alias = champ_alias
        self.config = config
        self.client = MlflowClient()

    def _load_test_file(self):
        xtest = load_file(Path(self.config.x_test))
        ytest = load_file(Path(self.config.y_test))
        loger.info("Test file loaded successfully")
        return xtest, ytest
    
    
    def _evaluate(self, name, alias):
        x_test, y_test = self._load_test_file()
        model = mlflow.pyfunc.load_model(f"models:/{name}@{alias}")
        loger.info(f"{alias} model loaded successfully from mlflow registry!!")
        p = model.predict(x_test)
        return {
            "precision": precision_score(y_test, p),
            "recall": recall_score(y_test, p),
            "f1": f1_score(y_test, p)
        }


    def _select_champion_model(self):
        model_promotion = self.champ_name
        chall = self._evaluate(
            name=self.chall_name,
            alias=self.chall_alias
        )
        loger.info("Champion model metrics: %s", chall)
        
        try:
            champ = self._evaluate(
                name=self.champ_name,
                alias= self.champ_alias
            )
            loger.info("Champion model metrics: %s", champ)
            better = (
                chall["f1"] > champ["f1"] + 0.002 and
                chall["precision"] >= champ["precision"] - 0.005 and
                chall["recall"] >= champ["recall"] - 0.01
            )
        except MlflowException:
            champ, better = None, chall["precision"] >= 0.96

        v = self.client.get_model_version_by_alias(
            self.chall_name,
            self.chall_alias
        ).version
        
        if better:
            if champ:
                old_champ = self.client.get_model_version_by_alias(self.champ_name, self.champ_alias).version
                self.client.set_registered_model_alias(self.champ_name, "previous", old_champ)
            self.client.set_registered_model_alias(self.chall_name, "champion", v)
            self.client.set_model_version_tag(self.chall_name, v, "validation", "Promoted")
            model_promotion = self.chall_name
            print(f"v: {v} promoted to champion")
            loger.info(f"v: %s promoted to champion", v)
        else:
            self.client.set_registered_model_alias(self.chall_name, "archived", v)
            loger.info("Registred model: %s alias set to archived", self.chall_name)
            self.client.set_model_version_tag(self.chall_name, v, "validation", "rejected")
            print(f"v: {v} rejected, champion unchanged")
            loger.info("v: %s rejected, champion unchanged", v)

        return model_promotion