import time
from plyer import notification
from analyzer import Analyzer

class AIIntervention:
    def __init__(self):  # Check every hour
        self.analyzer = Analyzer()

    def send_notification(self, message):
        """Sends a system notification."""
        notification.notify(
            title="AI Coach",
            message=message,
            timeout=5,
            app_name="AI_Self_Improvement"
        )

    def analyze_and_intervene(self):
        """Analyzes the latest transcription and gives real-time advice."""
        text = self.analyzer.get_latest_transcription()
        if not text:
            return  # No transcription available

        sentiment_result = self.analyzer.analyze_sentiment(text)
        keywords = self.analyzer.extract_keywords(text)

        # AI Interventions Based on Sentiment
        if sentiment_result["label"] == "Negative":
            self.send_notification("You seem frustrated. Take a deep breath. You’re making progress. 💪")
        elif sentiment_result["label"] == "Positive":
            self.send_notification("Great energy today! Keep up the momentum! 🚀")

        # AI Interventions Based on Keywords
        if "distraction" in keywords or "youtube" in keywords:
            self.send_notification("You've mentioned distractions. Want a Pomodoro session? ⏳")
        if "stress" in keywords or "tired" in keywords:
            self.send_notification("You seem stressed. Try a 5-minute break. ☕")

    def run(self, ai_event):
        """Continuously waits for new transcriptions and intervenes if needed."""
        while True:
            ai_event.wait()  # Wait until a new transcription is ready
            self.analyze_and_intervene()
            ai_event.clear()  # Reset event for the next cycle

# Run AI Interventions
if __name__ == "__main__":
    ai_coach = AIIntervention()
    ai_coach.run()
