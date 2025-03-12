from analyzer import analyze_sentiment, extract_keywords

# Example transcribed text
text_sample = "I am happy that I studied, but am so sleepy."

# Analyze text
sentiment_result = analyze_sentiment(text_sample)
keyword_result = extract_keywords(text_sample)

# Print results
print("Sentiment Analysis:", sentiment_result)
print("Keyword Analysis:", keyword_result)