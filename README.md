# Voice to Notes

A Python tool for transcribing audio files to text using OpenAI's Whisper model.

## Features

- Transcribe various audio formats (MP3, WAV, M4A, FLAC, OGG)
- Support for multiple languages
- Local processing (no data sent to external servers)
- Progress tracking for long transcriptions
- Configurable model size for different accuracy/speed trade-offs

## Installation

This project uses `uv` for dependency management. Make sure you have Python 3.8+ installed.

1. Install `uv` if you haven't already:
```bash
pip install uv
```

2. Clone this repository:
```bash
git clone https://github.com/yourusername/voice-to-notes.git
cd voice-to-notes
```

3. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Usage

### As a Python Package

Basic usage:
```python
from voice_to_notes import transcribe

# Transcribe a single file
transcript = transcribe("path/to/your/audio.mp3")
print(transcript)

# Transcribe with specific model size
transcript = transcribe("path/to/your/audio.mp3", model_size="base")
```

### Using Scripts

The `scripts` directory contains ready-to-use scripts for common tasks:

- `transcribe_recording.py`: Transcribes an audio file and saves the output to the `transcripts` directory
  ```bash
  python scripts/transcribe_recording.py
  ```

Available model sizes:
- `tiny`: Fastest, least accurate
- `base`: Good balance of speed and accuracy
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

## Development

Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

## License

MIT License - see LICENSE file for details 