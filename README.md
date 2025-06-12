# Voice AI Assistant

A Python-based speech-to-speech assistant that listens to your voice, processes your input via Google’s Gemini API, and speaks responses aloud. It uses Vosk (or Gemini) for local STT, a configurable Gemini chat session for LLM, and pyttsx3 for TTS with skip-on-keypress support.

## Features

- **Dynamic STT model selection** via `config/stt_models.json`
- **Push-button mic control** (press Enter to start/stop listening)  
- **Full conversation history** printed on exit (if needed)
- **Skip TTS playback** by pressing “s” during speech  
- **Clean module separation**  
  - `src/stt.py` for speech recognition  
  - `src/llm.py` for LLM integration  
  - `src/tts.py` for text-to-speech

## Getting Started

### Prerequisites

- Python 3.11+  
- [UV package manager](https://github.com/astral-sh/uv)  
- A Gemini API key stored in a `.env` file as `GEMINI_API_KEY` (should be inside `src` folder, see [Project Structure](#project-structure))

### Installation

Run `pip install uv` if you don't have uv installed.

After cloning the repo, create a virtual environment using `uv venv`, and then activate using `source .venv/bin/activate` for Mac and `.venv\Scripts\activate.bat` for Windows (cmd), and then use `uv sync` to install all the dependencies.

Run the program using `uv run ./main.py`.

### Usage

- Change show_history (to show full conversation history at the end) in main.py if needed.
- Change stt_mode in main.py if needed ('api' to send audio directly to Gemini or 'local' to use local stt models)
- Press **Enter** to start or stop recording.
- After stopping, your speech is sent to Gemini and the AI’s reply is printed and spoken.
- During TTS playback, press **s** to skip.
- Press **Ctrl+C** to exit and if needed, display the full chat history.

### Project Structure

``` python
voice-ai-assistant/
├── .venv/
├── config/
│ └── stt_models.json # STT model mappings
├── models/
│ └── stt/ # Vosk model directories
├── src/
| ├── .env # GEMINI_API_KEY
│ ├── init.py
│ ├── stt.py # VoskMicRecognizer
│ ├── audio.py # Record voice and return byte data
│ ├── llm.py # Gemini chat wrapper
│ └── tts.py # TextToSpeech with skip support
├── main.py
├── pyproject.toml
└── README.md
```

## Future Improvements

- **STT model upgrades**: Feeding audio to Gemini directly works good, but may run into usage limits. Using local models solves this. Vosk can be swapped with Whisper, Coqui or SpeechBrain for higher accuracy.
- **TTS alternatives**: Integrate Mimic 3 or Coqui TTS for more natural voices.
- **Streaming LLM responses**: Use Gemini’s streaming API for real-time text playback.
- **Avatar lip-sync**: Add NVIDIA Audio2Face, Wav2Lip, or PyToon to animate a visual avatar.  
- **GUI or web UI**: Build a frontend with PyQt, Streamlit, or Flask for user-friendly interaction.  
- **Packaging & CI**: Containerize with Docker, add GitHub Actions for testing and releases.  
- **Multi-language support**: Extend STT/TTS for languages beyond English.
