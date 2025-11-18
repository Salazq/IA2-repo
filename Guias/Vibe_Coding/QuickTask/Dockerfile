# 🐳 Dockerfile para QuickTask
# Multi-stage build para optimizar el tamaño de la imagen

FROM python:3.11-slim as builder

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --user -r requirements.txt

# ===== Imagen final =====
FROM python:3.11-slim

# Crear usuario no-root para mayor seguridad
RUN useradd -m -u 1000 appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder
COPY --from=builder /root/.local /home/appuser/.local

# Crear directorio para base de datos con permisos correctos
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Copiar código de la aplicación
COPY --chown=appuser:appuser ./app ./app

# Asegurar que los scripts en .local están en el PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
