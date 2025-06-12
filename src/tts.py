import pyttsx3

def speak_text(text, voice_name=None, rate=180):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    if voice_name:
        voices = engine.getProperty('voices')
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"[TTS] Using voice: {voice.name}")
                break
    print("[TTS] Speaking..")
    engine.say(text)
    engine.runAndWait()
    print("[TTS] Done speaking.")