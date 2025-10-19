# 📊 Arquitectura de QuickTask

## 🏗️ Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente HTTP                          │
│                    (Browser, curl, Postman)                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP Requests
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    main.py                            │  │
│  │  - Rutas REST (/tasks)                               │  │
│  │  - Inyección de dependencias                         │  │
│  │  - Manejo de errores                                 │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  schemas.py                           │  │
│  │  - Validación con Pydantic                           │  │
│  │  - TaskCreate, TaskUpdate, TaskResponse              │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   crud.py                             │  │
│  │  - create_task()                                     │  │
│  │  - get_tasks()                                       │  │
│  │  - update_task()                                     │  │
│  │  - delete_task()                                     │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               database.py                             │  │
│  │  - SQLAlchemy Engine                                 │  │
│  │  - SessionLocal                                      │  │
│  │  - get_db() dependency                               │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 models.py                             │  │
│  │  - Task (ORM Model)                                  │  │
│  │  - Definición de tabla                               │  │
│  └────────────┬──────────────────────────────────────────┘  │
└────────────────┼──────────────────────────────────────────┘
                 │
                 │ SQL Queries
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      SQLite Database                         │
│                      quicktask.db                            │
│  ┌────────────────────────────────────────┐                │
│  │           Tabla: tasks                  │                │
│  ├────────┬──────────┬──────────┬─────────┤                │
│  │   id   │  title   │  desc... │ complet │                │
│  ├────────┼──────────┼──────────┼─────────┤                │
│  │   1    │  Task 1  │  Desc 1  │  false  │                │
│  │   2    │  Task 2  │  Desc 2  │  true   │                │
│  └────────┴──────────┴──────────┴─────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de una Petición

### Ejemplo: Crear una nueva tarea

```
1. Cliente envía POST /tasks con JSON
   ↓
2. FastAPI recibe request en main.py
   ↓
3. Pydantic valida datos con TaskCreate (schemas.py)
   ↓
4. Se llama a crud.create_task() con datos validados
   ↓
5. CRUD convierte a modelo ORM (models.Task)
   ↓
6. SQLAlchemy ejecuta INSERT en SQLite
   ↓
7. Se retorna Task con ID generado
   ↓
8. Pydantic serializa a TaskResponse
   ↓
9. FastAPI envía JSON response al cliente
```

## 🧩 Componentes Principales

### 1. **main.py** - Controlador
- Define las rutas HTTP
- Maneja requests/responses
- Inyecta dependencias (DB session)
- Gestiona errores HTTP

### 2. **schemas.py** - Validación
- Define contratos de API
- Valida datos entrantes
- Serializa respuestas
- Documentación automática

### 3. **crud.py** - Lógica de Negocio
- Operaciones sobre datos
- Abstrae la capa de datos
- Independiente de HTTP
- Reutilizable

### 4. **models.py** - Capa de Datos
- Define estructura de BD
- Mapeo objeto-relacional
- Constraints y relaciones

### 5. **database.py** - Conexión
- Configuración de SQLAlchemy
- Pool de conexiones
- Gestión de sesiones

## 📝 Esquema de Datos

### Modelo Task

```python
Task
├── id: Integer (PK, Auto-increment)
├── title: String (NOT NULL, MAX 200)
├── description: String (NULLABLE, MAX 1000)
└── completed: Boolean (DEFAULT False)
```

### Esquemas Pydantic

```python
TaskCreate (Input)          TaskResponse (Output)
├── title                   ├── id
├── description             ├── title
                            ├── description
                            └── completed

TaskUpdate (Partial Input)
├── title (optional)
├── description (optional)
└── completed (optional)
```

## 🔐 Principios de Diseño

### 1. **Separación de Responsabilidades**
- Cada módulo tiene un propósito específico
- Bajo acoplamiento, alta cohesión

### 2. **Inyección de Dependencias**
- FastAPI gestiona ciclo de vida de sesiones DB
- Facilita testing con mocks

### 3. **Validación en Capas**
- Pydantic valida formato
- CRUD valida lógica de negocio
- SQLAlchemy valida constraints DB

### 4. **Manejo de Errores**
- Validación → 422 Unprocessable Entity
- No encontrado → 404 Not Found
- Creación exitosa → 201 Created
- Eliminación exitosa → 204 No Content

## 🧪 Testing Strategy

### Base de Datos en Memoria
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
```
- Aislamiento completo
- Sin efectos secundarios
- Rápido y eficiente

### Cobertura de Tests
- ✅ Endpoints REST
- ✅ Validación de datos
- ✅ Casos exitosos
- ✅ Casos de error
- ✅ Filtrado y paginación
- ✅ Actualizaciones parciales

## 🐳 Despliegue Docker

### Dockerfile Multi-Stage
```
Stage 1 (builder): Instalar dependencias
Stage 2 (runtime): Copiar solo lo necesario
```

**Beneficios:**
- Imagen más pequeña
- Mayor seguridad (usuario no-root)
- Mejor rendimiento

### Docker Compose
```yaml
services:
  quicktask-api:
    - Auto-restart
    - Health checks
    - Volume mounting
    - Port mapping
```

## 📈 Escalabilidad

### Horizontal
- Stateless API
- Múltiples instancias
- Load balancer

### Vertical
- Aumentar recursos container
- Pool de conexiones DB
- Caching (Redis)

### Base de Datos
- Migrar a PostgreSQL para producción
- Índices en campos frecuentes
- Conexión pool optimizado

## 🔜 Evolución del Proyecto

### Fase 1: MVP ✅ (Actual)
- CRUD básico
- SQLite
- Tests unitarios

### Fase 2: Producción
- Autenticación JWT
- PostgreSQL
- Migraciones Alembic
- Logging estructurado

### Fase 3: Características Avanzadas
- Categorías y etiquetas
- Fechas límite
- Notificaciones
- Búsqueda full-text

### Fase 4: Frontend
- React/Vue SPA
- WebSockets para real-time
- PWA para móvil

---

**Desarrollado con 🤖 Vibe Coding**
