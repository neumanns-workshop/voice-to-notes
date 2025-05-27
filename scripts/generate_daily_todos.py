import json
import os
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict
from openai import OpenAI
from tqdm import tqdm

from voice_to_notes.models import ProcessedTranscript, ActionItem, DailyTodoList

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_todos.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY = "ollama"
OLLAMA_MODEL = "gemma3:27b"

def load_processed_transcripts(processed_dir: Path) -> List[ProcessedTranscript]:
    """Load all processed transcripts from the directory."""
    processed_files = list(processed_dir.glob("*.json"))
    transcripts = []
    
    for file in processed_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                transcripts.append(ProcessedTranscript.model_validate(data))
        except Exception as e:
            logger.error(f"Error loading {file}: {e}")
            continue
    
    return transcripts

def group_transcripts_by_date(transcripts: List[ProcessedTranscript], processed_dir: Path) -> Dict[str, List[ProcessedTranscript]]:
    """Group transcripts by their date based on the filename."""
    grouped = defaultdict(list)
    
    # Create a mapping of processed files to their original transcript files
    processed_files = {f.name: f for f in processed_dir.glob("*.json")}
    
    for transcript in transcripts:
        # Find the corresponding processed file
        for filename, file_path in processed_files.items():
            if filename.startswith("transcript_"):
                # Extract date from filename (format: transcript_YYMMDD_HHMM)
                try:
                    date_str = filename.split("_")[1]  # Get YYMMDD part
                    year = "20" + date_str[:2]  # Convert YY to YYYY
                    month = date_str[2:4]
                    day = date_str[4:6]
                    date = f"{year}-{month}-{day}"
                    grouped[date].append(transcript)
                    break
                except (IndexError, ValueError) as e:
                    logger.warning(f"Could not parse date from filename {filename}: {e}")
                    continue
    
    return dict(grouped)

def generate_daily_todo(client: OpenAI, transcripts: List[ProcessedTranscript], date: str) -> DailyTodoList:
    """Generate a consolidated to-do list for a specific day using Ollama."""
    
    # Prepare input for the LLM
    input_data = {
        "date": date,
        "transcripts": [
            {
                "summary": t.summary.model_dump(mode='json'),
                "action_items": [item.model_dump(mode='json') for item in t.action_items]
            }
            for t in transcripts
        ]
    }
    
    system_prompt = """You are an AI assistant that consolidates multiple transcripts into a single, organized daily to-do list. Your task is to:
1. Combine and deduplicate action items
2. Prioritize items based on their importance and dependencies
3. Consolidate key decisions, blockers, opportunities, and risks
4. Ensure the output is clear and actionable

Focus on creating a coherent and practical daily plan that captures all important items."""

    user_prompt = f"""Please consolidate these transcripts into a daily to-do list for {date}:

{json.dumps(input_data, indent=2)}"""

    try:
        logger.info(f"Generating daily to-do list for {date}")
        completion = client.beta.chat.completions.parse(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=DailyTodoList
        )
        
        return completion.choices[0].message.parsed

    except Exception as e:
        logger.error(f"Error generating daily to-do list: {e}")
        raise

def save_daily_todo(todo_list: DailyTodoList, output_dir: Path):
    """Save the daily to-do list to a JSON file."""
    output_path = output_dir / f"daily_todo_{todo_list.date}.json"
    logger.info(f"Saving daily to-do list to {output_path}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(todo_list.model_dump(), f, indent=2, default=str)

def main():
    # Initialize OpenAI client for Ollama
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key=OLLAMA_API_KEY,
    )

    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    
    # Define paths
    processed_dir = project_root / "processed_transcripts"
    output_dir = project_root / "daily_todos"
    
    # Load and group transcripts
    transcripts = load_processed_transcripts(processed_dir)
    grouped_transcripts = group_transcripts_by_date(transcripts, processed_dir)
    
    logger.info(f"Found transcripts for {len(grouped_transcripts)} different dates")
    
    # Generate daily to-do lists
    for date, date_transcripts in tqdm(grouped_transcripts.items(), desc="Generating daily to-do lists"):
        try:
            todo_list = generate_daily_todo(client, date_transcripts, date)
            save_daily_todo(todo_list, output_dir)
            logger.info(f"Successfully generated to-do list for {date}")
        except Exception as e:
            logger.error(f"Failed to generate to-do list for {date}: {e}")
            continue

if __name__ == "__main__":
    main() 