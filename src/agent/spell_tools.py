import json
import os
from rapidfuzz import fuzz
from langchain_core.tools import tool

DATA_PATH = "data/spells_all.json"

def _extract_text(entry) -> str:
    """Extrai todo o texto contido nos campos 'entries' do 5eTools (recursivo para dicts/lists)."""
    if isinstance(entry, str):
        return entry
    if isinstance(entry, list):
        return " ".join(_extract_text(e) for e in entry)
    if isinstance(entry, dict):
        sub_entries = entry.get("entries", [])
        return f"{entry.get('name', '')} " + " ".join(_extract_text(e) for e in sub_entries)
    return ""

def _load_spells() -> list[dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("spell", [])

@tool
def search_spells(query: str, top_k: int = 3) -> str:
    """Busca magias no banco do 5eTools por nome ou palavras-chave de efeito/descrição.
    Retorna o JSON bruto das magias mais relevantes encontradas.

    Você sempre deve suar essa função. Nunca assuma que sabe sobre uma magia.
    """
    spells = _load_spells()
    if not spells:
        return "Nenhuma magia encontrada na base de dados local."

    query_lower = query.lower()
    scored_spells = []

    for spell in spells:
        name = spell.get("name", "")
        entries_text = _extract_text(spell.get("entries", []))

        # Pontuação no nome (peso 70%)
        name_score = fuzz.token_set_ratio(query_lower, name.lower())
        
        # Pontuação na descrição (peso 30%)
        text_score = fuzz.partial_ratio(query_lower, entries_text.lower())

        total_score = (name_score * 0.7) + (text_score * 0.3)

        if total_score > 35:
            scored_spells.append((total_score, spell))

    # Ordena pelos melhores scores
    scored_spells.sort(key=lambda x: x[0], reverse=True)
    results = [spell for _, spell in scored_spells[:top_k]]

    if not results:
        return f"Nenhuma magia correspondente encontrada para '{query}'."

    print(f"Contexto resgatado: \n{results}")

    return json.dumps(results, ensure_ascii=False)