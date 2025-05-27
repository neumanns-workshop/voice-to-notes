import json
import os
import logging
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from typing import Optional
from tqdm import tqdm

from voice_to_notes.models import ProcessedTranscript, TranscriptSummary, ActionItem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcript_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY = "ollama"  # Required by the OpenAI client, but often unused by Ollama
OLLAMA_MODEL = "gemma3:27b"  # Using Gemma 3 27B model for processing

def load_transcript(transcript_path: Path) -> str:
    """Load the transcript text from a file."""
    logger.info(f"Loading transcript from {transcript_path}")
    with open(transcript_path, 'r') as f:
        return f.read()

def process_with_ollama(client: OpenAI, transcript: str) -> ProcessedTranscript:
    """Process the transcript using Ollama to generate structured output."""
    
    # System prompt for the LLM
    system_prompt = """You are an AI assistant that processes transcripts to extract actionable insights. Your task is to:
1. Identify key decisions and commitments made
2. List current blockers and dependencies
3. Highlight potential opportunities and ideas
4. Note any risks or concerns
5. Extract specific action items with priorities and dependencies

Focus on extracting the most valuable insights that will help move things forward. Be concise but specific."""

    # User prompt with the transcript
    user_prompt = f"""Please process this transcript and provide structured output:

{transcript}"""

    try:
        logger.info("Sending transcript to Ollama for processing")
        # Call Ollama API with Pydantic parsing
        completion = client.beta.chat.completions.parse(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ProcessedTranscript
        )

        # Get the parsed response
        return completion.choices[0].message.parsed

    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
        raise

def save_processed_transcript(processed: ProcessedTranscript, output_path: Path):
    """Save the processed transcript to a JSON file."""
    logger.info(f"Saving processed transcript to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(processed.model_dump(), f, indent=2, default=str)

def main():
    # Initialize OpenAI client for Ollama
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key=OLLAMA_API_KEY,
    )

    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    
    # Define paths
    transcripts_dir = project_root / "transcripts"
    output_dir = project_root / "processed_transcripts"
    
    # Get all transcript files
    transcript_files = list(transcripts_dir.glob("*.txt"))
    logger.info(f"Found {len(transcript_files)} transcript files to process")
    
    # Process each transcript file with progress bar
    for transcript_file in tqdm(transcript_files, desc="Processing transcripts"):
        logger.info(f"Processing {transcript_file.name}")
        
        try:
            # Load transcript
            transcript_text = load_transcript(transcript_file)
            
            # Process with Ollama
            processed = process_with_ollama(client, transcript_text)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"{transcript_file.stem}_processed_{timestamp}.json"
            
            # Save processed transcript
            save_processed_transcript(processed, output_file)
            logger.info(f"Successfully processed {transcript_file.name}")
            
        except Exception as e:
            logger.error(f"Failed to process {transcript_file.name}: {e}")
            continue

if __name__ == "__main__":
    main() 