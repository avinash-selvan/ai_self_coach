import sounddevice as sd
import wave
import time
from datetime import datetime

# Sampling rate 
SAMPLE_RATE = 44100
DURATION = 30
CHANNELS = 1

def record_audio():
    print("🎤Recording for 30 seconds")

    audio_data = sd.rec(
        int(DURATION*SAMPLE_RATE),
        samplerate= SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16'
    )

    sd.wait()

    print("✅ Recording complete")

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    
    print(f"💾 Audio saved as {filename}")

if __name__ == "__main__":
    record_audio()