import os
import joblib
import pandas as pd
from emailClassifier import loger
from emailClassifier.utils import *
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from emailClassifier.utils.text_cleaner import TextCleaner
from emailClassifier.entity import DataTransformationConfig


class DataTransform:
      def __init__(self, config: DataTransformationConfig):
            self.config = config

      def get_pipeline(self):
            return Pipeline([
                  ('cleaner', TextCleaner()),
                  ('tfidf',   TfidfVectorizer(
                        max_features=1000,
                        ngram_range=(1,1)
                  ))
            ])

      def split_data(self) -> None:
            df = pd.read_csv(self.config.data_path)

            X_train, X_val, y_train, y_val = train_test_split(
                  df['text'], df['label'],
                  test_size=0.2,
                  random_state=42
            )

            tfidf_vectorizer = self.get_pipeline()


            X_train_matrix = tfidf_vectorizer.fit_transform(X_train)
            X_val_matrix = tfidf_vectorizer.transform(X_val)

            # Save the vectorizer to pkl file
            vectorizer_path = os.path.join(self.config.root_dir, "vectorizer.pkl")
            joblib.dump(tfidf_vectorizer, vectorizer_path)
            loger.info(f"Vectorizer saved to {vectorizer_path}")

            joblib.dump(X_train_matrix, os.path.join(self.config.root_dir, "x_train.pkl"))
            joblib.dump(X_val_matrix, os.path.join(self.config.root_dir, "x_val.pkl"))
            joblib.dump(y_train, os.path.join(self.config.root_dir, "y_train.pkl"))
            joblib.dump(y_val, os.path.join(self.config.root_dir, "y_val.pkl"))

            loger.info("Splitted data into train test split")