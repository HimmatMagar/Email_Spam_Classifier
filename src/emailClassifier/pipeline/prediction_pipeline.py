import re
import emoji
import joblib
from pathlib import Path
from nltk.corpus import stopwords


class PredictionPipeline:
      def __init__(self):
            self.model = joblib.load(Path('artifact/build_model/model.pkl'))
            self.vectorizer = joblib.load(Path('artifact/data_transformation/vectorizer.pkl'))
      

      def transform_user_data(self, data):
            """
            Transform user data by cleaning and preprocessing text.
            
            Args:
                data (pd.DataFrame): DataFrame with 'text' column
                
            Returns:
                pd.DataFrame: DataFrame with cleaned text
            """
            df = data.copy()  # Work with a copy to avoid modifying original
            
            def emojis_to_text(text):
                  if isinstance(text, str):
                        emoji_text = emoji.demojize(text, language='en')
                        emoji_text = emoji_text.replace(":", " ")
                        emoji_text = emoji_text.replace("_", " ")
                        return re.sub(r'\s+', ' ', emoji_text).strip()
                  return text

            # Apply emoji conversion
            df['text'] = df['text'].apply(emojis_to_text)

            # Remove extra blank lines/newlines between sentences
            df['text'] = df['text'].str.replace(r'\n+', ' ', regex=True)

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

      def vectorize_data(self, data):
            """
            Convert text data to numerical vectors using pre-trained TF-IDF vectorizer.
            
            Args:
                data (pd.DataFrame): DataFrame with 'text' column containing cleaned text
                
            Returns:
                sparse matrix: Vectorized text data (numbers)
            """
            vectorized_matrix = self.vectorizer.transform(data['text'])
            
            return vectorized_matrix

      def predict_spam(self, data):
            prediction = self.model.predict(data)
            return int(prediction[0])