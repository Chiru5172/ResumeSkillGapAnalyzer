import re
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


def clean_text(text):
    # Lowercase
    text = text.lower()

    # Remove special characters & numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    return " ".join(filtered_words)
