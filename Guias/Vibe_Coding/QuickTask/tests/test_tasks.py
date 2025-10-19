"""
📁 test_tasks.py
Pruebas unitarias e integración para la API de tareas.
Utiliza una base de datos SQLite en memoria para aislar las pruebas.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Configurar base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia de base de datos para usar la base de pruebas"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override de la dependencia
app.dependency_overrides[get_db] = override_get_db

# Cliente de pruebas
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Fixture que se ejecuta antes de cada test.
    Crea las tablas y las elimina después del test.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ==================== TESTS DE ENDPOINTS ====================

def test_read_root():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "QuickTask" in response.json()["message"]


def test_health_check():
    """Test del endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    """Test de creación de una nueva tarea"""
    task_data = {
        "title": "Comprar leche",
        "description": "Ir al supermercado y comprar leche descremada"
    }
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] is False
    assert "id" in data


def test_create_task_without_description():
    """Test de creación de tarea sin descripción (campo opcional)"""
    task_data = {
        "title": "Llamar al dentista"
    }
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] is None
    assert data["completed"] is False


def test_create_task_validation_error():
    """Test de validación al crear tarea sin título"""
    task_data = {
        "description": "Descripción sin título"
    }
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 422  # Validation Error


def test_get_all_tasks_empty():
    """Test de obtener tareas cuando no hay ninguna"""
    response = client.get("/tasks")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks():
    """Test de obtener todas las tareas"""
    # Crear varias tareas
    tasks = [
        {"title": "Tarea 1", "description": "Descripción 1"},
        {"title": "Tarea 2", "description": "Descripción 2"},
        {"title": "Tarea 3", "description": "Descripción 3"}
    ]
    
    for task in tasks:
        client.post("/tasks", json=task)
    
    # Obtener todas las tareas
    response = client.get("/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all("id" in task for task in data)


def test_get_task_by_id():
    """Test de obtener una tarea específica por ID"""
    # Crear tarea
    task_data = {"title": "Tarea específica", "description": "Descripción"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Obtener la tarea
    response = client.get(f"/tasks/{task_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_get_task_not_found():
    """Test de intentar obtener una tarea que no existe"""
    response = client.get("/tasks/9999")
    
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


def test_update_task():
    """Test de actualización completa de una tarea"""
    # Crear tarea
    task_data = {"title": "Tarea original", "description": "Descripción original"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Actualizar tarea
    update_data = {
        "title": "Tarea actualizada",
        "description": "Nueva descripción",
        "completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["completed"] is True


def test_update_task_partial():
    """Test de actualización parcial (solo el estado)"""
    # Crear tarea
    task_data = {"title": "Tarea parcial", "description": "Descripción"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Actualizar solo el estado
    update_data = {"completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]  # No cambió
    assert data["description"] == task_data["description"]  # No cambió
    assert data["completed"] is True  # Cambió


def test_update_task_not_found():
    """Test de actualizar una tarea que no existe"""
    update_data = {"title": "Nueva tarea"}
    response = client.put("/tasks/9999", json=update_data)
    
    assert response.status_code == 404


def test_delete_task():
    """Test de eliminación de una tarea"""
    # Crear tarea
    task_data = {"title": "Tarea a eliminar"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Eliminar tarea
    response = client.delete(f"/tasks/{task_id}")
    
    assert response.status_code == 204
    
    # Verificar que ya no existe
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test de eliminar una tarea que no existe"""
    response = client.delete("/tasks/9999")
    
    assert response.status_code == 404


def test_filter_tasks_by_completed():
    """Test de filtrado de tareas por estado"""
    # Crear tareas con diferentes estados
    client.post("/tasks", json={"title": "Tarea 1"})
    task2_response = client.post("/tasks", json={"title": "Tarea 2"})
    task3_response = client.post("/tasks", json={"title": "Tarea 3"})
    
    # Marcar algunas como completadas
    client.put(f"/tasks/{task2_response.json()['id']}", json={"completed": True})
    client.put(f"/tasks/{task3_response.json()['id']}", json={"completed": True})
    
    # Filtrar solo pendientes
    response_pending = client.get("/tasks?completed=false")
    assert response_pending.status_code == 200
    assert len(response_pending.json()) == 1
    
    # Filtrar solo completadas
    response_completed = client.get("/tasks?completed=true")
    assert response_completed.status_code == 200
    assert len(response_completed.json()) == 2


def test_pagination():
    """Test de paginación"""
    # Crear 10 tareas
    for i in range(10):
        client.post("/tasks", json={"title": f"Tarea {i+1}"})
    
    # Obtener las primeras 5
    response = client.get("/tasks?skip=0&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    # Obtener las siguientes 5
    response = client.get("/tasks?skip=5&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
