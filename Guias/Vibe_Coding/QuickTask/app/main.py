"""
📁 main.py
Aplicación principal de FastAPI.
Define los endpoints REST y la configuración de la aplicación QuickTask.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import engine, get_db, Base
from . import crud, schemas

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="QuickTask API",
    description="API REST minimalista para gestión de tareas personales",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz de bienvenida.
    """
    return {
        "message": "Bienvenido a QuickTask API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Crear una nueva tarea"
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva tarea en el sistema.
    
    - **title**: Título de la tarea (obligatorio)
    - **description**: Descripción detallada (opcional)
    """
    return crud.create_task(db=db, task=task)


@app.get(
    "/tasks",
    response_model=List[schemas.TaskResponse],
    tags=["Tasks"],
    summary="Listar todas las tareas"
)
def read_tasks(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    completed: Optional[bool] = Query(None, description="Filtrar por estado (true/false)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de tareas con opciones de paginación y filtrado.
    
    - **skip**: Saltar N primeros registros (paginación)
    - **limit**: Limitar resultados a N registros
    - **completed**: Filtrar por estado completado (opcional)
    """
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit, completed=completed)
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    tags=["Tasks"],
    summary="Obtener una tarea específica"
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una tarea específica por su ID.
    
    - **task_id**: ID único de la tarea
    """
    db_task = crud.get_task(db=db, task_id=task_id)
    
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    return db_task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    tags=["Tasks"],
    summary="Actualizar una tarea"
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una tarea existente.
    Solo se actualizan los campos proporcionados.
    
    - **task_id**: ID de la tarea a actualizar
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **completed**: Nuevo estado (opcional)
    """
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task)
    
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    return db_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Eliminar una tarea"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una tarea del sistema.
    
    - **task_id**: ID de la tarea a eliminar
    """
    success = crud.delete_task(db=db, task_id=task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    return None


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de verificación de salud de la aplicación.
    """
    return {"status": "healthy", "service": "QuickTask API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
