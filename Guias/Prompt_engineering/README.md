# Desarrollo de la guía de Prompt Engineering


## Ejercicio 1

### 1.A: Prompt Simple


```python
import re

def validar_contrasena(password: str) -> bool:
    """
    Valida una contraseña con las siguientes reglas:
    1. Longitud mínima de 8 caracteres
    2. Debe tener al menos una letra mayúscula
    3. Debe tener al menos una letra minúscula
    4. Debe tener al menos un número
    5. Debe tener al menos un carácter especial (@$!%*?&)

    Retorna True si cumple todas las condiciones, False en caso contrario.
    """
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):  # al menos una mayúscula
        return False

    if not re.search(r"[a-z]", password):  # al menos una minúscula
        return False

    if not re.search(r"[0-9]", password):  # al menos un número
        return False

    if not re.search(r"[@$!%*?&]", password):  # al menos un caracter especial
        return False

    return True


# Ejemplos de uso:
print(validar_contrasena("Hola123!"))   # ✅ True
print(validar_contrasena("hola123"))    # ❌ False
print(validar_contrasena("HOLA@123"))   # ✅ True

```


### 1.B: Prompt Avanzado

```python
def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si una contraseña cumple con los criterios de seguridad definidos.

    Reglas de validación:
    1. Longitud mínima de 12 caracteres.
    2. Debe contener al menos una letra mayúscula (A-Z).
    3. Debe contener al menos una letra minúscula (a-z).
    4. Debe contener al menos un número (0-9).
    5. Debe contener al menos un carácter especial (@, #, $, %, &, !).

    Parámetros
    ----------
    contrasena : str
        La contraseña a validar.

    Retorna
    -------
    bool
        True si la contraseña cumple todas las reglas,
        False en caso contrario.
    """
    if len(contrasena) < 12:
        return False

    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    caracteres_especiales = "@#$%&!"
    tiene_especial = any(c in caracteres_especiales for c in contrasena)

    return all([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])


# Ejemplos de uso
print(validar_contrasena("Segura123!@#"))   # ✅ Válida (True)
print(validar_contrasena("segura123456"))   # ❌ Inválida: falta mayúscula y especial (False)
print(validar_contrasena("Corta1!"))        # ❌ Inválida: longitud insuficiente (False)

```

### 1.C: Evaluación Comparativa


Completitud: ¿La función del prompt simple incluyó todas las reglas?

- Simple: cumple con reglas básicas de validación de contraseñas, pero usa una longitud mínima que no coincide con lo que se pide en el  más estricto prompt avanzado.
- Avanzado: incluye todas las reglas especificada (longitud mínima de 12, mayúscula, minúscula, número y carácter especial).

Claridad: ¿El código está bien documentado? ¿Es fácil de entender?

- Simple: tiene comentarios y es entendible, pero no incluye docstring ni explicación de parámetros y retorno.
- Avanzado: inluye el  docstrings (explica parámetros y retorno), lo que mejora la comprensión.
  
Utilidad: ¿El prompt avanzado proporcionó ejemplos de uso que facilitan la prueba y la integración?

- Simple: incluye ejemplos básicos de uso con print.
- Avanzado: muestra un caso válido y dos casos inválidos, esto facilita pruebas y demuestra distintos fallos.

Robustez: ¿La función maneja casos borde que el prompt simple podría haber ignorado?


- Simple: Puede fallar en casos límite como contraseñas justo en la longitud mínima o que cumplen parcialmente las reglas.
- Avanzado: Exige 12 caracteres y valida explícitamente cada regla, evitando ambigüedades.


## Ejercicio 2

### 2.A: Prompt Simple


```python

{
  "evento": "Reunión de lanzamiento",
  "proyecto": "Proyecto Fénix",
  "fecha": "2024-10-15",
  "hora": "10:30 AM",
  "lugar": "Sala Júpiter",
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ],
  "presupuesto": {
    "monto": 25000,
    "moneda": "USD"
  }
}

```


### 2.B: Prompt Avanzado

```python
{
  "proyecto": {
    "nombre": "Proyecto Fénix",
    "presupuesto": {
      "monto": 25000,
      "moneda": "USD"
    }
  },
  "reunion": {
    "fecha": "2024-10-15",
    "hora": "10:30",
    "ubicacion": "Sala Júpiter"
  },
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ]
}

```

### 2.C: Evaluación Comparativa


