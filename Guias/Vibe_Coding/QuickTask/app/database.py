"""
📁 database.py
Configuración de la base de datos SQLite con SQLAlchemy.
Gestiona la conexión y las sesiones de base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión para SQLite
# El archivo de base de datos se creará en /app/data para Docker
import os

# Crear directorio data si no existe
os.makedirs("/app/data", exist_ok=True) if os.path.exists("/app") else None

# Usar /app/data en Docker, o directorio actual en desarrollo local
if os.path.exists("/app/data"):
    SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/quicktask.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./quicktask.db"

# Crear el motor de base de datos
# check_same_thread=False es necesario para SQLite con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependencia que proporciona una sesión de base de datos.
    Se utiliza en las rutas de FastAPI para inyección de dependencias.
    Asegura que la sesión se cierre después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
