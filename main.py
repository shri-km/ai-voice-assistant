from json import load
from multiprocessing import Process, freeze_support
from msvcrt import kbhit, getwch
from time import sleep
import src.llm as llm
from src.tts import speak_text

stt_mode = 'api'
show_history = True

def load_model_config(model_key, task='stt'):
    with open(f"config/{task}_models.json", "r") as f:
        model_map = load(f)
    return model_map.get(model_key)


def tts_with_skip(text, voice_name=None, rate=180):
    #print("[DEBUG] Entered tts_with_skip()")
    p = Process(target=speak_text, args=(text, voice_name, rate))
    p.start()
    print("[Info] Press 's' to skip TTS, or wait for it to finish.")

    skip_triggered = False

    while p.is_alive():
        if kbhit():
            key = getwch()
            print(f"[DEBUG] Key pressed: {key}")
            if key.lower() == 's':
                print("[DEBUG] 's' detected, terminating TTS process.")
                p.terminate()
                skip_triggered = True
                break
        sleep(0.05)

    #print("[DEBUG] Waiting for TTS process to join...")
    p.join()
    #print("[DEBUG] TTS process joined.")

    if skip_triggered:
        print("[Info] TTS skipped by user.")
    else:
        print("[Info] TTS finished.")
    #print("[DEBUG] Exiting tts_with_skip()")

if __name__ == "__main__":

    if stt_mode == 'api':
        from src.audio import APIMicRecorder
        from google.genai.types import Part
        recognizer = APIMicRecorder()
    else:
        from src.stt import VoskMicRecognizer
        recognizer = VoskMicRecognizer(model_path=load_model_config('en-small'))

    freeze_support()

    print("Press [Enter] to start/stop mic. Press Ctrl+C to exit.")

    try:
        while True:
            input()  # Wait for Enter
            if recognizer.running:
                text = recognizer.stop_listening()
                if text:
                    # Feed into llm
                    if stt_mode == 'api':
                        res = llm.send_message([Part.from_bytes(data=text,mime_type="audio/wav")])
                    else:    
                        res = llm.send_message(text)
                    print(f'AI: {res.text}')
                    #TTS
                    tts_with_skip(res.text)
                else:
                    print('[Info] Your voice was not clear/audible. Please try again.')
                    continue
            else:
                recognizer.start_listening()

    except KeyboardInterrupt:
        
        print("[Info] Exiting.")
        recognizer.stop_listening()

        if show_history:
            print("\nChat history:")
            for message in llm.get_history():
                content = []
                for part in message.parts:
                    # If the part has text, use it
                    if getattr(part, "text", None):
                        content.append(part.text)
                    # If the part has file data, indicate it
                    elif getattr(part, "file_data", None):
                        # We can later customize this to show file name, type, etc.
                        file_name = getattr(part.file_data, "file_name", "file")
                        content.append(f"[file attached: {file_name}]")
                    # Can add more handlers for other types if needed (e.g., images, video, etc.)
                    else:
                        content.append("[non-text]")
                # Join all parts for this message and print
                print(f"{message.role}: {' '.join(content)}")