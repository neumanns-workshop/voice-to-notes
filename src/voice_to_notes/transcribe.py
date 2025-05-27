"""Core transcription functionality using OpenAI's Whisper."""

import os
from pathlib import Path
from typing import Optional, Union

import torch
import whisper
from pydub import AudioSegment
from tqdm import tqdm

# Supported audio formats
SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}

def _convert_to_wav(input_path: Union[str, Path]) -> Path:
    """Convert audio file to WAV format if necessary."""
    input_path = Path(input_path)
    if input_path.suffix.lower() == ".wav":
        return input_path
    
    if input_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported audio format: {input_path.suffix}. "
                       f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
    
    # Create a temporary WAV file
    wav_path = input_path.with_suffix(".wav")
    audio = AudioSegment.from_file(input_path)
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe(
    audio_path: Union[str, Path],
    model_size: str = "base",
    language: Optional[str] = None,
    device: Optional[str] = None,
) -> str:
    """
    Transcribe an audio file to text using OpenAI's Whisper.
    
    Args:
        audio_path: Path to the audio file
        model_size: Size of the Whisper model to use
            ("tiny", "base", "small", "medium", "large")
        language: Language code (e.g., "en", "es", "fr"). If None, auto-detected
        device: Device to use for inference ("cpu", "cuda", "mps")
    
    Returns:
        Transcribed text
    """
    # Set device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load model
    model = whisper.load_model(model_size, device=device)
    
    # Convert audio to WAV if necessary
    wav_path = _convert_to_wav(audio_path)
    
    try:
        # Transcribe
        result = model.transcribe(
            str(wav_path),
            language=language,
            verbose=False,
        )
        
        return result["text"]
    
    finally:
        # Clean up temporary WAV file if it was created
        if wav_path != audio_path:
            wav_path.unlink(missing_ok=True) 