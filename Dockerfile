# =============================
# STAGE 1 : build des dépendances
# =============================
FROM python:3.10-slim AS builder

WORKDIR /app

# Installer outils système minimaux pour build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances dans un dossier temporaire
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


# =============================
# STAGE 2 : image finale
# =============================
FROM python:3.10-slim

WORKDIR /app

# Installer juste ce qui est nécessaire pour exécuter
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copier les wheels déjà construits
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copier le code source
COPY . .

EXPOSE 5000

# Démarrage de ton app Flask
CMD ["python", "app.py"]

