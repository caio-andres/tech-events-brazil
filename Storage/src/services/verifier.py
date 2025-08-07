import requests
from datetime import datetime
from utils.hash_utils import calcular_hash
from utils.file_utils import read_text, write_text
from config import HASH_FILE

def verificar_alteracao(url: str) -> bool:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Baixando {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    atual = calcular_hash(resp.content)
    anterior = read_text(HASH_FILE)

    if anterior != atual:
        print("✅ Detectada alteração.")
        write_text(HASH_FILE, atual)
        return True

    print("ℹ️ Sem alterações.")
    return False
