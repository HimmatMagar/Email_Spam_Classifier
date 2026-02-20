import os
import logging
from pathlib import Path


logging.basicConfig(
      level=logging.INFO,
      format="[%(asctime)s: %(message)s]"
)


project_name = "emailClassifier"

list_of_file = [
      f"src/{project_name}/__init__.py",
      f"src/{project_name}/components/__init__.py",
      f"src/{project_name}/utils/__init__.py",
      f"src/{project_name}/config/__init__.py",
      f"src/{project_name}/pipeline/__init__.py",
      f"src/{project_name}/entity/__init__.py",
      f"src/{project_name}/constants/__init__.py",
      "config/config.yaml",
      "params.yaml",
      "schema.yaml",
      "main.py",
      "app.py",
      "requirements.txt",
      "setup.py",
      "research/trials.ipynb",
      "templates/index.html"
]

for filepath in list_of_file:
      file = Path(filepath)

      filedir, filename = os.path.split(file)

      if filedir != "" :
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"File directory created: {filedir} for {filename}")

      if (not os.path.exists(file)) or (os.path.getsize(file) == 0):
            with open(file, 'w') as f:
                  pass
                  logging.info(f"Creating file: {file}")

      else:
            logging.info("File already exist")
