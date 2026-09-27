import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.agent.spell_tools import search_spells

SYSTEM_PROMPT = (
    "Você é o D.A.D.D.Y. (Database Assistant for Dumb Doubts & Yelling), assistente de regras e magias de D&D 5e para o Mestre da mesa.\n\n"
    "Sua missão é ajudar o Mestre a tomar decisões rápidas com base estrita na regra escrita (RAW - Rules As Written).\n\n"
    "Instruções obrigatórias para sua resposta:\n"
    "1. Indique claramente a fonte do texto e o nome da magia/regra (ex: 'Na magia Fireball do Player's Handbook...').\n"
    "2. Cite os trechos da regra/efeito de forma literal utilizando explicitamente a expressão 'abre aspas' e 'fecha aspas' para delimitar a citação direta. Exemplo: abre aspas 'a target takes 8d6 fire damage' fecha aspas.\n"
    "3. Seja sucinto, objetivo e direto ao ponto da dúvida para não interromper o ritmo da sessão.\n"
    "4. A sua resposta será lida por um sintetizador de voz (TTS) e também exibida na tela do terminal, por isso não deve utilizar markdown na sua resposta deixando o texto mais limpo possível. Não adicione negrito em nada."
    "5. Sempre que puxar um dado que venha dos livros oficiais, cheque se não possui uma versão mais recente em outro livro repetindo uma busca mais abrangente. Caso existam divergências, explique as duas versões para o usuário, mas priorize em falar da mais nova e apenas fale por cima da antiga (apenas explique detalhadamente se o usuário pedir para você explicar justamente as diferenças entre as versões). Caso não exista divergencia e o usuário não falou nada de versões, não precisa mencionar nada sobre as versões."
    "Por fim, seja sempre direto. As perguntas direcionadas para você devem ser respondidas o mais rápido possivel. Seja conciso e vá direto ao ponto. Caso a pergunta do usuário precisa de uma resposta mais longa, você pode explicar os detalhes. Mas caso seja pontual, seja breve e claro. Nunca seja prolixo. Sempre priorize um texto curto e rápido. Não enrole."
)

class DaddyAgent:
    def __init__(self, transcriber=None, speaker=None, listener=None, model_name: str = "gemini-3.8-flash"):
        self.transcriber = transcriber
        self.speaker = speaker
        self.listener = listener

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1
        )
        tools = [search_spells]
        
        self.agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

    def ask(self, query: str) -> str:
        inputs = {"messages": [("user", query)]}
        result = self.agent.invoke(inputs)
        return result["messages"][-1].content

    def start(self):
        print("\n[D.A.D.D.Y.] Orquestrador e Agente de Decisões prontos!")

        while True:
            query = ""

            # 1. Captura de áudio ou fallback para digitação no terminal
            if self.listener:
                audio_data = self.listener.listen()
                if audio_data.size == 0:
                    continue
                if self.transcriber:
                    query = self.transcriber.transcribe(audio_data)
                    print(f"\n[Mestre (Transcrito)]: {query}")
            else:
                query = input("\n[Mestre (Digite a dúvida)]: ")

            if not query.strip():
                continue

            # 2. Processa com o LangGraph / Gemini
            response = self.ask(query)[-1]["text"]

            # 3. Printa no terminal para leitura do Mestre
            print("\n" + "=" * 40)
            print(f"[D.A.D.D.Y. - Resposta RAW]:\n{response}")
            print("=" * 40 + "\n")

            # 4. Fala a resposta no Speaker caso esteja ativo
            if self.speaker:
                self.speaker.speak(response)