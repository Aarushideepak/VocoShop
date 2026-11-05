
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient

load_dotenv()

client = GnaniTTSClient()


def speak(text):
    audio = client.synthesize(
        text,
        voice="Kaveri",
        model="timbre-v2.5",
        language="kn-IN"
    )

    with open("response.wav", "wb") as file:
        file.write(audio)

    data, samplerate = sf.read("response.wav")

    sd.play(data, samplerate, device=3)
    sd.wait()

    print("Audio playback completed")
