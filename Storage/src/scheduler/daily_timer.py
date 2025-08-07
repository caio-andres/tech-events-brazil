import time
from datetime import datetime, timedelta

def esperar_ate_proxima_execucao(hora: int, minuto: int) -> None:
    agora = datetime.now()
    proximo = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
    if agora >= proximo:
        proximo += timedelta(days=1)
    secs = int((proximo - agora).total_seconds())
    print(f"[{agora:%H:%M:%S}] Dormindo por {secs}s até {proximo:%Y-%m-%d %H:%M:%S}")
    time.sleep(secs)
