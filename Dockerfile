# =============================
# IMAGE FINALE
# =============================
FROM python:3.10-slim

WORKDIR /app

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

EXPOSE 5000

# Démarrage de l'application Flask
CMD ["python", "app.py"]
