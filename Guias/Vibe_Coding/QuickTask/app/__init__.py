"""
📁 __init__.py
Inicializa el paquete app y expone los componentes principales.
"""

from .database import Base, engine, get_db
from .models import Task
from . import schemas, crud

__all__ = ["Base", "engine", "get_db", "Task", "schemas", "crud"]
