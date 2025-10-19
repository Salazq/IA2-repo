# 🚀 Script de inicio rápido para QuickTask
# Ejecuta: .\run.ps1

Write-Host "🚀 Iniciando QuickTask..." -ForegroundColor Green
Write-Host ""

# Verificar si el entorno virtual existe
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Activar entorno virtual
Write-Host "✨ Activando entorno virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "📥 Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# Ejecutar aplicación
Write-Host ""
Write-Host "🎉 Iniciando servidor..." -ForegroundColor Green
Write-Host "📚 Documentación: http://localhost:8000/docs" -ForegroundColor Magenta
Write-Host "🌐 API: http://localhost:8000" -ForegroundColor Magenta
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
