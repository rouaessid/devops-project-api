# Image de base python légère
FROM python:3.9-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie des requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app/ app/

# Copie de la clé (Docker en a besoin, mais elle ne sera pas dans Git grâce au .gitignore)
COPY firebase-key.json .

# Commande de lancement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]