from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
      root_dir: Path
      data_path: str
      zip_file: Path
      unzip_file: Path


@dataclass
class DataValidationConfig:
      root_dir: Path
      data_path: Path
      status_file: str
      schema: dict