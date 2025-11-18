# ⚡ Comandos Rápidos - QuickTask

Referencia rápida de comandos útiles para trabajar con QuickTask.

---

## 🚀 Inicio Rápido

```powershell
# Opción 1: Script automático
.\run.ps1

# Opción 2: Docker
docker-compose up

# Opción 3: Manual
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

---

## 🐍 Python / Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar (PowerShell)
.\venv\Scripts\Activate.ps1

# Activar (CMD)
.\venv\Scripts\activate.bat

# Desactivar
deactivate

# Instalar dependencias
pip install -r requirements.txt

# Actualizar pip
python -m pip install --upgrade pip

# Ver paquetes instalados
pip list

# Congelar dependencias
pip freeze > requirements.txt
```

---

## 🧪 Testing

```powershell
# Ejecutar todos los tests
pytest

# Tests en modo verbose
pytest -v

# Test específico
pytest tests/test_tasks.py::test_create_task

# Con cobertura
pytest --cov=app

# Cobertura con reporte HTML
pytest --cov=app --cov-report=html

# Ver reporte de cobertura
.\htmlcov\index.html

# Tests con output
pytest -s

# Detener en primer fallo
pytest -x

# Re-ejecutar solo tests fallidos
pytest --lf
```

---

## 🚀 Ejecutar Aplicación

```powershell
# Desarrollo con hot-reload
uvicorn app.main:app --reload

# Especificar host y puerto
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Sin reload (producción)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Con logging
uvicorn app.main:app --reload --log-level debug

# Ejecutar como módulo
python -m uvicorn app.main:app --reload
```

---

## 🐳 Docker

```powershell
# Construir imagen
docker build -t quicktask .

# Ejecutar contenedor
docker run -p 8000:8000 quicktask

# Con volumen
docker run -p 8000:8000 -v ${PWD}/data:/app/data quicktask

# Docker Compose - Iniciar
docker-compose up

# Docker Compose - Background
docker-compose up -d

# Docker Compose - Rebuild
docker-compose up --build

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Ver contenedores
docker ps

# Entrar al contenedor
docker exec -it quicktask_api sh

# Ver logs de contenedor
docker logs quicktask_api
```

---

## 🌐 API Testing (curl)

```powershell
# Crear tarea
curl -X POST "http://localhost:8000/tasks" `
  -H "Content-Type: application/json" `
  -d '{"title": "Mi tarea", "description": "Descripción"}'

# Listar tareas
curl -X GET "http://localhost:8000/tasks"

# Obtener tarea específica
curl -X GET "http://localhost:8000/tasks/1"

# Actualizar tarea
curl -X PUT "http://localhost:8000/tasks/1" `
  -H "Content-Type: application/json" `
  -d '{"completed": true}'

# Eliminar tarea
curl -X DELETE "http://localhost:8000/tasks/1"

# Health check
curl -X GET "http://localhost:8000/health"

# Filtrar pendientes
curl -X GET "http://localhost:8000/tasks?completed=false"

# Paginación
curl -X GET "http://localhost:8000/tasks?skip=0&limit=10"
```

---

## 🔧 PowerShell (Invoke-RestMethod)

```powershell
# Crear tarea
$body = @{
    title = "Mi tarea"
    description = "Descripción"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Listar tareas
Invoke-RestMethod -Uri "http://localhost:8000/tasks"

# Obtener tarea
$id = 1
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$id"

# Actualizar tarea
$body = @{ completed = $true } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$id" `
    -Method PUT `
    -Body $body `
    -ContentType "application/json"

# Eliminar tarea
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$id" -Method DELETE

# Formatear salida
Invoke-RestMethod -Uri "http://localhost:8000/tasks" | Format-Table
```

---

## 📊 Base de Datos

```powershell
# SQLite CLI (si está instalado)
sqlite3 quicktask.db

# Ver tablas
.tables

# Ver estructura de tabla
.schema tasks

# Consultar datos
SELECT * FROM tasks;

# Salir
.quit

# Eliminar base de datos
Remove-Item quicktask.db
```

---

## 🔍 Linting y Formateo

```powershell
# Instalar herramientas
pip install black flake8 mypy isort

# Formatear código con Black
black app/ tests/

# Verificar formato
black --check app/ tests/

# Linting con flake8
flake8 app/ tests/

# Con configuración
flake8 app/ tests/ --max-line-length=100 --ignore=E501

# Type checking con mypy
mypy app/

# Ordenar imports con isort
isort app/ tests/

