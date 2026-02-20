import os
import yaml
import json
import pickle
from pathlib import Path
from box.config_box import ConfigBox
from src.emailClassifier import loger
from ensure import ensure_annotations
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(file_path: Path) -> ConfigBox:
      try:
            with open(file_path, 'r') as f:
                  data = yaml.safe_load(f)
                  loger.info(f"Yaml file loaded from: {file_path}")
                  return ConfigBox(data)
      except BoxValueError:
            raise ValueError("yaml file is empty")
      except Exception as e:
            raise e
      

@ensure_annotations
def create_dir(file_path: list, verbose = True):
      for filename in file_path:
            os.makedirs(filename, exist_ok=True)

            if verbose:
                  loger.info(f"file directory {filename} created successfully")


@ensure_annotations
def load_file(file_path: Path):
      try:
            with open(file_path, 'rb') as f:
                  data = pickle.load(f)
                  loger.info(f"Pickle file {file_path} loaded successfully")
                  return data
      except BoxValueError:
            raise ValueError("Pickle file is empty")
      except Exception as e:
            raise e


@ensure_annotations
def save_file(file_path: Path, data: dict):
      try:
            with open(file_path, 'w') as f:
                  json.dump(data, f, indent=4)
            loger.info(f"json file {file_path} saved successfully")
      except Exception as e:
            raise e