"""Speech-to-Text functionality using Whisper"""

import io
from typing import Optional
from loguru import logger


class SpeechToText:
    """Convert speech to text using OpenAI Whisper"""

    def __init__(self, model: str = "base", language: str = "fr"):
        """
        Initialize STT

        Args:
            model: Whisper model size (tiny, base, small, medium, large)
            language: Target language (fr, ar, en)
        """
        self.model_name = model
        self.language = language
        self._model = None

    def _load_model(self):
        """Lazy load Whisper model"""
        if self._model is None:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name)
                logger.info(f"Whisper model loaded: {self.model_name}")
            except ImportError:
                logger.error("Whisper not installed. Install with: pip install openai-whisper")
                raise

    async def transcribe_audio(
        self, audio_data: bytes, language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio to text

        Args:
            audio_data: Audio file bytes
            language: Override language

        Returns:
            dict with 'text', 'language', 'segments'
        """
        try:
            self._load_model()

            # Save audio to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            # Transcribe
            result = self._model.transcribe(
                temp_path,
                language=language or self.language,
                fp16=False,
            )

            # Clean up
            import os
            os.unlink(temp_path)

            return {
                "text": result["text"],
                "language": result.get("language", self.language),
                "segments": result.get("segments", []),
                "success": True,
            }

        except Exception as e:
            logger.error(f"Error in transcription: {str(e)}")
            return {
                "text": "",
                "language": self.language,
                "error": str(e),
                "success": False,
            }

    async def transcribe_file(self, file_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe audio file

        Args:
            file_path: Path to audio file
            language: Override language

        Returns:
            dict with transcription results
        """
        try:
            with open(file_path, "rb") as f:
                audio_data = f.read()
            return await self.transcribe_audio(audio_data, language)
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return {"text": "", "error": str(e), "success": False}