# Todo en uno
black app/ tests/ ; flake8 app/ tests/ ; mypy app/
```

---

## 📦 Dependencias

```powershell
# Ver dependencias desactualizadas
pip list --outdated

# Actualizar un paquete
pip install --upgrade fastapi

# Actualizar todos los paquetes (cuidado)
pip install --upgrade -r requirements.txt

# Ver dependencias de un paquete
pip show fastapi

# Desinstalar paquete
pip uninstall fastapi
```

---

## 🗂️ Git

```powershell
# Inicializar repo
git init

# Añadir archivos
git add .

# Commit
git commit -m "feat: descripción del cambio"

# Ver estado
git status

# Ver historial
git log --oneline

# Crear rama
git checkout -b feature/nueva-funcionalidad

# Cambiar de rama
git checkout main

# Merge
git merge feature/nueva-funcionalidad

# Push
git push origin main

# Pull
git pull origin main

# Ver cambios
git diff

# Descartar cambios
git checkout -- archivo.py
```

---

## 📝 Documentación

```powershell
# Ver documentación Swagger
Start-Process "http://localhost:8000/docs"

# Ver ReDoc
Start-Process "http://localhost:8000/redoc"

# Descargar OpenAPI spec
Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" `
    -OutFile "openapi.json"

# Generar docs con Sphinx (si está instalado)
sphinx-quickstart
sphinx-build -b html docs/ docs/_build/
```

---

## 🔍 Debugging

```powershell
# Ejecutar con debugger
python -m pdb app/main.py

# Ver logs de la aplicación
uvicorn app.main:app --reload --log-level debug

# Imprimir requests HTTP
$env:HTTPX_LOG_LEVEL="DEBUG"
pytest -s

# Ver variables de entorno
Get-ChildItem Env:

# Establecer variable de entorno
$env:DEBUG = "True"
```

---

## 📊 Monitoreo y Performance

```powershell
# Ver uso de CPU/RAM del contenedor
docker stats quicktask_api

# Benchmark con ApacheBench (si está instalado)
ab -n 1000 -c 10 http://localhost:8000/tasks

# Medir tiempo de respuesta
Measure-Command { Invoke-RestMethod "http://localhost:8000/tasks" }

# Ver procesos Python
Get-Process python
```

---

## 🧹 Limpieza

```powershell
# Limpiar cache de Python
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse

# Limpiar cache de pytest
Remove-Item -Recurse .pytest_cache

# Limpiar cobertura
Remove-Item -Recurse htmlcov/
Remove-Item .coverage

# Limpiar entorno virtual
Remove-Item -Recurse venv/

# Limpiar base de datos
Remove-Item quicktask.db

# Limpiar todo
Remove-Item -Recurse venv/, __pycache__, .pytest_cache, htmlcov/, *.db
```

---

## 🚀 Deployment

```powershell
# Tag de version
docker tag quicktask quicktask:v1.0.0

# Push a registry
docker push username/quicktask:v1.0.0

# Export/Import imagen
docker save quicktask > quicktask.tar
docker load < quicktask.tar

# Backup de base de datos
Copy-Item quicktask.db -Destination "backup_$(Get-Date -Format 'yyyyMMdd').db"
```

---

## 🔧 Troubleshooting

```powershell
# Puerto ocupado - Ver qué está usando el puerto 8000
netstat -ano | findstr :8000

# Matar proceso
taskkill /PID <PID> /F

# Verificar instalación de Python
python --version
pip --version

# Verificar instalación de Docker
docker --version
docker-compose --version

# Re-instalar dependencias
Remove-Item -Recurse venv/
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Reconstruir contenedor
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## 📚 Recursos

```powershell
# Abrir documentación en navegador
Start-Process "http://localhost:8000/docs"

# Abrir GitHub del proyecto
Start-Process "https://github.com/usuario/quicktask"

# Ver este archivo
Get-Content QUICK_COMMANDS.md | Select-String "keyword"
```

---

## 💡 Tips

```powershell
# Alias útiles (añadir a $PROFILE)
function dev { uvicorn app.main:app --reload }
function test { pytest -v }
function docker-up { docker-compose up }
function docker-down { docker-compose down }

# Para crear alias permanentes
notepad $PROFILE
# Añadir las funciones y reiniciar PowerShell
```

---

**⚡ Comandos más usados:**

```powershell
.\run.ps1                    # Iniciar app
.\test.ps1                   # Ejecutar tests
docker-compose up            # Docker
pytest -v                    # Tests detallados
uvicorn app.main:app --reload  # Dev server
```

---

**🔖 Guardar este archivo para referencia rápida!**
