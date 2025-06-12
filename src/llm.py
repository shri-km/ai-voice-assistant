from google.genai import Client, types
from dotenv import load_dotenv
from os import getenv

load_dotenv()

system_instruction = """
You are a helpful AI assistant. You are being used as an llm in the middle of a speech to speech AI assistant. 
Give answers precisely and to the point.
If the input is only text, it would have been transcribed by an STT model.
It would have a high error rate as it is run locally. Take that into account and try to figure out what
that user may be trying to ask you and give answers accordingly.
"""

client = Client(api_key=getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-2.0-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.5,
        max_output_tokens=150,
    )
    )

def send_message(text):
    return chat.send_message(text)

def get_history():
    return chat.get_history()