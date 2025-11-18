"""
📁 crud.py
Operaciones CRUD (Create, Read, Update, Delete) para las tareas.
Contiene la lógica de negocio para interactuar con la base de datos.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


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


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """
    Obtiene una tarea específica por su ID.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a buscar
    
    Returns:
        La tarea si existe, None en caso contrario
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    completed: Optional[bool] = None
) -> List[models.Task]:
    """
    Obtiene una lista de tareas con paginación opcional.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (para paginación)
        limit: Número máximo de registros a devolver
        completed: Filtro opcional por estado (True/False/None)
    
    Returns:
        Lista de tareas
    """
    query = db.query(models.Task)
    
    # Filtrar por estado si se especifica
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    return query.offset(skip).limit(limit).all()


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
    """
    db_task = get_task(db, task_id)
    
    if db_task is None:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Elimina una tarea de la base de datos.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a eliminar
    
    Returns:
        True si la tarea fue eliminada, False si no existía
    """
    db_task = get_task(db, task_id)
    
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    return True
