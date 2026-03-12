FROM python:3.11-slim

# Empêche la création de fichiers .pyc et force l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Récupération de l'exécutable 'uv' depuis l'image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Étape de cache pour les dépendances
COPY pyproject.toml .
# On installe les dépendances listées dans le pyproject.toml
RUN uv pip install --system .

# Copie du script de l'API
COPY main.py .

# Le container écoutera sur le port 8000
EXPOSE 8000

# Lancement : on bind sur 0.0.0.0 pour être accessible depuis l'hôte
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]