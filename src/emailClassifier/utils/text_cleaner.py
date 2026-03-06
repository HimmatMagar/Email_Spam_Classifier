import re
import emoji
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin


class TextCleaner(BaseEstimator, TransformerMixin):
    """
    A text cleaning transformer that handles various text preprocessing tasks.
    
    Cleaning steps:
    1. Convert emojis to text representation
    2. Remove/normalize whitespace and newlines
    3. Convert to lowercase
    4. Remove URLs and email addresses
    5. Remove special characters and punctuation
    6. Remove numbers
    7. Remove extra whitespace
    8. Remove English stopwords
    """
    
    def __init__(self, remove_stopwords=True, remove_numbers=True, lowercase=True):
        """
        Initialize TextCleaner.
        
        Args:
            remove_stopwords (bool): Whether to remove English stopwords
            remove_numbers (bool): Whether to remove numeric characters
            lowercase (bool): Whether to convert text to lowercase
        """
        self.remove_stopwords = remove_stopwords
        self.remove_numbers = remove_numbers
        self.lowercase = lowercase
        self.stop_words = set(stopwords.words('english'))
    
    def fit(self, X, y=None):
        """Fit method (no fitting required for this transformer)."""
        return self
    
    def transform(self, X, y=None):
        """
        Transform text data by cleaning it.
        
        Args:
            X: Pandas Series or list of text strings
            y: Ignored, present for pipeline compatibility
            
        Returns:
            Cleaned text data in same format as input
        """
        def clean_text(text):
            """Clean individual text string."""
            # Handle non-string inputs
            if not isinstance(text, str):
                return ""
            
            # Remove leading/trailing whitespace
            text = text.strip()
            
            if not text:
                return ""
            
            # Convert to lowercase
            if self.lowercase:
                text = text.lower()
            
            # Convert emojis to text
            text = emoji.demojize(text, language='en')
            text = text.replace(":", " ").replace("_", " ")
            
            # Remove URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            
            # Remove email addresses
            text = re.sub(r'\S+@\S+', '', text)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove newlines and carriage returns
            text = re.sub(r'[\r\n]+', ' ', text)
            
            # Remove special characters and punctuation, keep only alphanumeric and spaces
            text = re.sub(r'[^\w\s]', '', text)
            
            # Remove numbers if specified
            if self.remove_numbers:
                text = re.sub(r'\d+', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove stopwords if specified
            if self.remove_stopwords:
                words = text.split()
                words = [w for w in words if w.lower() not in self.stop_words]
                text = ' '.join(words)
            
            return text.strip()
        
        # Handle both pandas Series and list inputs
        if hasattr(X, 'apply'):
            return X.apply(clean_text)
        else:
            return [clean_text(text) for text in X]