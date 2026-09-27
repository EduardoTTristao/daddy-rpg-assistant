FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    portaudio19-dev \
    libpulse0 \
    pulseaudio-utils \
    libasound2-plugins \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Redireciona o áudio ALSA para o PulseAudio
RUN echo "pcm.!default {\n  type pulse\n}\nctl.!default {\n  type pulse\n}" > /etc/asound.conf

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]