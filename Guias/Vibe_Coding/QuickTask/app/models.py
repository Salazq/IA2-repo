"""
📁 models.py
Modelos ORM de la base de datos usando SQLAlchemy.
Define la estructura de la tabla Task en la base de datos.
"""

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Task(Base):
    """
    Modelo ORM para la tabla de tareas.
    
    Atributos:
        id: Identificador único de la tarea (clave primaria)
        title: Título de la tarea (obligatorio)
        description: Descripción detallada de la tarea (opcional)
        completed: Estado de la tarea (pendiente=False / completada=True)
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """Representación en string del modelo Task"""
        status = "completada" if self.completed else "pendiente"
        return f"<Task(id={self.id}, title='{self.title}', status={status})>"
