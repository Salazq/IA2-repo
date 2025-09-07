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

**Estructura:** ¿El JSON del prompt simple tiene una estructura lógica y predecible?

- El JSON del prompt simple tiene una estructura lógica, pero mezcla conceptos en el mismo nivel. El del prompt avanzado, en cambio, organiza la información de forma jerarquica, lo que lo hace más predecible 

**Precisión:** ¿Los tipos de datos son correctos (números vs. strings)?
- En el simple algunos valores como hora y presupuesto pueden quedar como string. En el avanzado se normalizan a tipos correctos.
  
**Parseabilidad:** ¿El JSON generado por el prompt avanzado es directamente utilizable por una aplicación sin necesidad de limpieza o conversión?

- El prompt avanzado, al seguir un esquema normalizado, puede integrarse sin necesidad de transformaciones adicionales.


**Manejo de Nulos:** ¿Cómo manejaría cada uno un texto donde, por ejemplo, el presupuesto no se menciona?

- En el simple, los campos no mencionados desaparecen. El avanzado, define que los campos faltantes como null, garantizando que la estructura se mantenga uniforme.


## Ejercicio 3

### 3.A: Prompt Simple


```

Un **agujero negro** es uno de los objetos más enigmáticos y extremos del universo. Se forma cuando una gran cantidad de materia queda concentrada en un espacio muy pequeño, generando una gravedad tan intensa que nada puede escapar de ella, ni siquiera la luz.

### Formación

La mayoría de los agujeros negros se originan cuando una estrella masiva (mucho más grande que el Sol) agota su combustible nuclear. Al no poder sostenerse por la presión de las reacciones en su núcleo, la gravedad provoca que la estrella colapse sobre sí misma. Si la masa restante supera un cierto límite, se forma un agujero negro.

### Partes principales

* **Horizonte de sucesos:** es el “punto de no retorno”. Cualquier cosa que cruce esta frontera queda atrapada para siempre.
* **Singularidad:** el centro del agujero negro, donde la densidad teórica es infinita y las leyes de la física tal como las conocemos dejan de aplicarse.
* **Disco de acreción:** materia (gas, polvo, estrellas) que gira alrededor del agujero negro antes de ser absorbida. Este disco se calienta y emite enormes cantidades de energía, en ocasiones visible desde la Tierra.

### Tipos de agujeros negros

1. **De masa estelar:** resultado del colapso de estrellas masivas.
2. **Supermasivos:** se encuentran en el centro de la mayoría de las galaxias, incluyendo la Vía Láctea. Pueden tener millones o miles de millones de veces la masa del Sol.
3. **Intermedios:** más grandes que los estelares, pero más pequeños que los supermasivos; son los más difíciles de detectar.
4. **Primordiales:** hipotéticos agujeros negros muy pequeños que podrían haberse formado en los primeros instantes del universo.

### Importancia científica

Los agujeros negros no solo son fascinantes por su fuerza gravitatoria, sino también porque nos ayudan a entender la relatividad de Einstein, la naturaleza del espacio-tiempo y el comportamiento de la materia en condiciones extremas. Además, los avances en su observación —como la famosa primera “foto” del agujero negro en la galaxia M87 en 2019— nos muestran que, aunque no podamos verlos directamente, su influencia en el cosmos es inmensa.

¿Quieres que te lo escriba con un tono más **divulgativo y sencillo** (como para un público general), o más **técnico y científico** (con fórmulas y teorías)?

```


### 3.B: Prompt Avanzado

```
Imagina en el espacio un lugar tan poderoso que nada puede escapar de él, ni siquiera la luz: eso es un agujero negro. Es como un aspirador cósmico invisible que traga todo lo que se acerque demasiado. Los astrónomos no lo ven directamente, pero saben que está allí porque las estrellas cercanas giran a su alrededor como si bailaran alrededor de un compañero invisible. Los agujeros negros son misteriosos portales del universo, recordándonos que el cosmos guarda secretos tan enormes y fascinantes que aún estamos aprendiendo a descifrarlos.
```

### 3.C: Evaluación Comparativa

**Adecuación a la Audiencia:** ¿Qué respuesta es más apropiada y comprensible para un niño?
- El prompt avanzado es más apropiado para un niño, porque explica los agujeros negros con ejemplos sencillos, mientras que el simple usa palabras técnicas que podrían ser confusas.


**Tono:** ¿Logró el prompt simple capturar el tono de asombro solicitado?
- El prompt avanzado captura mejor el asombro solicitado, ya que lo cuenta como una historia. El prompt simple lo dice de  pero de una forma más seria.


**Creatividad:** ¿Qué respuesta es más original y memorable?
- El prompt avanzado es más memorable, ya que utiliza metáforas e ideas que captan la atención. El simple se centra más en dar datos y definiciones.


**Cumplimiento de Restricciones:** ¿El prompt avanzado logró evitar la jerga técnica como se le pidió?

- Sí, El prompt avanzado cumple la regla de no usar jerga técnica. El simple introduce términos que son más difíciles de entender.




