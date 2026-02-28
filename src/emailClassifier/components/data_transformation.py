import os
import re
import emoji
import joblib
import pandas as pd
from nltk.corpus import stopwords
from src.emailClassifier import loger
from src.emailClassifier.utils import *
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from src.emailClassifier.entity import DataTransformationConfig


class DataTransform:
      def __init__(self, config: DataTransformationConfig):
            self.config = config

      
      def transform_data(self):
            # Load dataset
            df = pd.read_csv(self.config.data_path)

            # Convert emojis to text
            def emojis_to_text(text):
                  if isinstance(text, str):
                        emoji_text = emoji.demojize(text, language='en')
                        emoji_text = emoji_text.replace(":", " ")
                        emoji_text = emoji_text.replace("_", " ")
                        return re.sub(r'\s+', ' ', emoji_text).strip()
                  return text

            # Apply emoji conversion
            df['text'] = df['text'].apply(emojis_to_text)

            # Remove punctuation
            df['text'] = df['text'].str.replace(r'[^\w\s]', '', regex=True)

            # Remove numbers
            df['text'] = df['text'].str.replace(r'\d+', '', regex=True)

            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            df['text'] = df['text'].apply(
                  lambda x: ' '.join(word for word in x.split() if word.lower() not in stop_words)
            )

            return df


      def word_to_matrix(self):
            df = self.transform_data()
            tfidf_vectorizer = TfidfVectorizer(
                  max_features=1000,
                  ngram_range=(1,1)
            )

            tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])
            y = df['label']

            return tfidf_matrix, y
      

      def split_data(self):
            tfidf_matrix, y = self.word_to_matrix()
            x_train, x_val, y_train, y_val = train_test_split(tfidf_matrix, y, test_size=0.3)

            joblib.dump(x_train, os.path.join(self.config.root_dir, "x_train.pkl"))
            joblib.dump(x_val, os.path.join(self.config.root_dir, "x_val.pkl"))
            joblib.dump(y_train, os.path.join(self.config.root_dir, "y_train.pkl"))
            joblib.dump(y_val, os.path.join(self.config.root_dir, "y_val.pkl"))

            loger.info("Splitted data into train test split")
      