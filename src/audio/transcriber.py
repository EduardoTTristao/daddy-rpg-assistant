import numpy as np
from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_size: str = "small", device: str = "cuda", compute_type: str = "float16"):
        print(f"[Transcriber] Carregando modelo Whisper '{model_size}' na GPU ({device})...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("[Transcriber] Modelo Whisper pronto!")

    def transcribe(self, audio_data: np.ndarray) -> str:
        if audio_data.size == 0:
            return ""

        segments, _ = self.model.transcribe(
            audio_data,
            beam_size=5,
            language="pt"
        )

        text = " ".join([segment.text.strip() for segment in segments])
        return text.strip()