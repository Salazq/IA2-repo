"""
📁 schemas.py
Esquemas de validación usando Pydantic.
Define los modelos de datos para requests y responses de la API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    """
    Esquema base con los campos comunes de una tarea.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada (opcional)")
    completed: bool = Field(default=False, description="Estado de la tarea")


class TaskCreate(BaseModel):
    """
    Esquema para crear una nueva tarea.
    No incluye el ID ya que se genera automáticamente.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada (opcional)")


class TaskUpdate(BaseModel):
    """
    Esquema para actualizar una tarea existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Nuevo título")
    description: Optional[str] = Field(None, max_length=1000, description="Nueva descripción")
    completed: Optional[bool] = Field(None, description="Nuevo estado")


class TaskResponse(TaskBase):
    """
    Esquema de respuesta que incluye todos los campos, incluyendo el ID.
    Se usa para devolver tareas desde la API.
    """
    id: int = Field(..., description="ID único de la tarea")

    class Config:
        """Configuración para permitir la conversión desde modelos ORM"""
        from_attributes = True  # Anteriormente orm_mode = True en Pydantic v1
