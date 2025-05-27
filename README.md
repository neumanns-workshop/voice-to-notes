# Voice to Notes

A Python application that transcribes voice recordings to text and processes them into structured notes using AI.

## Features

- Transcribe audio files to text using local Whisper model
- Process transcripts using Ollama (local LLM) to generate:
  - Key decisions and commitments
  - Current blockers and dependencies
  - Potential opportunities and ideas
  - Identified risks and concerns
  - Actionable items with priorities and due dates
- Generate consolidated daily to-do lists from multiple transcripts
- Save processed transcripts in structured JSON format

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- CUDA-capable GPU recommended for faster transcription

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice-to-notes.git
cd voice-to-notes
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Install and start Ollama:
- Follow instructions at https://ollama.ai/
- Pull the Gemma model:
```bash
ollama pull gemma3:27b
```

## Usage

1. Place your audio files in the `recordings` directory.

2. Transcribe the audio files:
```bash
python scripts/transcribe_recording.py
```

3. Process the transcripts:
```bash
python scripts/process_transcript.py
```

4. Generate daily to-do lists:
```bash
python scripts/generate_daily_todos.py
```

The processed transcripts will be saved in the `processed_transcripts` directory as JSON files, and daily to-do lists will be saved in the `daily_todos` directory.

## Project Structure

```
voice-to-notes/
├── recordings/           # Directory for audio files
├── transcripts/         # Directory for raw transcript text files
├── processed_transcripts/ # Directory for processed transcript JSON files
├── daily_todos/        # Directory for consolidated daily to-do lists
├── scripts/
│   ├── transcribe_recording.py  # Script for audio transcription
│   ├── process_transcript.py    # Script for transcript processing
│   └── generate_daily_todos.py  # Script for generating daily to-do lists
├── src/
│   └── voice_to_notes/
│       ├── __init__.py
│       ├── transcribe.py        # Core transcription functionality
│       └── models.py           # Pydantic models for structured output
├── pyproject.toml
└── README.md
```

## Output Format

### Processed Transcripts
Processed transcripts are saved as JSON files with the following structure:

```json
{
  "summary": {
    "key_decisions": ["Decision 1", "Decision 2"],
    "blockers": ["Blocker 1", "Blocker 2"],
    "opportunities": ["Opportunity 1", "Opportunity 2"],
    "risks": ["Risk 1", "Risk 2"]
  },
  "action_items": [
    {
      "description": "Action item description",
      "priority": 3,
      "due_date": "2024-03-20T10:00:00",
      "blockers": ["Dependency 1"],
      "status": "pending"
    }
  ],
  "metadata": {
    "processed_at": "2024-03-19T15:30:00",
    "model_used": "ollama",
    "version": "1.0"
  }
}
```

### Daily To-Do Lists
Daily to-do lists are saved as JSON files with the following structure:

```json
{
  "date": "2024-03-20",
  "action_items": [
    {
      "description": "Action item description",
      "priority": 3,
      "due_date": "2024-03-20T10:00:00",
      "blockers": ["Dependency 1"],
      "status": "pending"
    }
  ],
  "key_decisions": ["Decision 1", "Decision 2"],
  "blockers": ["Blocker 1", "Blocker 2"],
  "opportunities": ["Opportunity 1", "Opportunity 2"],
  "risks": ["Risk 1", "Risk 2"]
}
```

## License

MIT License

## Scripts

### 1. `transcribe_recording.py`
Transcribes audio recordings into text files.

### 2. `process_transcript.py`
Processes transcript text files to extract actionable insights using Ollama.

### 3. `generate_daily_todos.py`
Aggregates processed transcripts by date and generates consolidated daily to-do lists using Ollama. 