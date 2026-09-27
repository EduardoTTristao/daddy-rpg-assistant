import sounddevice as sd
import numpy as np

class Listener:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.channels = 1

    def listen(self) -> np.ndarray:
        input("\n[Listener] Pressione ENTER para começar a falar...")
        print("[Listener] Gravando... Pressione ENTER para parar.")

        audio_chunks = []

        def callback(indata, frames, time, status):
            if status:
                print(f"[Listener] Status: {status}")
            audio_chunks.append(indata.copy())

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            callback=callback,
        ):
            input()

        print("[Listener] Gravação finalizada.")
        
        if not audio_chunks:
            return np.array([], dtype=np.float32)

        audio_data = np.concatenate(audio_chunks, axis=0).flatten()
        return audio_data