from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
      root_dir: Path
      data_path: str
      zip_file: Path
      unzip_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
      root_dir: Path
      data_path: Path
      status_file: str
      schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
      root_dir: Path
      data_path: Path


@dataclass(frozen=True)
class ModelBuilingConfig:
      root_dir: Path
      xtrain_data: Path
      ytrain_data: Path
      model: str
      C: int
      kernel: str
      gamma: str

