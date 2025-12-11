# Proyecto Final - Probabilidad y Estadística

Este repositorio contiene el desarrollo del proyecto final para la asignatura de Probabilidad y Estadística de la Universidad Distrital Francisco José de Caldas.

## Tema

El proyecto se centra en la **Prueba de rangos con signo de Wilcoxon para un experimento de observaciones pareadas**. El objetivo es implementar un algoritmo en Python para esta prueba, aplicable tanto a muestras pequeñas como a muestras grandes, basándose en la teoría de la sección 15.4 y 15.5 del texto "Estadística Matemática con aplicaciones" de Wackerly, Mendenhall y Scheaffer.

## Archivos del Proyecto

### Código Python

El proyecto incluye dos versiones del algoritmo de Wilcoxon:

#### 1. `wilcoxon_interactivo.py` - Versión Interactiva

**Cuándo usar**: Para explorar el algoritmo de forma interactiva, ingresando tus propios datos o probando los ejemplos incluidos.

**Características**:
- Menú interactivo con `input()` para navegación
- Permite ingresar datos personalizados
- Incluye 3 ejemplos precargados (n=10, n=27, n=35)
- Selección manual entre tabla exacta y aproximación normal (para 26 ≤ n ≤ 30)
- Ideal para sesiones de clase o aprendizaje individual

**Cómo ejecutar**:
```bash
python3 wilcoxon_interactivo.py
```

Luego sigue las instrucciones del menú para:
1. Ingresar tus propios datos
2. Ejecutar uno de los ejemplos precargados
3. Salir del programa

#### 2. `wilcoxon_colab.py` - Versión para Google Colab

**Cuándo usar**: Para ejecutar múltiples pruebas automáticamente, especialmente en Google Colab o Jupyter Notebooks.

**Características**:
- **No requiere `input()`** - Ejecución completamente automática
- Ejecuta 4 casos de prueba al correr el script:
  - **Ejemplo 15.8** del libro de Wackerly et al. (2008) - Programa de lectura
  - **Muestra pequeña** (n=10) con tabla exacta
  - **Muestra grande** (n=35) con aproximación normal
  - **Caso con empates** y diferencias cero
- Parámetros configurables (`nombre_muestra1`, `nombre_muestra2`)
- Verificación automática: T+ + T- = n(n+1)/2
- Resumen final de todas las pruebas ejecutadas

**Cómo ejecutar en Google Colab**:

1. Sube el archivo `wilcoxon_colab.py` a tu sesión de Colab o clona este repositorio:
   ```python
   !git clone https://github.com/slmorenog-ud/PruebaDeWilcoxon.git
   %cd PruebaDeWilcoxon
   ```

2. Ejecuta el script:
   ```python
   !python wilcoxon_colab.py
   ```

**Cómo ejecutar localmente**:
```bash
python3 wilcoxon_colab.py
```

**Personalizar las pruebas**:

Puedes modificar los casos de prueba en la función `ejecutar_pruebas_automaticas()` o usar directamente la función `test_wilcoxon()`:

```python
from wilcoxon_colab import test_wilcoxon

# Tus datos
muestra1 = [5, 7, 9, 11, 13]
muestra2 = [6, 8, 10, 12, 14]

# Ejecutar test
test_wilcoxon(
    muestra1, muestra2,
    nombre_muestra1="Antes",
    nombre_muestra2="Después",
    usar_aproximacion_normal=False
)
```

### Documentación

- **`README.md`**: Este archivo, con la descripción general del proyecto e instrucciones
- **`Secciones 15.4 - 15.5.pdf`**: Secciones del libro de referencia (Wackerly et al.)
- **`/latex_src`**: Contiene el archivo fuente `.tex` del ensayo argumentativo, junto con la bibliografía y otros recursos necesarios para la compilación del documento

### Archivo Legacy

- **`code`**: Versión original del código (conservado como respaldo)

## Metodología Implementada

Ambas versiones implementan la Prueba de Rangos con Signo de Wilcoxon siguiendo estos pasos:

1. **Calcular diferencias** entre pares de observaciones
2. **Eliminar diferencias cero** del análisis
3. **Asignar rangos** a valores absolutos (manejando empates con rango promedio)
4. **Aplicar signos** originales a los rangos
5. **Calcular T+ y T-** (sumas de rangos positivos y negativos)
6. **Seleccionar método estadístico**:
   - n ≤ 25: Tabla exacta de Wilcoxon
   - 26 ≤ n ≤ 30: Usuario decide (solo versión interactiva) o tabla exacta (versión Colab)
   - n > 30: Aproximación por distribución normal
7. **Decisión estadística** basada en nivel de significancia α=0.05 (dos colas)

## Requisitos

- Python 3.x
- Biblioteca estándar de Python (no se requieren dependencias externas)
- Para Google Colab: Conexión a internet y cuenta de Google

## Estructura del Proyecto

```
/
├── README.md                    # Este archivo
├── wilcoxon_interactivo.py     # Versión interactiva con menú
├── wilcoxon_colab.py           # Versión automatizada para Colab
├── code                        # Versión original (legacy)
├── Secciones 15.4 - 15.5.pdf  # Teoría del libro de referencia
└── latex_src/                  # Fuentes LaTeX del ensayo
```

## Integrantes - Turno #10

- **Álvarez Ortiz Arley Santiago** - 20241020008
- **Martínez Pardo Silvana** - 20241020010
- **Moreno Granado Sergio Leonardo** - 20242020091
- **Rodríguez Camacho Juan Esteban** - 20241020029

## Información Adicional

- **Institución**: Universidad Distrital Francisco José de Caldas
- **Facultad**: Facultad de Ingeniería
- **Programa**: Ingeniería de Sistemas
- **Asignatura**: Probabilidad y Estadística
- **Docente**: Diego Alberto Chitiva Huertas
- **Fecha de entrega**: Jueves, 11 de diciembre

## Referencias

- Wackerly, D. D., Mendenhall, W., & Scheaffer, R. L. (2008). *Estadística matemática con aplicaciones* (7a ed.). Cengage Learning.

Este proyecto busca aplicar los conceptos teóricos de la estadística en un problema práctico, desarrollando una solución algorítmica y documentando el proceso de manera formal.
