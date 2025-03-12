from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    return classifier(text)

print(analyze_sentiment("I loved that I studied today"))