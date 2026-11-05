
import time
import sounddevice as sd
import soundfile as sf

from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.stt.exceptions import APIError
from assistant import process_command

load_dotenv()

client = GnaniSTTClient()

print("===== KIRANAVOICE =====")
print("Speak your command. Say 'exit' to stop.")

while True:
    print("\nListening... Speak now!")

    audio = sd.rec(
        int(5 * 16000),
        samplerate=16000,
        channels=1,
        device=1
    )

    sd.wait()

    sf.write("recorded_command.wav", audio, 16000)

    print("Processing your speech...")

    result = None

    for attempt in range(3):
        try:
            result = client.transcribe(
                "recorded_command.wav",
                language_code="en-IN"
            )
            break

        except APIError as e:
            print(f"Gnani API error: {e}")

            if getattr(e, "status_code", None) != 504:
                raise

            if attempt == 2:
                print("Gnani server is unavailable. Please try again.")
            else:
                print("Retrying in 3 seconds...")
                time.sleep(3)

    if result is None:
        continue

    transcript = result["transcript"].strip()
    if not transcript:
        print("No speech detected. Please try again.")
        continue
    print("You said:", transcript)

    if "exit" in transcript.lower():
        print("KiranaVoice: Goodbye!")
        break

    process_command(transcript)
