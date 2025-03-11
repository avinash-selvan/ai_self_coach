import sounddevice as sd
import wave
import time
import os
from datetime import datetime
from notifier import TEST_INTERVAL
from transcriber import Transcriber  # Import transcriber

TEST_DURATION = 10

class Recorder:
    def __init__(self, duration=30, freq=44100, save_dir="logs"):
        self.duration = duration  # Recording duration in seconds
        self.freq = freq  # Sampling frequency
        self.running = True  # Allows stopping later
        self.save_dir = save_dir
        self.transcriber = Transcriber()

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

    def start(self, event, interval=3600):
        """Runs the recorder in a loop, capturing audio at set intervals."""
        print(f"🎤 Recorder started, capturing every {interval} seconds.")
        try:
            while self.running:
                event.wait()
                self.record_audio()
                self.transcriber.process_latest_audio()
                # print(f"⏳ Sleeping for {interval} seconds before next recording...")
                # time.sleep(interval)
                event.clear()
        except KeyboardInterrupt:
            print("\n🛑 Recording stopped by user.")

    def stop(self):
        """Stops recording loop."""
        self.running = False

if __name__ == "__main__":
    recorder = Recorder(duration=TEST_DURATION)
    recorder.start(interval=TEST_INTERVAL)
