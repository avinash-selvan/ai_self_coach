import sounddevice as sd
import soundfile as sf

# Load and play the recorded audio
filename = "2025-03-11_11-19-10.wav"  # Change if using a different file name
data, samplerate = sf.read(filename)
sd.play(data, samplerate)
sd.wait()