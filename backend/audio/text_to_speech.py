"""Text-to-Speech functionality"""

from typing import Optional
from loguru import logger


class TextToSpeech:
    """Convert text to speech using gTTS"""

    def __init__(self, language: str = "fr"):
        """
        Initialize TTS

        Args:
            language: Target language (fr, ar, en)
        """
        self.language = language

    async def synthesize(
        self, text: str, language: Optional[str] = None, slow: bool = False
    ) -> bytes:
        """
        Synthesize text to speech

        Args:
            text: Text to synthesize
            language: Override language
            slow: Speak slowly

        Returns:
            Audio data as bytes
        """
        try:
            from gtts import gTTS
            import io

            lang = language or self.language

            # Create TTS object
            tts = gTTS(text=text, lang=lang, slow=slow)

            # Save to bytes
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            return audio_fp.read()

        except Exception as e:
            logger.error(f"Error in TTS: {str(e)}")
            return b""

    async def synthesize_to_file(
        self, text: str, output_path: str, language: Optional[str] = None
    ) -> bool:
        """
        Synthesize and save to file

        Args:
            text: Text to synthesize
            output_path: Output file path
            language: Override language

        Returns:
            Success status
        """
        try:
            audio_data = await self.synthesize(text, language)
            if audio_data:
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                return True
            return False
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return False
