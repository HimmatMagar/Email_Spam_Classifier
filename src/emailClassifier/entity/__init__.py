from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
      root_dir: Path
      data_path: str
      zip_file: Path
      unzip_file: Path
