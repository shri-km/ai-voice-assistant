import sounddevice as sd
from sys import stderr
from json import loads
from threading import Thread
from queue import Queue
from vosk import Model, KaldiRecognizer

class VoskMicRecognizer:
    def __init__(self, model_path="models/stt/vosk-small-en", samplerate=16000):
        self.q = Queue()
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, samplerate)
        self.running = False
        self.samplerate = samplerate
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[Mic Error] {status}", file=stderr)
        self.q.put(bytes(indata))

    def start_listening(self):
        if self.running:
            print("[Info] Already running.")
            return
        self.running = True
        print("[Info] Starting mic. Speak now.")
        self.stream = sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16',
                                        channels=1, callback=self._callback)
        self.stream.start()
        Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        while self.running:
            data = self.q.get()
            if self.recognizer.AcceptWaveform(data):
                result = loads(self.recognizer.Result())
                text = result.get("text", "").strip()
        # if text:
        #     print("You said:", text)

            # Print partial results if needed, optional

            # else:
            #     partial = loads(self.recognizer.PartialResult())
            #     partial_text = partial.get("partial", "").strip()
            #     if partial_text:
            #         print(f"[Partial] {partial_text}", end='\r')

    def stop_listening(self):
        if not self.running:
            print("[Info] Not currently running.")
            return ""
        self.running = False
        self.stream.stop()
        self.stream.close()
        # Flush any remaining audio left in buffer
        final_result = loads(self.recognizer.FinalResult())
        text = final_result.get("text", "").strip()
        if text:
            print("[Info] You said:", text)
        print("[Info] Mic stopped.")
        return text