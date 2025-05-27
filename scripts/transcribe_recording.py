#!/usr/bin/env python3
"""Script to transcribe audio files and save the output."""

import logging
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

from voice_to_notes import transcribe

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    
    # Define paths
    recordings_dir = project_root / "recordings"
    transcripts_dir = project_root / "transcripts"
    transcripts_dir.mkdir(exist_ok=True)
    
    # Get all audio files
    audio_files = list(recordings_dir.glob("*.mp3"))
    logger.info(f"Found {len(audio_files)} audio files to transcribe")
    
    # Process each audio file with progress bar
    for audio_file in tqdm(audio_files, desc="Transcribing audio files"):
        logger.info(f"Transcribing {audio_file.name}")
        
        try:
            # Use the recording's date identifier for the output filename
            output_file = transcripts_dir / f"transcript_{audio_file.stem}.txt"
            
            # Transcribe the audio file
            transcript = transcribe(
                audio_file,
                model_size="base",  # Using base model for good balance of speed/accuracy
            )
            
            # Save the transcript
            output_file.write_text(transcript)
            logger.info(f"Transcript saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to transcribe {audio_file.name}: {e}")
            continue

if __name__ == "__main__":
    main() 