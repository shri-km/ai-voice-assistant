from sounddevice import InputStream
from io import BytesIO
from wave import open
from sys import stderr
from threading import Thread
from queue import Queue

class APIMicRecorder:
    def __init__(self, samplerate=16000, channels=1):
        self.q = Queue()
        self.samplerate = samplerate
        self.channels = channels
        self.running = False
        self.frames = []
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[Mic Error] {status}", file=stderr)
        self.q.put(indata.copy())

    def start_listening(self):
        if self.running:
            print("[Info] Already running.")
            return
        self.running = True
        self.frames = []
        print("[Info] Starting mic. Speak now.")
        self.stream = InputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16',
                                     channels=self.channels, callback=self._callback)
        self.stream.start()
        Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        while self.running:
            data = self.q.get()
            self.frames.append(data)

    def stop_listening(self):
        if not self.running:
            print("[Info] Not currently running.")
            return b""
        self.running = False
        self.stream.stop()
        self.stream.close()
        print("[Info] Mic stopped.")

        # Combine all recorded frames
        from numpy import concatenate
        if not self.frames:
            print("[Info] No audio recorded.")
            return b""
        audio_np = concatenate(self.frames, axis=0)

        # Write to WAV in memory
        buf = BytesIO()
        with open(buf, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(self.samplerate)
            wf.writeframes(audio_np.tobytes())
        return buf.getvalue()
