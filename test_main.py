from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

# Client de test
client = TestClient(app)

# 1. Test Simple : Health Check
def test_read_health():
    """Vérifie que l'API répond OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 2. Test Observabilité : Metrics Prometheus
def test_metrics_endpoint():
    """Vérifie que Prometheus expose bien les métriques"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_info" in response.text

# 3. Test Complexe : Création de tâche (AVEC MOCK)
@patch("app.main.db")
def test_create_task(mock_db):
    """Teste la route POST /tasks en simulant Firebase"""
    # On prépare le faux objet (Mock)
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_document
    
    # Données de test
    task_payload = {"title": "Test Task", "description": "Unit Test", "completed": False}

    # Appel de l'API
    response = client.post("/tasks", json=task_payload)

    # Vérifications
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    
    # Preuve qu'on a bien appelé la "fausse" base de données
    mock_collection.document.assert_called()