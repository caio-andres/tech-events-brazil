import requests
import os
from utils.file_utils import read_lines, write_lines
from config import SEEN_FILE

# Adicione esta linha para pegar o ID do canal do .env
NOTIFY_CHANNEL_ID = int(os.getenv("NOTIFY_CHANNEL_ID", "0"))
DISCORD_NOTIFY_URL = (
    "http://localhost:8000/notify_new_events"  # ajuste a URL se rodar fora do localhost
)


def processar_tba(url: str) -> None:
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get("tba", [])
    if not data:
        print("⚠️ tba vazio.")
        return

    ultimos3 = data[-3:]
    seen = read_lines(SEEN_FILE)
    novos = [e for e in data if e["nome"] not in seen]

    # Notifica o Discord apenas com os novos eventos!
    if novos and NOTIFY_CHANNEL_ID:
        print("Enviando novos eventos para o Discord...")
        try:
            resp_notify = requests.post(
                DISCORD_NOTIFY_URL,
                json={"novos_eventos": novos, "channel_id": NOTIFY_CHANNEL_ID},
                timeout=10,
            )
            print("Resposta do Discord:", resp_notify.text)
        except Exception as e:
            print("Falha ao notificar o Discord:", e)

    combinado = {e["nome"]: e for e in ultimos3 + novos}
    print("\n📋 TBA (3 últimos + novos):")
    for nome, item in combinado.items():
        cidade, uf, tipo = (
            item.get("cidade", ""),
            item.get("uf", ""),
            item.get("tipo", ""),
        )
        print(f"- {nome} | {item['url']} | {cidade}/{uf} | {tipo}")

    write_lines(SEEN_FILE, {e["nome"] for e in data})
    print("✅ tba_seen atualizado.\n")
