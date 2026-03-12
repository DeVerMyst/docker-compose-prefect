import random
from datetime import datetime

import httpx
from prefect import flow, task

# httpx.Client() et le bloc with
# Au lieu d'ouvrir une connexion à chaque requête, on utilise un Client.
# Il garde la connexion ouverte pour les requêtes suivantes (Connection Pooling).
# Le with (Context Manager) garantit que la "porte" réseau est refermée proprement dès que le travail est fini,
# évitant les fuites de mémoire et les plantages du serveur.


@task(tags=["calcul_max"], retries=3, retry_delay_seconds=10)
def appeler_api(a, b):
    debut = datetime.now().strftime("%H:%M:%S")
    with httpx.Client(timeout=10.0) as client:
        # On appelle l'API (qui dort 5 secondes)
        r = client.get(f"http://localhost:8000/calcul?a={a}&b={b}")
        res = r.json()["resultat"]

        # On affiche l'heure de FIN pour bien voir les groupes
        fin = datetime.now().strftime("%H:%M:%S")
        print(f"Démarré à {debut} -> Fini à {fin} | Résultat: {res}")
        return res


@flow(name="Demo Concurrence avec UV", log_prints=True)
def pipeline_calcul():
    print("Envoi de 10 tâches à l'API (bridage à 2 via tag)...")

    futures = []
    # 1. On lance les tâches (elles partent en file d'attente)
    for _ in range(10):
        fut = appeler_api.submit(random.randint(1, 10), random.randint(1, 10))
        futures.append(fut)

    # 2. IMPORTANT : On attend explicitement que chaque tâche soit terminée
    for f in futures:
        f.result()

    print("Toutes les tâches sont terminées !")


if __name__ == "__main__":
    pipeline_calcul()
