# 🚀 DevOps Project API: End-to-End REST Service

Ce projet est une démonstration complète d'un service backend moderne intégrant les principes DevOps : développement API, conteneurisation, automatisation CI/CD, observabilité, sécurité et déploiement Kubernetes.

---

## 🏗️ Architecture du Projet

L'application est construite avec **FastAPI** et utilise **Firebase Firestore** comme base de données NoSQL. Elle est entièrement conteneurisée et orchestrée via GitHub Actions.

### 🛠️ Technologies Utilisées
- **Backend** : FastAPI (Python), Uvicorn.
- **Base de données** : Firebase Firestore.
- **Conteneurisation** : Docker, Docker Compose.
- **Orchestration** : Kubernetes (Manifests YAML).
- **CI/CD** : GitHub Actions.
- **Sécurité** : Bandit (SAST), OWASP ZAP (DAST), Flake8 (Linting).
- **Observabilité** : Prometheus (Metrics), Grafana (Dashboard), Python-JSON-Logger (Logs), OpenTelemetry (Tracing).

---

## 🚀 Guide de Démarrage Local

### 1. Prérequis
- Python 3.9+
- Docker & Docker Compose
- Un fichier `firebase-key.json` valide à la racine.

### 2. Installation & Lancement
```bash
# Clonez le repo
git clone https://github.com/votre-user/devops-project-api.git
cd devops-project-api

# Installation des dépendances
pip install -r requirements.txt

# Lancement local (sans Docker)
uvicorn app.main:app --reload
```

### 3. Utilisation de Docker
```bash
# Build et lancement avec Docker Compose
docker-compose up --build
```
L'API sera accessible sur `http://localhost:8000`.

---

## 📡 API Endpoints (Documentation)

L'API gère une liste de tâches (To-Do List).
- **GET** `/health` : Vérifie l'état de santé de l'API.
- **GET** `/tasks` : Récupère toutes les tâches depuis Firebase.
- **POST** `/tasks` : Crée une nouvelle tâche.
- **PUT** `/tasks/{id}` : Met à jour une tâche existante.
- **DELETE** `/tasks/{id}` : Supprime une tâche.
- **GET** `/metrics` : Expose les métriques Prometheus.
- **GET** `/docs` : Documentation Swagger UI interactive.

---

## 📊 Observabilité & Monitoring

L'application intègre les trois piliers de l'observabilité, avec une stack de monitoring complète dans Kubernetes :

1.  **Logs Structurés** : Utilisation de `python-json-logger` pour produire des logs au format JSON, facilitant l'indexation.
2.  **Métriques** : Intégration de `prometheus-fastapi-instrumentator`. Les métriques sont exposées sur `/metrics`.
3.  **Tracing** : Configuration d'**OpenTelemetry** pour suivre le cycle de vie des requêtes.

### 📈 Monitoring Stack (Kubernetes)
Le dossier `k8s/monitoring/` contient la configuration pour le monitoring en cluster :
- **Prometheus** : Déployé pour scraper automatiquement les métriques de l'API toutes les 5 secondes.
- **Grafana** : Déployé pour visualiser les données, avec Prometheus pré-configuré comme source de données.

---

## 🛡️ Sécurité (DevSecOps)

La sécurité est intégrée à chaque étape du pipeline :
- **SAST (Static Analysis)** : Bandit scanne le code source pour détecter des failles de sécurité.
- **DAST (Dynamic Analysis)** : OWASP ZAP effectue un scan dynamique sur le conteneur en cours d'exécution.
- **Secrets Management** : La clé Firebase est injectée via les GitHub Secrets.

---

## ⚙️ CI/CD Pipeline

Le workflow GitHub Actions (`.github/workflows/main.yml`) automatise tout :
1.  **Linting** : Qualité du code avec `Flake8`.
2.  **Tests** : Tests unitaires avec `Pytest`.
3.  **SAST** : Scan avec `Bandit`.
4.  **Build & Push** : Construction et publication sur Docker Hub.
5.  **DAST** : Scan dynamique avec `OWASP ZAP`.

---

## ☸️ Déploiement Kubernetes

Les fichiers YAML se trouvent dans le dossier `k8s/`.

### Déploiement de l'Application
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Déploiement du Monitoring
```bash
kubectl apply -f k8s/monitoring/prometheus-config.yml
kubectl apply -f k8s/monitoring/stack.yml
```

---

