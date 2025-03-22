import sounddevice as sd
import wave
import time
import os
from datetime import datetime
from notifier import TEST_INTERVAL
from transcriber import Transcriber  # Import transcriber
from analyzer import Analyzer

TEST_DURATION = 30

class Recorder:
    def __init__(self, duration=30, freq=44100, save_dir="logs"):
        self.duration = duration  # Recording duration in seconds
        self.freq = freq  # Sampling frequency
        self.running = True  # Allows stopping later
        self.save_dir = save_dir
        self.transcriber = Transcriber()
        self.analyzer = Analyzer()

        # Ensure logs directory exists
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def record_audio(self):
        """Records audio and saves it with a timestamp."""
        print("🔴 Recording started...")
        recording = sd.rec(int(self.duration * self.freq), samplerate=self.freq, channels=2, dtype='int16')
        sd.wait()

        # Save with timestamp
        filename = os.path.join(self.save_dir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".wav")
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.freq)
            wf.writeframes(recording.tobytes())

        print(f"✅ Recording saved: {filename}")

    def start(self, record_event, ai_event):
        """Runs the recorder in a loop, capturing audio when the notifier goes off"""
        try:
            while self.running:
                record_event.wait()  # Wait for notifier signal
                
                self.record_audio()  # Record audio
                self.transcriber.process_latest_audio()  # Transcribe it
                
                time.sleep(2)  # 🕒 Allow time for transcription to be saved
                
                self.analyzer.analyze_latest_transcription()  # ✅ Analyze text
                
                time.sleep(1)  # 🕒 Allow processing before intervention
                
                ai_event.set()  # ✅ Signal AI intervention
                
                record_event.clear()  # Reset event for the next cycle
        except KeyboardInterrupt:
            print("\n🛑 Recording stopped by user.")

if __name__ == "__main__":
    recorder = Recorder(duration=TEST_DURATION)
    recorder.start(interval=TEST_INTERVAL)
