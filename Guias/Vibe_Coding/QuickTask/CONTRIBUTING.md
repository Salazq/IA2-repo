# 🤝 Guía de Contribución - QuickTask

## 🌟 Metodología Vibe Coding

Este proyecto sigue la metodología **Vibe Coding**, que promueve la colaboración creativa entre humanos e IA para producir código de alta calidad.

### Principios Fundamentales

1. **Intención Clara**: El humano define objetivos y contexto
2. **Colaboración Activa**: La IA genera, el humano valida
3. **Iteración Rápida**: Ciclos cortos de feedback
4. **Calidad Primero**: Código limpio, documentado y testeado

---

## 🚀 Cómo Contribuir

### 1. Configurar Entorno de Desarrollo

```powershell
# Clonar el repositorio
git clone <repository-url>
cd QuickTask

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install black flake8 mypy pre-commit
```

### 2. Crear una Rama

```powershell
git checkout -b feature/nombre-descriptivo
# o
git checkout -b bugfix/descripcion-del-bug
```

### 3. Hacer Cambios

- Escribe código limpio y documentado
- Añade tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 4. Ejecutar Tests

```powershell
# Tests unitarios
pytest -v

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_tasks.py::test_create_task -v
```

### 5. Verificar Calidad del Código

```powershell
# Formatear código con Black
black app/ tests/

# Verificar estilo con flake8
flake8 app/ tests/ --max-line-length=100

# Verificar tipos con mypy
mypy app/
```

### 6. Commit y Push

```powershell
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/nombre-descriptivo
```

### 7. Crear Pull Request

- Describe claramente los cambios
- Referencia issues relacionados
- Asegúrate de que los tests pasen
- Solicita revisión

---

## 📝 Estándares de Código

### Estilo Python

Seguimos **PEP 8** con algunas adaptaciones:

```python
# ✅ CORRECTO

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """
    Crea una nueva tarea en la base de datos.
    
    Args:
        db: Sesión de base de datos
        task: Datos de la tarea a crear
    
    Returns:
        La tarea creada con su ID asignado
    """
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# ❌ INCORRECTO (sin tipado, sin docstring)

def create_task(db, task):
    db_task = models.Task(title=task.title, description=task.description, completed=False)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
```

### Nomenclatura

```python
# Variables y funciones: snake_case
user_name = "John"
def get_user_by_id(user_id: int):
    pass

# Clases: PascalCase
class TaskManager:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_TASKS_PER_PAGE = 100
DATABASE_URL = "sqlite:///./app.db"

# Variables privadas: _prefijo
_internal_cache = {}
```

### Docstrings

Usamos el formato **Google Style**:

```python
def update_task(
    db: Session, 
    task_id: int, 
    task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    """
    Actualiza una tarea existente.
    
    Solo actualiza los campos que se proporcionan (actualización parcial).
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a actualizar
        task_update: Nuevos datos de la tarea
    
    Returns:
        La tarea actualizada si existe, None en caso contrario
    
    Example:
        >>> update_data = TaskUpdate(completed=True)
        >>> task = update_task(db, 1, update_data)
        >>> task.completed
        True
    """
    # Implementación...
```

---

## 🧪 Guía de Testing

### Estructura de Tests

```python
def test_nombre_descriptivo():
    """Test que describe claramente lo que se prueba"""
    # Arrange (Preparar)
    task_data = {"title": "Test Task", "description": "Test"}
    
    # Act (Actuar)
    response = client.post("/tasks", json=task_data)
    
    # Assert (Afirmar)
    assert response.status_code == 201
    assert response.json()["title"] == task_data["title"]
```

### Cobertura Mínima

- **Líneas**: 80% mínimo
- **Funciones críticas**: 100%
- **Endpoints**: Todos deben tener tests

### Casos a Probar

```python
# ✅ Casos exitosos
def test_create_task_success():
    pass

# ✅ Casos de error
def test_create_task_missing_title():
    pass

# ✅ Casos límite
def test_create_task_max_length_title():
    pass

# ✅ Casos especiales
def test_create_task_with_special_characters():
    pass
```

---

## 🎯 Tipos de Commits

Seguimos **Conventional Commits**:

```bash
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: formateo, sin cambios de lógica
refactor: refactorización de código
test: añadir o modificar tests
chore: mantenimiento, dependencias
perf: mejoras de rendimiento
```

