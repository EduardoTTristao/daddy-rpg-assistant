import os
import io
import sounddevice as sd
import soundfile as sf
from google import genai
from google.genai import types
import time
import numpy as np

class Speaker:
    def __init__(self, voice_name: str = "Milo", model_name: str = "gemini-3.8-flash-lite-tts"):
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.voice_name = voice_name

    def speak(self, text: str):
        if not text or not text.strip():
            return

        try:

            styled_text = f"[seductive, horny, fast] {text}"

            config = types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self.voice_name
                        )
                    )
                )
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=styled_text,
                config=config
            )

            audio_bytes = None
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        audio_bytes = part.inline_data.data
                        break

            if not audio_bytes:
                print("[Speaker Erro]: Nenhum dado de áudio retornado pelo Gemini.")
                return

            # 1. Lê o áudio diretamente da memória RAM
            data, fs = sf.read(io.BytesIO(audio_bytes))

            # 2. Cria 0.3 segundos de silêncio (zeros) com a mesma estrutura de canais
            padding_samples = int(fs * 0.6)
            if data.ndim > 1:
                silence = np.zeros((padding_samples, data.shape[1]), dtype=data.dtype)
            else:
                silence = np.zeros(padding_samples, dtype=data.dtype)

            # 3. Anexa o silêncio ao final do áudio original
            data_padded = np.concatenate([data, silence])

            # 4. Toca o áudio com o padding extra e aguarda o flush completo do PulseAudio
            sd.play(data_padded, fs)
            sd.wait()
            time.sleep(0.5)  # Garante que a placa de som no Windows processou o buffer inteiro

        except Exception as e:
            print(f"[Speaker Erro]: Falha ao gerar ou reproduzir áudio via Gemini TTS: {e}")