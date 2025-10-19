# 📝 QuickTask - Gestor Minimalista de Tareas

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**QuickTask** es una aplicación minimalista de gestión de tareas personales desarrollada con **FastAPI** y **SQLite**, siguiendo la metodología **Vibe Coding** (colaboración humano-IA).

## 🚀 Características

- ✅ **CRUD completo** de tareas (Crear, Leer, Actualizar, Eliminar)
- 🗄️ **Persistencia** con SQLite y SQLAlchemy ORM
- ✨ **Validación** automática con Pydantic
- 📚 **Documentación interactiva** con Swagger UI
- 🧪 **Pruebas unitarias** con pytest
- 🐳 **Despliegue** con Docker y docker-compose
- 🎯 **Código limpio** y tipado

## 📦 Estructura del Proyecto

```
QuickTask/
│
├── app/
│   ├── __init__.py          # Inicialización del paquete
│   ├── main.py              # Aplicación FastAPI y rutas
│   ├── database.py          # Configuración de SQLAlchemy
│   ├── models.py            # Modelos ORM
│   ├── schemas.py           # Esquemas Pydantic
│   └── crud.py              # Operaciones CRUD
│
├── tests/
│   ├── __init__.py
│   └── test_tasks.py        # Tests unitarios
│
├── requirements.txt         # Dependencias
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Orquestación
├── .gitignore
├── .dockerignore
└── README.md
```

## 🛠️ Instalación y Ejecución

### Opción 1: Ejecución Local con Python

#### 1. Clonar o navegar al directorio del proyecto

```powershell
cd QuickTask
```

#### 2. Crear y activar entorno virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar en Windows PowerShell
.\venv\Scripts\Activate.ps1

# Activar en Windows CMD
.\venv\Scripts\activate.bat
```

#### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

#### 4. Ejecutar la aplicación

```powershell
# Opción 1: Con uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Ejecutar el script main.py
python -m app.main
```

#### 5. Acceder a la aplicación

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Opción 2: Ejecución con Docker

#### 1. Construir y ejecutar con docker-compose

```powershell
docker-compose up --build
```

#### 2. Detener los contenedores

```powershell
docker-compose down
```

#### 3. Acceder a la aplicación

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## 🧪 Ejecutar Pruebas

### Ejecutar todos los tests

```powershell
pytest
```

### Ejecutar tests con cobertura

```powershell
pytest --cov=app --cov-report=html
```

### Ejecutar tests en modo verbose

```powershell
pytest -v
```

## 📡 API Endpoints

### Documentación Interactiva

La documentación completa está disponible en `/docs` cuando la aplicación está ejecutándose.

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Verificación de salud |
| `POST` | `/tasks` | Crear nueva tarea |
| `GET` | `/tasks` | Listar todas las tareas |
| `GET` | `/tasks/{id}` | Obtener tarea específica |
| `PUT` | `/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/tasks/{id}` | Eliminar tarea |

## 📋 Ejemplos de Uso con curl

### 1. Crear una nueva tarea

```powershell
curl -X POST "http://localhost:8000/tasks" `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Comprar leche",
    "description": "Ir al supermercado y comprar leche descremada"
  }'
```

### 2. Listar todas las tareas

```powershell
curl -X GET "http://localhost:8000/tasks"
```

### 3. Obtener una tarea específica

```powershell
curl -X GET "http://localhost:8000/tasks/1"
```

### 4. Actualizar una tarea (marcar como completada)

```powershell
curl -X PUT "http://localhost:8000/tasks/1" `
  -H "Content-Type: application/json" `
  -d '{
    "completed": true
  }'
```

### 5. Actualizar título y descripción

```powershell
curl -X PUT "http://localhost:8000/tasks/1" `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Comprar leche y pan",
    "description": "Ir al supermercado antes de las 6pm"
  }'
```

### 6. Eliminar una tarea

```powershell
curl -X DELETE "http://localhost:8000/tasks/1"
```

### 7. Filtrar tareas completadas

```powershell
curl -X GET "http://localhost:8000/tasks?completed=true"
```

### 8. Filtrar tareas pendientes con paginación

```powershell
curl -X GET "http://localhost:8000/tasks?completed=false&skip=0&limit=10"
```

## 📊 Modelos de Datos

### Task (Tarea)

```python
{
  "id": 1,                    # Generado automáticamente
  "title": "Título",          # Obligatorio, máx 200 caracteres
  "description": "Desc...",   # Opcional, máx 1000 caracteres
  "completed": false          # Por defecto: false
}
```

## 🔧 Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno y rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM para Python
- **[Pydantic](https://docs.pydantic.dev/)** - Validación de datos
- **[SQLite](https://www.sqlite.org/)** - Base de datos embebida
- **[Pytest](https://docs.pytest.org/)** - Framework de testing
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Docker](https://www.docker.com/)** - Contenedores

## 🎯 Metodología: Vibe Coding

Este proyecto fue desarrollado siguiendo la metodología **Vibe Coding**, una aproximación colaborativa donde:

- 🧠 **El humano** aporta la intención, criterio y contexto
- 🤖 **La IA** colabora generando código, pruebas y documentación
- 🔄 **Flujo iterativo** entre creatividad y técnica

### Principios aplicados:

1. ✅ Estructura modular y organizada
2. ✅ Código limpio con tipado
3. ✅ Documentación automática
4. ✅ Pruebas exhaustivas
5. ✅ Despliegue reproducible

## 📝 Notas de Desarrollo

### Base de Datos

- El archivo `quicktask.db` se crea automáticamente en la raíz del proyecto
- Para usar una base de datos en memoria (testing), se configura en los tests
- Para producción, considera migrar a PostgreSQL o MySQL

### Variables de Entorno

Puedes crear un archivo `.env` para configuraciones personalizadas:

```env
DATABASE_URL=sqlite:///./quicktask.db
HOST=0.0.0.0
PORT=8000
```

### Migraciones

Para proyectos más complejos, considera usar **Alembic** para migraciones de base de datos:

```powershell
pip install alembic
alembic init alembic
```

## 🐛 Solución de Problemas

### Error: "Module not found"

Asegúrate de estar en el entorno virtual activado y haber instalado las dependencias:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Address already in use"

El puerto 8000 está ocupado. Usa otro puerto:

```powershell
uvicorn app.main:app --reload --port 8001
```

### Tests fallan

Verifica que estés en el directorio raíz del proyecto:

```powershell
cd QuickTask
pytest -v
```

## 🚀 Próximas Mejoras

- [ ] Autenticación y autorización (JWT)
- [ ] Categorías y etiquetas para tareas
- [ ] Fechas de vencimiento y recordatorios
- [ ] Frontend con React/Vue
- [ ] API de notificaciones
- [ ] Exportar tareas a CSV/JSON
- [ ] Búsqueda y filtros avanzados

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado con la metodología **Vibe Coding** - Colaboración Humano-IA.

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

📧 ¿Preguntas o sugerencias? Abre un issue o contacta al equipo.

---

**¡Happy Coding! 🎉**
