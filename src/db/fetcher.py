import os
import json
import requests

class SpellFetcher:
    BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/spells"
    DATA_DIR = "data"

    def _get_spell_files(self):
        index_url = f"{self.BASE_URL}/index.json"

        response = requests.get(index_url, timeout=10)
        response.raise_for_status()
        index_data = response.json()
        
        return list(index_data.values()) if isinstance(index_data, dict) else index_data

    def sync_spells(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)
        print("[Fetcher] Sincronizando base de magias do 5eTools...")

        spell_files = self._get_spell_files()
        all_spells = []

        for file_name in spell_files:
            url = f"{self.BASE_URL}/{file_name}"
            dest_path = os.path.join(self.DATA_DIR, file_name)

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            spells = data.get("spell", [])
            all_spells.extend(spells)

            print(f"  └─ [OK] {file_name} ({len(spells)} magias)")

        unified_path = os.path.join(self.DATA_DIR, "spells_all.json")
        with open(unified_path, "w", encoding="utf-8") as f:
            json.dump({"spell": all_spells}, f, ensure_ascii=False, indent=2)

        print(f"[Fetcher] Sincronização concluída! Total de {len(all_spells)} magias.")