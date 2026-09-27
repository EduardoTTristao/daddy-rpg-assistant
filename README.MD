# 🎲 D.A.D.D.Y. — Digital Assistant for Dungeon Drafting & You

> **Assistente de RPG autônomo**

O **D.A.D.D.Y.** é um assistente vocal de mesa projetado para Mestres e jogadores de RPG. Ele opera em segundo plano com escuta contínua, basta dizer `"Please Daddy"` que o sistema irá transcrever sua pergunta usando sua GPU local e, por meio de um sistema de RAG, responderá por voz em tempo real.

---

## 🛠️ Arquitetura do Sistema

```text
 [ Microfone (PulseAudio) ]
            │
            ▼
 [ openWakeWord (CPU - ONNX) ] ──(Loop de escuta passiva em 2º plano)
            │
    Gatilho "Please Daddy"
            │
            ▼
 [ Gravação do Comando (VAD) ]
            │
            ▼
 [ Faster-Whisper (GPU CUDA) ] ──► Transcrição local em texto
            │
            ▼
 [ Gemini API (Flash Lite) ]  ──► Processamento do prompt + Agente
            │
            ▼
 [ Gemini TTS (Voz: Milo) ]   ──► Estilo: [seductive, horny, fast]
            │
            ▼
 [ Reprodutor RAM (SoundDevice)] ──► Saída de Áudio na Mesa
```

---

## 📋 Pré-requisitos

Antes de iniciar, garanta que você possui instalado no sistema hospedeiro:

* **Docker** e **Docker Compose**.
* **NVIDIA Container Toolkit** (para suporte a aceleração por GPU CUDA dentro do container).
* **PulseAudio** (ou PipeWire com suporte a PulseAudio) rodando no sistema.
* Uma chave de API do Google Gemini (`GOOGLE_API_KEY`).

---

## 📦 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone [https://github.com/EduardoTTristao/daddy-rpg-assistant.git](https://github.com/EduardoTTristao/daddy-rpg-assistant.git)
cd daddy-rpg-assistant
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com a sua chave da API do Gemini:
```env
GOOGLE_API_KEY=sua_chave_api_aqui
```

---

## 🎧 Configuração do Áudio (PulseAudio Daemon)

Para que o container Docker consiga acessar o seu microfone e saídas de áudio sem conflitos de permissão, é necessário manter o servidor de áudio ativo rodando em um terminal separado no sistema hospedeiro.

1. Abra um **novo terminal dedicado** no seu sistema hospedeiro.
2. Garanta que o daemon do PulseAudio está rodando e expondo o socket correto executando:
   ```bash
   pulseaudio --daemon
   ```
3. Mantenha este terminal aberto durante toda a execução do D.A.D.D.Y.

---

## 🚀 Como Executar

Com o daemon do PulseAudio ativo no outro terminal, execute os seguintes comandos no terminal principal do projeto:

### 1. Construir a Imagem Docker
```bash
docker compose build
```

### 2. Iniciar o Agente
```bash
docker compose run --rm daddy
```

---

## 🎮 Como Usar na Mesa de RPG

1. Assim que a aplicação iniciar, você verá no terminal:
   ```text
   [Listener] 🎧 Escutando em segundo plano... Fale 'Please Daddy'!
   ```
2. Fale **"Please Daddy"** próximo ao microfone.
3. O sistema identificará o gatilho e começará a gravar o seu comando:
   ```text
   [Listener] 🎙️ 'Please Daddy' detectado!
   [Listener] Gravando seu comando...
   ```
4. Faça a sua pergunta (ex: *"Quais são os efeitos básicos da magia desejo?"*).
5. Após uma breve pausa de fala, o D.A.D.D.Y. processará a pergunta e responderá em voz alta.

---

## 📌 To-Do / Próximos Passos

- [ ] Adicionar tool de consulta de classe (e sua respectiva base de dados baixada do 5e tools)
- [ ] Adicionar tool de consulta de regras (e sua respectiva base de dados baixada do 5e tools)
- [ ] Adicionar tool de consulta de feats (e sua respectiva base de dados baixada do 5e tools)
- [ ] Adicionar tool de consulta de itens (e sua respectiva base de dados baixada do 5e tools)
- [ ] Adicionar tool de consulta de especies (e sua respectiva base de dados baixada do 5e tools)
- [ ] Adicionar tool de consulta de monstros (e sua respectiva base de dados baixada do 5e tools)
- [ ] Historico de chat
- [ ] Filtrar somente 24 ou 14, dependendo do pedido do usuário
- [ ] Criar um subagente com analise estatistica tendo tools de calculo medio de dano, vida efetiva, probabilidades e etc.

---

## 📜 Licença

Este projeto é voltado para uso pessoal e de entretenimento em mesas de RPG. Distribuído sob a licença MIT.