from prefect import flow, task
import httpx
import random
from datetime import datetime

@task(tags=["calcul_max"], retries=3, retry_delay_seconds=5)
def appeler_api(a, b):
    debut = datetime.now().strftime("%H:%M:%S")
    with httpx.Client(timeout=10.0) as client:
        r = client.get(f"http://localhost:8000/calcul?a={a}&b={b}")
        res = r.json()["resultat"]
        fin = datetime.now().strftime("%H:%M:%S")
        print(f"[{debut} -> {fin}] Calcul : {a}+{b} = {res}")
        return res

@flow(name="Flow Ordonnance toutes les 10s")
def pipeline_calcul_recurrent():
    a, b = random.randint(1, 10), random.randint(1, 10)
    appeler_api(a, b)

if __name__ == "__main__":
    # Cette commande crée un "Deployment" avec un planning (interval de 10s)
    pipeline_calcul_recurrent.serve(
        name="mon-deployment-automatique",
        interval=20 # on définit le scheduling (en secondes)
    )