# Démo : Concurrence & Orchestration (FastAPI + Prefect)

Ce projet démontre comment limiter la charge sur une infrastructure (API) en utilisant les **Tags** et les **Concurrency Limits** de Prefect.

## Lancer l'API (Infrastructure)

Dans le dossier contenant le `Dockerfile` et le `docker-compose.yml` :

```bash
docker compose up -d
```

*L'API est maintenant disponible sur `http://localhost:8000`.*

## Configurer l'Orchestrateur (Prefect)
Ouvre un terminal et lance le serveur local de Prefect :

```bash
prefect server start
```

*Accède à l'interface sur `http://localhost:4200`.*

## Créer la règle de limitation

Dans un **nouveau terminal** (connecté au serveur prefect déjà lancé), crée le "feu de signalisation" pour le tag `calcul_max` (limite à 2 exécutions simultanées) :

```bash
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect concurrency-limit create calcul_max 2
```

## Exécuter le Workflow

Lance le script Python qui va envoyer 10 requêtes d'un coup :

```bash
python flow_prefect.py
```


> **Ce qu'il faut observer :** Les logs s'affichent **2 par 2** toutes les 5 secondes (malgré l'envoi simultané).


--- 