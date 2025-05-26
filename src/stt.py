import json
from vosk import Model, KaldiRecognizer
from typing import Optional, Generator
from contextlib import contextmanager


class STT:
    """Speech-to-Text engine using VOSK model.

    Example:
        >>> with STT() as stt:
        ...     if stt.recognizer.AcceptWaveform(audio_data):
        ...         result = json.loads(stt.recognizer.Result())
        ...         print(f"Transcribed: {result['text']}")
    """
    def __init__(self, model_path):
        """Initialize the STT engine with the specified model."""
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass

    def start(self):
        """Start the audio stream."""
        if self.stream is None:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=3072
            )
            self.stream.start_stream()
            
    def stop(self):
        """Stop and cleanup resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.audio:
            self.audio.terminate()
            
    def transcribe_chunk(self) -> Optional[str]:
        """Transcribe a single chunk of audio data.
        
        Returns:
            str or None: Transcribed text if speech was detected, None otherwise
        """
        if not self.stream:
            raise RuntimeError("Stream not started. Call start() first or use context manager.")
            
        data = self.stream.read(1536, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            return result["text"].strip()
        return None
        
    def transcribe_stream(self) -> Generator[str, None, None]:
        """Generate transcribed text chunks from the audio stream.
        
        Yields:
            str: Transcribed text chunks when speech is detected
        """
        try:
            while True:
                text = self.transcribe_chunk()
                if text:
                    yield text
        except KeyboardInterrupt:
            print("\nStopping transcription...")
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise
            
    @contextmanager
    def transcribe_session(self):
        """Context manager for a transcription session."""
        self.start()
        try:
            yield self
        finally:
            self.stop()

   