import requests
import hashlib
import os
import time
import argparse
from datetime import datetime, timedelta
import json

HASH_FILE = 'ultimo_hash.txt'
SEEN_FILE = 'tba_seen.txt'
DB_JSON_URL = 'https://raw.githubusercontent.com/agenda-tech-brasil/agenda-tech-brasil/refs/heads/main/src/db/database.json'

def calcular_hash(conteudo):
    return hashlib.sha256(conteudo).hexdigest()

def carregar_hash_anterior():
    if not os.path.exists(HASH_FILE):
        return None
    return open(HASH_FILE, 'r').read().strip()

def salvar_hash_atual(hash_atual):
    with open(HASH_FILE, 'w') as f:
        f.write(hash_atual)

def carregar_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def salvar_seen(nomes):
    with open(SEEN_FILE, 'w') as f:
        for nome in sorted(nomes):
            f.write(nome + "\n")

def esperar_ate_proxima_execucao(hora: int, minuto: int):
    agora = datetime.now()
    proximo = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
    if agora >= proximo:
        proximo += timedelta(days=1)
    secs = (proximo - agora).total_seconds()
    print(f"[{agora.strftime('%H:%M:%S')}] Aguarda até {proximo.strftime('%Y-%m-%d %H:%M:%S')} ({int(secs)}s)...")
    time.sleep(secs)

def verificar_alteracao(url: str) -> bool:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verificando JSON em {url}...")
    resp = requests.get(url)
    resp.raise_for_status()
    conteudo = resp.content
    atual = calcular_hash(conteudo)
    anterior = carregar_hash_anterior()
    if anterior != atual:
        print("✅ JSON MODIFICADO desde a última verificação.")
        salvar_hash_atual(atual)
        return True
    print("ℹ️ Nenhuma alteração detectada.")
    return False

def processar_tba(url: str):
    # Baixa e parseia o JSON
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    tba = data.get('tba', [])
    if not tba:
        print("⚠️ Não há itens em 'tba'.")
        return

    # Últimos 3
    ultimos3 = tba[-3:]

    # Itens novos
    seen = carregar_seen()
    novos = [item for item in tba if item['nome'] not in seen]

    # Combina, evitando duplicados por nome
    combinado = { item['nome']: item for item in ultimos3 }
    for item in novos:
        combinado[item['nome']] = item

    # Exibe
    print("\n📋 Itens TBA (3 últimos + novos):")
    for nome, item in combinado.items():
        cidade = item.get('cidade', '') or ''
        uf     = item.get('uf', '') or ''
        tipo   = item.get('tipo', '') or ''
        print(f"- {nome} | {item.get('url')} | {cidade}/{uf} | {tipo}")

    # Atualiza seen
    todos_nomes = { item['nome'] for item in tba }
    salvar_seen(todos_nomes)
    print("✅ Estado de itens vistos em tba atualizado.\n")

def main():
    parser = argparse.ArgumentParser(description="Monitora alterações num JSON e processa itens de tba.")
    parser.add_argument('--url',
                        default=DB_JSON_URL,
                        help='URL do JSON a ser verificado')
    parser.add_argument('--hour', type=int, default=13, help='Hora diária de execução (0-23)')
    parser.add_argument('--minute', type=int, default=0,  help='Minuto de execução diária (0-59)')
    args = parser.parse_args()

    while True:
        esperar_ate_proxima_execucao(args.hour, args.minute)

        try:
            mudou = verificar_alteracao(args.url)
        except Exception as e:
            print(f"❌ Falha ao verificar alterações: {e}")
            continue

        try:
            processar_tba(args.url)
        except Exception as e:
            print(f"❌ Erro ao processar tba: {e}")

if __name__ == "__main__":
    main()
