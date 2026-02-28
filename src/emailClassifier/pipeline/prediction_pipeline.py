import re
import emoji
import joblib
from pathlib import Path
from nltk.corpus import stopwords


class PredictionPipeline:
      def __init__(self):
            self.model = joblib.load(Path('artifact/build_model/model.pkl'))
      

      def transform_user_data(self, data):
            def emojis_to_text(text):
                  if isinstance(text, str):
                        emoji_text = emoji.demojize(text, language='en')
                        emoji_text = emoji_text.replace(":", " ")
                        emoji_text = emoji_text.replace("_", " ")
                        return re.sub(r'\s+', ' ', emoji_text).strip()
                  return text

            # Apply emoji conversion
            data['text'] = data['text'].apply(emojis_to_text)

            # Remove punctuation
            data['text'] = data['text'].str.replace(r'[^\w\s]', '', regex=True)

            # Remove numbers
            data['text'] = data['text'].str.replace(r'\d+', '', regex=True)

            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            data['text'] = data['text'].apply(
                  lambda x: ' '.join(word for word in x.split() if word.lower() not in stop_words)
            )

            return data


      def predict_spam(self, data):
            prediction = self.model.predict(data)
            return prediction