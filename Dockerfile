# =============================
# IMAGE FINALE
# =============================
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour scikit-surprise et pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libgomp1 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir numpy==1.21.6 pandas==1.5.3
RUN pip install --no-cache-dir scikit-surprise Flask

# Copier le code source de l’application
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Démarrer l’application Flask
CMD ["python", "app.py"]
