import os
import io
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
import openwakeword
from openwakeword.model import Model

class Listener:
    def __init__(self, model_path: str = "models/please_daddy.onnx", sample_rate: int = 16000, chunk_size: int = 1280):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        openwakeword.utils.download_models()

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"[Listener Erro]: Modelo Wake Word não encontrado em '{model_path}'.")

        self.oww_model = Model(
            wakeword_models=[model_path],
            inference_framework="onnx"
        )
        self.model_key = list(self.oww_model.models.keys())[0]

    def _play_beep(self):
        """1. Opção via Terminal (Windows Bell): Zero dependências e instantâneo."""
        sys.stdout.write('\a')
        sys.stdout.flush()

    def listen(self, transcriber=None) -> np.ndarray | None:
        print("\n[Listener] 🎧 Escutando em segundo plano... Fale 'Please Daddy'!")
        
        detected = False
        
        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
            while True:
                try:
                    chunk, _ = stream.read(self.chunk_size)
                    chunk_flat = chunk.flatten()

                    prediction = self.oww_model.predict(chunk_flat)
                    score = prediction.get(self.model_key, 0.0)

                    if score > 0.5:
                        print(f"\n[Listener] 🎙️ 'Please Daddy' detectado! (Confiança: {score:.2f})")
                        self.oww_model.reset()
                        detected = True
                        break

                except (KeyboardInterrupt, EOFError):
                    return None

        if not detected:
            return None

        # Toca o alerta sonoro
        self._play_beep()

        print("[Listener] Gravando seu comando...")
        command_buffer = []
        silence_chunks = 0
        silence_threshold = 400

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
            while True:
                try:
                    chunk, _ = stream.read(self.chunk_size)
                    chunk_flat = chunk.flatten()
                    command_buffer.append(chunk_flat)

                    volume = np.abs(chunk_flat).mean()
                    if volume < silence_threshold:
                        silence_chunks += 1
                    else:
                        silence_chunks = 0

                    if silence_chunks > 20 or len(command_buffer) > 150:
                        print("[Listener] 🛑 Comando capturado. Processando resposta...")
                        break

                except (KeyboardInterrupt, EOFError):
                    return None

        if command_buffer:
            return np.concatenate(command_buffer).astype(np.float32) / 32768.0

        return None