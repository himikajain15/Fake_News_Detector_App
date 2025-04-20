import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
    return " ".join(tokens)

if __name__ == "__main__":
    sample_text = "This is a Fake News Article! Beware of misleading information."
    print(preprocess_text(sample_text))
