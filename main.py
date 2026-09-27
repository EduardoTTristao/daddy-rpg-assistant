import sys
from dotenv import load_dotenv

from src.db.fetcher import SpellFetcher
from src.audio.transcriber import Transcriber
from src.audio.speaker import Speaker
from src.audio.listener import Listener
from src.agent.daddy_agent import DaddyAgent

# Carrega variáveis de ambiente (.env)
load_dotenv()

def main():
    print("[D.A.D.D.Y.] Inicializando o assistente...")

    fetcher = SpellFetcher()
    fetcher.sync_spells()

    transcriber = Transcriber()
    speaker = Speaker()
    listener = Listener()

    daddy = DaddyAgent(
        transcriber=transcriber,
        speaker=speaker,
        listener=listener
    )

    print("[D.A.D.D.Y.] Pronto para uso na mesa! Aguardando invocação...")
    daddy.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[D.A.D.D.Y.] Encerrando com sucesso.")
        sys.exit(0)