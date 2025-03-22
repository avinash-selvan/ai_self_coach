import os
import textblob
from collections import Counter
import spacy
import json  # For saving data in a structured way

class Analyzer:
    def __init__(self, transcript_folder="logs/Text", analysis_folder="logs/Analysis"):
        self.transcript_folder = transcript_folder
        self.analysis_folder = analysis_folder
        self.nlp = spacy.load("en_core_web_sm")  # Load SpaCy for NLP

        # Ensure the analysis folder exists
        if not os.path.exists(self.analysis_folder):
            os.makedirs(self.analysis_folder)

    def get_latest_transcription(self):
        """Finds the most recent transcription file and returns its text content."""
        files = [f for f in os.listdir(self.transcript_folder) if f.endswith(".txt")]
        if not files:
            return None  # No transcriptions yet

        # Get the latest file based on modified time
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.transcript_folder, f)))
        latest_path = os.path.join(self.transcript_folder, latest_file)

        with open(latest_path, "r", encoding="utf-8") as file:
            return latest_file, file.read()  # Return filename along with content

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

    def save_analysis(self):
        """Save the sentiment and keyword analysis of the latest transcription to a file."""
        transcription_filename, text = self.get_latest_transcription()
        
        if text:
            # Analyze the transcription
            sentiment_analysis = self.analyze_sentiment(text)
            keyword_analysis = self.extract_keywords(text)
            
            # Create the analysis data structure
            analysis_data = {
                "transcription_filename": transcription_filename,
                "sentiment": sentiment_analysis,
                "keywords": keyword_analysis
            }
            
            # Generate the filename for the analysis file (use transcription filename as base)
            base_filename = os.path.splitext(transcription_filename)[0]  # Remove the ".txt" extension
            analysis_filename = f"{base_filename}_analysis.json"  # Save as JSON for structured data

            # Path to save the analysis
            analysis_filepath = os.path.join(self.analysis_folder, analysis_filename)
            
            # Save the analysis as a JSON file
            with open(analysis_filepath, "w", encoding="utf-8") as analysis_file:
                json.dump(analysis_data, analysis_file, ensure_ascii=False, indent=4)

            print(f"Analysis saved to: {analysis_filepath}")
        else:
            print("No transcription available to analyze.")

# Usage Example
if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.save_analysis()  # This will analyze the latest transcription and save the results
