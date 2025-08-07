import argparse
from config import DB_JSON_URL
from scheduler.daily_timer import esperar_ate_proxima_execucao
from services.verifier import verificar_alteracao
from services.tba_processor import processar_tba

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',    default=DB_JSON_URL)
    parser.add_argument('--hour',   type=int, default=8)
    parser.add_argument('--minute', type=int, default=32)
    args = parser.parse_args()

    while True:
        esperar_ate_proxima_execucao(args.hour, args.minute)
        try:
            verificar_alteracao(args.url)
        except Exception as e:
            print("Erro em verifier:", e)
        try:
            processar_tba(args.url)
        except Exception as e:
            print("Erro em processor:", e)

if __name__ == "__main__":
    main()
