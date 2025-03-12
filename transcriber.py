import os
import whisper
from datetime import datetime

TRANSCRIPT_FOLDER = "logs/Text"

class Transcriber:
    def __init__(self, audio_folder="logs/audio/", model_size="base", transcript_folder=TRANSCRIPT_FOLDER):
        """Initializes the Whisper model."""
        self.audio_folder = audio_folder
        self.transcript_folder = transcript_folder
        self.model = whisper.load_model(model_size, device="cpu")  # Load Whisper model

    def get_latest_audio(self):
        """Finds the latest recorded audio file."""
        files = [f for f in os.listdir(self.audio_folder) if f.endswith('.wav')]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.audio_folder, f)))
        return os.path.join(self.audio_folder, latest_file)

    def transcribe_audio(self, audio_path):
        """Transcribes audio using Whisper AI."""
        result = self.model.transcribe(audio_path)
        return result["text"]

    def save_transcription(self, text, output_folder="logs/Text/"):
        """Saves the transcribed text to a file."""
        filename = f"{output_folder}transcription_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Transcription saved: {filename}")

    def process_latest_audio(self):
        """Finds the latest audio file, transcribes it, and saves the text."""
        audio_path = self.get_latest_audio()
        if not audio_path:
            print("No audio files found!")
            return

        print(f"Processing: {audio_path}")
        transcription = self.transcribe_audio(audio_path)
        self.save_transcription(transcription)

if __name__ == "__main__":
    transcriber = Transcriber()
    transcriber.process_latest_audio()