### Ejemplos

```bash
feat: agregar endpoint para buscar tareas por título
fix: corregir validación de campo description
docs: actualizar README con ejemplos de Docker
test: agregar tests para filtrado por estado
refactor: simplificar lógica de update_task
```

---

## 🏗️ Arquitectura y Patrones

### Capas de la Aplicación

```
Presentación (main.py)
    ↓
Validación (schemas.py)
    ↓
Lógica de Negocio (crud.py)
    ↓
Acceso a Datos (models.py + database.py)
```

### Principios SOLID

#### Single Responsibility (S)
```python
# ✅ Cada función tiene una responsabilidad
def get_task(db: Session, task_id: int):
    """Solo obtiene una tarea"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# ❌ Múltiples responsabilidades
def get_and_validate_and_log_task(db, task_id):
    # Obtiene, valida Y registra log
    pass
```

#### Open/Closed (O)
```python
# ✅ Abierto a extensión, cerrado a modificación
class TaskFilter:
    def filter(self, query, **kwargs):
        if 'completed' in kwargs:
            query = query.filter(Task.completed == kwargs['completed'])
        return query
```

#### Dependency Injection (D)
```python
# ✅ Dependencias inyectadas
@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)
```

---

## 📊 Checklist para Pull Request

Antes de enviar un PR, verifica:

- [ ] El código sigue los estándares de estilo
- [ ] Todos los tests pasan (`pytest`)
- [ ] La cobertura de tests es adecuada
- [ ] El código está documentado
- [ ] No hay errores de linting (`flake8`)
- [ ] El tipado es correcto (`mypy`)
- [ ] La documentación está actualizada
- [ ] Los commits siguen el formato convencional
- [ ] El PR tiene una descripción clara
- [ ] Se han probado los cambios localmente

---

## 🐛 Reportar Bugs

### Template de Issue

```markdown
**Descripción del Bug**
Descripción clara y concisa del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer click en '...'
3. Ver error

**Comportamiento Esperado**
Qué debería pasar.

**Comportamiento Actual**
Qué pasa actualmente.

**Screenshots**
Si aplica, añadir capturas.

**Entorno**
- OS: [Windows 11, macOS, Linux]
- Python: [3.11.x]
- FastAPI: [0.109.0]

**Contexto Adicional**
Cualquier información relevante.
```

---

## 💡 Proponer Nuevas Features

### Template de Feature Request

```markdown
**Descripción de la Feature**
Descripción clara de la funcionalidad propuesta.

**Motivación**
¿Por qué es necesaria? ¿Qué problema resuelve?

**Solución Propuesta**
Cómo podría implementarse.

**Alternativas Consideradas**
Otras formas de resolver el problema.

**Impacto**
- Breaking changes: Sí/No
- Afecta a: API, Database, Tests, Docs
- Complejidad estimada: Baja/Media/Alta
```

---

## 🎓 Recursos para Aprender

### FastAPI
- [Documentación Oficial](https://fastapi.tiangolo.com/)
- [Tutorial Completo](https://fastapi.tiangolo.com/tutorial/)

### SQLAlchemy
- [Documentación](https://docs.sqlalchemy.org/)
- [ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

### Testing
- [Pytest Docs](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)

---

## 🤖 Vibe Coding en Práctica

### Workflow Recomendado

1. **Definir Intención**
   ```
   "Necesito un endpoint para buscar tareas por título"
   ```

2. **Colaborar con IA**
   ```
   IA genera código base → Humano revisa → IA ajusta
   ```

3. **Validar y Testear**
   ```
   Ejecutar tests → Verificar funcionamiento → Iterar
   ```

4. **Documentar**
   ```
   Añadir docstrings → Actualizar README → Ejemplos
   ```

5. **Refinar**
   ```
   Code review → Optimizar → Limpiar
   ```

---

## 📞 Contacto y Comunidad

- **Issues**: Para bugs y features
- **Discussions**: Para preguntas y ideas
- **Pull Requests**: Para contribuciones de código

---

## 🙏 Agradecimientos

Gracias por contribuir a QuickTask y por seguir la metodología Vibe Coding. Tu colaboración hace que este proyecto sea mejor cada día.

**¡Happy Coding! 🚀**
