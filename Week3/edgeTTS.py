import asyncio
import edge_tts
from edge_tts import VoicesManager


def speak(text: str, output_file: str) -> None:
    """Speak the given text and save it to the output file."""

    async def speak_async():
        voices = await VoicesManager.create()
        # voice = voices.find(Gender="Male", Language="en")
        # print(voice)

        communicate = edge_tts.Communicate(text, "en-US-BrianNeural")
        await communicate.save(output_file)

    asyncio.run(speak_async())
