# 💡 Ejemplos Prácticos de Uso - QuickTask

Esta guía contiene ejemplos detallados de uso de la API QuickTask.

## 📋 Tabla de Contenidos

1. [Operaciones Básicas](#operaciones-básicas)
2. [Casos de Uso Comunes](#casos-de-uso-comunes)
3. [Filtrado y Búsqueda](#filtrado-y-búsqueda)
4. [Manejo de Errores](#manejo-de-errores)
5. [Scripts de Automatización](#scripts-de-automatización)

---

## 🎯 Operaciones Básicas

### 1️⃣ Crear tu Primera Tarea

**PowerShell:**
```powershell
$body = @{
    title = "Aprender FastAPI"
    description = "Completar el tutorial de FastAPI en 2 horas"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**curl (PowerShell):**
```powershell
curl -X POST "http://localhost:8000/tasks" `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Aprender FastAPI",
    "description": "Completar el tutorial de FastAPI en 2 horas"
  }'
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "title": "Aprender FastAPI",
  "description": "Completar el tutorial de FastAPI en 2 horas",
  "completed": false
}
```

### 2️⃣ Listar Todas las Tareas

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method GET
```

**curl:**
```powershell
curl -X GET "http://localhost:8000/tasks"
```

### 3️⃣ Obtener una Tarea Específica

**PowerShell:**
```powershell
$taskId = 1
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId" -Method GET
```

### 4️⃣ Marcar Tarea como Completada

**PowerShell:**
```powershell
$taskId = 1
$body = @{ completed = $true } | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId" `
    -Method PUT `
    -Body $body `
    -ContentType "application/json"
```

### 5️⃣ Eliminar una Tarea

**PowerShell:**
```powershell
$taskId = 1
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId" -Method DELETE
```

---

## 🚀 Casos de Uso Comunes

### Escenario 1: Gestionar Tareas Diarias

```powershell
# 1. Crear lista de tareas del día
$tareasDia = @(
    @{ title = "Revisar emails"; description = "Inbox zero antes de las 10am" },
    @{ title = "Reunión de equipo"; description = "Daily standup a las 9:30am" },
    @{ title = "Desarrollar feature X"; description = "Completar el componente de login" }
)

foreach ($tarea in $tareasDia) {
    $body = $tarea | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
}

# 2. Ver todas las tareas pendientes
$pendientes = Invoke-RestMethod -Uri "http://localhost:8000/tasks?completed=false"
Write-Host "Tareas pendientes: $($pendientes.Count)"
$pendientes | Format-Table id, title, description

# 3. Completar una tarea
$taskId = 1
$body = @{ completed = $true } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId" `
    -Method PUT `
    -Body $body `
    -ContentType "application/json"

# 4. Ver progreso
$todas = Invoke-RestMethod -Uri "http://localhost:8000/tasks"
$completadas = ($todas | Where-Object { $_.completed }).Count
$progreso = [math]::Round(($completadas / $todas.Count) * 100, 2)
Write-Host "Progreso del día: $progreso% ($completadas/$($todas.Count))"
```

### Escenario 2: Actualización en Lote

```powershell
# Marcar todas las tareas como completadas
$tareas = Invoke-RestMethod -Uri "http://localhost:8000/tasks?completed=false"

foreach ($tarea in $tareas) {
    $body = @{ completed = $true } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($tarea.id)" `
        -Method PUT `
        -Body $body `
        -ContentType "application/json"
    Write-Host "✅ Tarea $($tarea.id) completada: $($tarea.title)"
}
```

### Escenario 3: Búsqueda y Filtrado

```powershell
# Buscar tareas por palabra clave (simulación client-side)
function Search-Tasks {
    param(
        [string]$Keyword
    )
    
    $allTasks = Invoke-RestMethod -Uri "http://localhost:8000/tasks"
    $results = $allTasks | Where-Object { 
        $_.title -like "*$Keyword*" -or $_.description -like "*$Keyword*" 
    }
    
    return $results
}

# Uso
$resultados = Search-Tasks -Keyword "FastAPI"
$resultados | Format-Table id, title, completed
```

---

## 🔍 Filtrado y Búsqueda

### Filtrar por Estado

**Solo pendientes:**
```powershell
curl -X GET "http://localhost:8000/tasks?completed=false"
```

**Solo completadas:**
```powershell
curl -X GET "http://localhost:8000/tasks?completed=true"
```

### Paginación

**Primeras 10 tareas:**
```powershell
curl -X GET "http://localhost:8000/tasks?skip=0&limit=10"
```

**Siguientes 10 tareas:**
```powershell
curl -X GET "http://localhost:8000/tasks?skip=10&limit=10"
```

### Combinación de Filtros

**Primeras 5 tareas completadas:**
```powershell
curl -X GET "http://localhost:8000/tasks?completed=true&skip=0&limit=5"
```

---

## ⚠️ Manejo de Errores

### Error 404: Tarea No Encontrada

```powershell
try {
    $tarea = Invoke-RestMethod -Uri "http://localhost:8000/tasks/9999" -Method GET
} catch {
    $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "❌ Error: $($errorDetails.detail)" -ForegroundColor Red
}
```

**Respuesta:**
```json
{
  "detail": "Tarea con ID 9999 no encontrada"
}
```

### Error 422: Validación Fallida

```powershell
# Intentar crear tarea sin título (campo obligatorio)
$body = @{ description = "Solo descripción" } | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
} catch {
    Write-Host "❌ Validación fallida: Título es obligatorio" -ForegroundColor Red
}
```

---

## 🤖 Scripts de Automatización

### Script 1: Backup de Tareas

```powershell
# backup-tasks.ps1
$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_tasks_$fecha.json"

$tareas = Invoke-RestMethod -Uri "http://localhost:8000/tasks"
$tareas | ConvertTo-Json -Depth 10 | Out-File -FilePath $backupFile

Write-Host "✅ Backup guardado en: $backupFile"
Write-Host "📊 Total de tareas: $($tareas.Count)"
```

### Script 2: Restaurar Tareas

```powershell
# restore-tasks.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$BackupFile
)

if (-Not (Test-Path $BackupFile)) {
    Write-Host "❌ Archivo no encontrado: $BackupFile" -ForegroundColor Red
    exit 1
}

$tareas = Get-Content $BackupFile | ConvertFrom-Json

foreach ($tarea in $tareas) {
    $body = @{
        title = $tarea.title
        description = $tarea.description
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" | Out-Null
    
    Write-Host "✅ Restaurada: $($tarea.title)"
}

Write-Host "🎉 Restauración completada: $($tareas.Count) tareas"
```

### Script 3: Reporte Diario

```powershell
# daily-report.ps1
$tareas = Invoke-RestMethod -Uri "http://localhost:8000/tasks"
$completadas = ($tareas | Where-Object { $_.completed }).Count
$pendientes = ($tareas | Where-Object { -not $_.completed }).Count
$progreso = if ($tareas.Count -gt 0) { 
    [math]::Round(($completadas / $tareas.Count) * 100, 2) 
} else { 0 }

Write-Host "`n📊 REPORTE DIARIO DE TAREAS" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📝 Total de tareas: $($tareas.Count)"
Write-Host "✅ Completadas: $completadas"
Write-Host "⏳ Pendientes: $pendientes"
Write-Host "📈 Progreso: $progreso%"
Write-Host "================================`n" -ForegroundColor Cyan

if ($pendientes -gt 0) {
    Write-Host "⏳ TAREAS PENDIENTES:" -ForegroundColor Yellow
    $tareas | Where-Object { -not $_.completed } | ForEach-Object {
        Write-Host "  [$($_.id)] $($_.title)"
    }
}
```

### Script 4: Limpieza Semanal

```powershell
# weekly-cleanup.ps1
Write-Host "🧹 Limpiando tareas completadas..." -ForegroundColor Yellow

$completadas = Invoke-RestMethod -Uri "http://localhost:8000/tasks?completed=true"

Write-Host "Encontradas $($completadas.Count) tareas completadas"
$confirmacion = Read-Host "¿Eliminar todas? (S/N)"

if ($confirmacion -eq "S") {
    foreach ($tarea in $completadas) {
        Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($tarea.id)" `
            -Method DELETE | Out-Null
        Write-Host "  ✅ Eliminada: $($tarea.title)"
    }
    Write-Host "`n🎉 Limpieza completada!" -ForegroundColor Green
} else {
    Write-Host "❌ Operación cancelada" -ForegroundColor Red
}
```

---

## 🧪 Testing con PowerShell

### Test de Integración Completo

```powershell
# integration-test.ps1
Write-Host "🧪 Ejecutando tests de integración..." -ForegroundColor Cyan

# Test 1: Crear tarea
Write-Host "`n1️⃣ Test: Crear tarea..."
$body = @{
    title = "Test Task"
    description = "Testing description"
} | ConvertTo-Json

$created = Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

if ($created.id -and $created.title -eq "Test Task") {
    Write-Host "✅ PASS: Tarea creada correctamente (ID: $($created.id))" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Error al crear tarea" -ForegroundColor Red
    exit 1
}

# Test 2: Obtener tarea
Write-Host "`n2️⃣ Test: Obtener tarea..."
$retrieved = Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($created.id)"

if ($retrieved.id -eq $created.id) {
    Write-Host "✅ PASS: Tarea obtenida correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Error al obtener tarea" -ForegroundColor Red
    exit 1
}

# Test 3: Actualizar tarea
Write-Host "`n3️⃣ Test: Actualizar tarea..."
$updateBody = @{ completed = $true } | ConvertTo-Json
$updated = Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($created.id)" `
    -Method PUT `
    -Body $updateBody `
    -ContentType "application/json"

if ($updated.completed -eq $true) {
    Write-Host "✅ PASS: Tarea actualizada correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ FAIL: Error al actualizar tarea" -ForegroundColor Red
    exit 1
}

# Test 4: Eliminar tarea
Write-Host "`n4️⃣ Test: Eliminar tarea..."
Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($created.id)" -Method DELETE

try {
    Invoke-RestMethod -Uri "http://localhost:8000/tasks/$($created.id)"
    Write-Host "❌ FAIL: La tarea no fue eliminada" -ForegroundColor Red
    exit 1
} catch {
    Write-Host "✅ PASS: Tarea eliminada correctamente" -ForegroundColor Green
}

Write-Host "`n🎉 Todos los tests pasaron exitosamente!" -ForegroundColor Green
```

---

## 📚 Recursos Adicionales

### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Colecciones Postman
Para importar en Postman, usa la siguiente URL de OpenAPI:
```
http://localhost:8000/openapi.json
```

---

**💡 Tip**: Guarda estos scripts en una carpeta `scripts/` dentro del proyecto para fácil acceso.

**🚀 Happy Coding con QuickTask!**
