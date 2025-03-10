import sounddevice as sd
import wave
from datetime import datetime

class VoiceRecorder:
    def __init__(self, duration=30, sample_rate=44100, channels=1):
        self.duration = duration
        self.sample_rate = sample_rate
        self.channels = channels
    
    def record(self):
        print("🎤 Recording for", self.duration, "seconds...")

        # Record Audio
        audio_data = sd.rec(int(self.duration * self.sample_rate), 
                            samplerate=self.sample_rate, 
                            channels=self.channels, 
                            dtype='int16')

        sd.wait()
        print("✅ Recording finished!")

        # Save to file
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        self.save_audio(filename, audio_data)

    def save_audio(self, filename, audio_data):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 2 bytes per sample (16-bit PCM)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

        print(f"💾 Audio saved as {filename}")

if __name__=="__main__":
    recorder = VoiceRecorder()
    recorder.record()
