import os
import zipfile
import urllib.request as r
from src.emailClassifier import loger
from src.emailClassifier.entity import DataIngestionConfig


class DataIngestion:
      def __init__(self, config: DataIngestionConfig):
            self.config = config

      def download_file(self):
            if not os.path.exists(self.config.ziped_file):
                  filename, header = r.urlretrieve(
                        url = self.config.source_url,
                        filename=self.config.ziped_data_path
                  )
                  loger.info(f"{filename} download with fillowing {header}")
            else:
                  loger.info("file already exist")


      def extract_zip_file(self):
            file = self.config.unzip_file
            os.makedirs(file, exist_ok=True)
            with zipfile.ZipFile(self.config.ziped_data_path, 'r') as f:
                  f.extractall(file)