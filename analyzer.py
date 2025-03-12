import os
import textblob
from collections import Counter
import spacy

class Analyzer:
    def __init__(self, transcript_folder="logs/Text"):
        self.transcript_folder = transcript_folder
        self.nlp = spacy.load("en_core_web_sm")  # Load SpaCy for NLP

    def get_latest_transcription(self):
        """Finds the most recent transcription file and returns its text content."""
        files = [f for f in os.listdir(self.transcript_folder) if f.endswith(".txt")]
        if not files:
            return None  # No transcriptions yet

        # Get the latest file based on modified time
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.transcript_folder, f)))
        latest_path = os.path.join(self.transcript_folder, latest_file)

        with open(latest_path, "r", encoding="utf-8") as file:
            return file.read()

    def analyze_sentiment(self, text):
        """Performs sentiment analysis on the given text."""
        blob = textblob.TextBlob(text)
        sentiment_score = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)
        
        if sentiment_score > 0.1:
            sentiment = "Positive"
        elif sentiment_score < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {"score": sentiment_score, "label": sentiment}

    def extract_keywords(self, text, num_keywords=5):
        """Extracts key topics from the transcription using NLP."""
        doc = self.nlp(text)
        words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
        keyword_counts = Counter(words)
        top_keywords = keyword_counts.most_common(num_keywords)

        return [word for word, count in top_keywords]

# Usage Example
if __name__ == "__main__":
    analyzer = Analyzer()
    text = analyzer.get_latest_transcription()
    
    if text:
        print("Latest Transcription:", text)
        print("Sentiment Analysis:", analyzer.analyze_sentiment(text))
        print("Keyword Analysis:", analyzer.extract_keywords(text))
    else:
        print("No transcriptions available.")
