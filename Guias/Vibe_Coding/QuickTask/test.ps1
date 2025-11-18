# 🧪 Script para ejecutar tests
# Ejecuta: .\test.ps1

Write-Host "🧪 Ejecutando pruebas de QuickTask..." -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual si existe
if (Test-Path "venv") {
    Write-Host "✨ Activando entorno virtual..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

# Ejecutar tests con pytest
Write-Host "🔍 Ejecutando tests..." -ForegroundColor Green
pytest -v --cov=app --cov-report=term-missing

Write-Host ""
Write-Host "✅ Tests completados!" -ForegroundColor Green
