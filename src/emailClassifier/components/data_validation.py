import pandas as pd
from src.emailClassifier import loger
from src.emailClassifier.entity import DataValidationConfig


class DataValidation:
      def __init__(self, config: DataValidationConfig):
            self.config = config

      def validate_column(self):
            try:
                  data = pd.read_csv(self.config.data_path)

                  data_col = list(data.columns)
                  schema = self.config.schema

                  for col in data_col:
                        if col not in schema:
                              validation_status = False
                              with open(self.config.status_file, 'w') as f:
                                    f.write(f"Validation Status: {validation_status}")
                        else:
                              validation_status = True
                              with open(self.config.status_file, 'w') as f:
                                    f.write(f"Validation Status: {validation_status}")
                                    
                  loger.info("Validation status written successfully")
            
            except Exception:
                 raise Exception