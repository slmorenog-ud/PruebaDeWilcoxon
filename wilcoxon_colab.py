import math

# Tolerancia para comparaciones de punto flotante
EPSILON = 0.0001

# Tabla de valores críticos de Wilcoxon
# Formato: TABLA[n][alpha][tipo_prueba]
# tipo_prueba: 'bilateral' o 'unilateral'
# Valores críticos para diferentes niveles de significancia
TABLA_VALORES_CRITICOS = {
    # n=3 a n=4 (muestras muy pequeñas)
    3: {0.05: {'unilateral': 0, 'bilateral': None}, 0.10: {'unilateral': 0, 'bilateral': 0}},
    4: {0.05: {'unilateral': 0, 'bilateral': 0}, 0.10: {'unilateral': 1, 'bilateral': 0}},
    # n=5 a n=10
    5: {0.01: {'unilateral': 0, 'bilateral': None}, 0.025: {'unilateral': 0, 'bilateral': 0}, 0.05: {'unilateral': 0, 'bilateral': 0}, 0.10: {'unilateral': 2, 'bilateral': 0}},
    6: {0.01: {'unilateral': 0, 'bilateral': None}, 0.025: {'unilateral': 0, 'bilateral': 0}, 0.05: {'unilateral': 2, 'bilateral': 0}, 0.10: {'unilateral': 3, 'bilateral': 2}},
    7: {0.01: {'unilateral': 0, 'bilateral': None}, 0.025: {'unilateral': 1, 'bilateral': 0}, 0.05: {'unilateral': 3, 'bilateral': 2}, 0.10: {'unilateral': 5, 'bilateral': 3}},
    8: {0.01: {'unilateral': 0, 'bilateral': 0}, 0.025: {'unilateral': 3, 'bilateral': 1}, 0.05: {'unilateral': 5, 'bilateral': 3}, 0.10: {'unilateral': 8, 'bilateral': 5}},
    9: {0.01: {'unilateral': 1, 'bilateral': 0}, 0.025: {'unilateral': 5, 'bilateral': 3}, 0.05: {'unilateral': 8, 'bilateral': 5}, 0.10: {'unilateral': 10, 'bilateral': 8}},
    10: {0.01: {'unilateral': 3, 'bilateral': 0}, 0.025: {'unilateral': 8, 'bilateral': 5}, 0.05: {'unilateral': 10, 'bilateral': 8}, 0.10: {'unilateral': 14, 'bilateral': 10}},
    # n=11 a n=15
    11: {0.01: {'unilateral': 5, 'bilateral': 1}, 0.025: {'unilateral': 10, 'bilateral': 7}, 0.05: {'unilateral': 13, 'bilateral': 10}, 0.10: {'unilateral': 17, 'bilateral': 13}},
    12: {0.01: {'unilateral': 7, 'bilateral': 3}, 0.025: {'unilateral': 13, 'bilateral': 9}, 0.05: {'unilateral': 17, 'bilateral': 13}, 0.10: {'unilateral': 21, 'bilateral': 17}},
    13: {0.01: {'unilateral': 9, 'bilateral': 5}, 0.025: {'unilateral': 17, 'bilateral': 12}, 0.05: {'unilateral': 21, 'bilateral': 17}, 0.10: {'unilateral': 26, 'bilateral': 21}},
    14: {0.01: {'unilateral': 12, 'bilateral': 7}, 0.025: {'unilateral': 21, 'bilateral': 15}, 0.05: {'unilateral': 25, 'bilateral': 21}, 0.10: {'unilateral': 31, 'bilateral': 25}},
    15: {0.01: {'unilateral': 15, 'bilateral': 9}, 0.025: {'unilateral': 25, 'bilateral': 19}, 0.05: {'unilateral': 30, 'bilateral': 25}, 0.10: {'unilateral': 36, 'bilateral': 30}},
    # n=16 a n=20
    16: {0.01: {'unilateral': 19, 'bilateral': 12}, 0.025: {'unilateral': 29, 'bilateral': 23}, 0.05: {'unilateral': 35, 'bilateral': 29}, 0.10: {'unilateral': 42, 'bilateral': 35}},
    17: {0.01: {'unilateral': 23, 'bilateral': 15}, 0.025: {'unilateral': 34, 'bilateral': 27}, 0.05: {'unilateral': 41, 'bilateral': 34}, 0.10: {'unilateral': 48, 'bilateral': 41}},
    18: {0.01: {'unilateral': 27, 'bilateral': 19}, 0.025: {'unilateral': 40, 'bilateral': 32}, 0.05: {'unilateral': 47, 'bilateral': 40}, 0.10: {'unilateral': 55, 'bilateral': 47}},
    19: {0.01: {'unilateral': 32, 'bilateral': 23}, 0.025: {'unilateral': 46, 'bilateral': 37}, 0.05: {'unilateral': 53, 'bilateral': 46}, 0.10: {'unilateral': 62, 'bilateral': 53}},
    20: {0.01: {'unilateral': 37, 'bilateral': 27}, 0.025: {'unilateral': 52, 'bilateral': 43}, 0.05: {'unilateral': 60, 'bilateral': 52}, 0.10: {'unilateral': 69, 'bilateral': 60}},
    # n=21 a n=25
    21: {0.01: {'unilateral': 42, 'bilateral': 32}, 0.025: {'unilateral': 58, 'bilateral': 49}, 0.05: {'unilateral': 67, 'bilateral': 58}, 0.10: {'unilateral': 77, 'bilateral': 68}},
    22: {0.01: {'unilateral': 48, 'bilateral': 37}, 0.025: {'unilateral': 65, 'bilateral': 55}, 0.05: {'unilateral': 75, 'bilateral': 65}, 0.10: {'unilateral': 86, 'bilateral': 75}},
    23: {0.01: {'unilateral': 54, 'bilateral': 43}, 0.025: {'unilateral': 73, 'bilateral': 62}, 0.05: {'unilateral': 83, 'bilateral': 73}, 0.10: {'unilateral': 94, 'bilateral': 83}},
    24: {0.01: {'unilateral': 61, 'bilateral': 49}, 0.025: {'unilateral': 81, 'bilateral': 69}, 0.05: {'unilateral': 91, 'bilateral': 81}, 0.10: {'unilateral': 104, 'bilateral': 91}},
    25: {0.01: {'unilateral': 68, 'bilateral': 56}, 0.025: {'unilateral': 89, 'bilateral': 76}, 0.05: {'unilateral': 100, 'bilateral': 89}, 0.10: {'unilateral': 113, 'bilateral': 100}},
    # n=26 a n=30
    26: {0.01: {'unilateral': 75, 'bilateral': 63}, 0.025: {'unilateral': 98, 'bilateral': 84}, 0.05: {'unilateral': 110, 'bilateral': 98}, 0.10: {'unilateral': 124, 'bilateral': 110}},
    27: {0.01: {'unilateral': 83, 'bilateral': 70}, 0.025: {'unilateral': 107, 'bilateral': 92}, 0.05: {'unilateral': 119, 'bilateral': 107}, 0.10: {'unilateral': 134, 'bilateral': 119}},
    28: {0.01: {'unilateral': 91, 'bilateral': 77}, 0.025: {'unilateral': 116, 'bilateral': 101}, 0.05: {'unilateral': 130, 'bilateral': 116}, 0.10: {'unilateral': 145, 'bilateral': 130}},
    29: {0.01: {'unilateral': 100, 'bilateral': 85}, 0.025: {'unilateral': 126, 'bilateral': 110}, 0.05: {'unilateral': 141, 'bilateral': 126}, 0.10: {'unilateral': 157, 'bilateral': 141}},
    30: {0.01: {'unilateral': 109, 'bilateral': 93}, 0.025: {'unilateral': 137, 'bilateral': 120}, 0.05: {'unilateral': 152, 'bilateral': 137}, 0.10: {'unilateral': 169, 'bilateral': 152}},
}

# Valores críticos Z para diferentes niveles de significancia
Z_CRITICOS = {
    # Para prueba bilateral (α/2 en cada cola)
    'bilateral': {0.01: 2.576, 0.025: 2.241, 0.05: 1.96, 0.10: 1.645},
    # Para prueba unilateral (α en una cola)
    'unilateral': {0.01: 2.326, 0.025: 1.96, 0.05: 1.645, 0.10: 1.282}
}

# Constante para definir el límite entre muestra pequeña/grande
LIMITE_TABLA_EXACTA = 30


def asignar_rangos_con_empates(valores_absolutos):
    """
    Asigna rangos a los valores absolutos, manejando empates con rango promedio.
    """
    n = len(valores_absolutos)
    indices = list(range(n))

    # Ordenar los índices según los valores absolutos (bubble sort)
    for i in range(n):
        for j in range(i + 1, n):
            if valores_absolutos[indices[i]] > valores_absolutos[indices[j]]:
                indices[i], indices[j] = indices[j], indices[i]

    # Asignar rangos
    rangos = [0] * n
    i = 0

    while i < n:
        j = i
        # Encontrar valores iguales (empates)
        while j < n and abs(valores_absolutos[indices[j]] - valores_absolutos[indices[i]]) < EPSILON:
            j += 1
        # Calcular el rango promedio para los empates
        rango_promedio = (i + 1 + j) / 2.0
        for k in range(i, j):
            rangos[indices[k]] = rango_promedio
        i = j
    return rangos


def test_wilcoxon_con_tabla_exacta(tamaño_muestra, estadistico_W, nivel_significancia, tipo_prueba='bilateral'):
    """
    Realiza la decisión estadística usando la tabla exacta de Wilcoxon.
    
    Parámetros:
    - tamaño_muestra: n (después de eliminar ceros)
    - estadistico_W: min(T+, T-)
    - nivel_significancia: 0.01, 0.025, 0.05 o 0.10
    - tipo_prueba: 'bilateral' o 'unilateral'
    """
    print("-" * 50)
    print("Cálculo estadístico - Tabla exacta de Wilcoxon")
    print("-" * 50)

    # Verificar si el tamaño de muestra está en la tabla
    if tamaño_muestra not in TABLA_VALORES_CRITICOS:
        print(f"ERROR: n={tamaño_muestra} no está en la tabla. Use aproximación normal.")
        return None
    
    # Verificar si el nivel de significancia está disponible
    if nivel_significancia not in TABLA_VALORES_CRITICOS[tamaño_muestra]:
        alphas_disponibles = list(TABLA_VALORES_CRITICOS[tamaño_muestra].keys())
        print(f"ERROR: α={nivel_significancia} no disponible para n={tamaño_muestra}")
        print(f"Valores disponibles: {alphas_disponibles}")
        return None
    
    valor_critico = TABLA_VALORES_CRITICOS[tamaño_muestra][nivel_significancia][tipo_prueba]
    
    if valor_critico is None:
        print(f"No existe valor crítico para n={tamaño_muestra}, α={nivel_significancia}, prueba {tipo_prueba}")
        print("Considere usar un nivel de significancia diferente o aproximación normal.")
        return None

    print(f"Tamaño de muestra: n={tamaño_muestra}")
    print(f"Nivel de significancia: α={nivel_significancia}")
    print(f"Tipo de prueba: {tipo_prueba}")
    print(f"Valor crítico: T₀ = {valor_critico}")
    print(f"Estadístico W calculado: {estadistico_W:.2f}")
    print()
    print("Regla de decisión: Si W ≤ T₀ → Rechazar H₀")
    print()

    if estadistico_W <= valor_critico:
        print("Conclusión: Se rechaza H₀")
        print("Existe una diferencia significativa entre las dos condiciones.")
        return True
    else:
        print("Conclusión: No se rechaza H₀")
        print("No hay evidencia suficiente de una diferencia significativa.")
        return False


def test_wilcoxon_con_aproximacion_normal(tamaño_muestra, T_positivo, T_negativo, nivel_significancia=0.05, tipo_prueba='bilateral', direccion=None):
    """
    Realiza la decisión estadística usando aproximación normal para muestras grandes.
    
    Parámetros:
    - tamaño_muestra: n (después de eliminar ceros)
    - T_positivo: suma de rangos positivos
    - T_negativo: suma de rangos negativos
    - nivel_significancia: 0.01, 0.025, 0.05 o 0.10
    - tipo_prueba: 'bilateral' o 'unilateral'
    - direccion: 'mayor' o 'menor' (solo para prueba unilateral)
    """
    print("\n" + "-" * 70)
    print("Cálculo estadístico - Aproximación por distribución normal")
    print("-" * 70)

    # Obtener valor crítico Z
    Z_CRITICO = Z_CRITICOS[tipo_prueba].get(nivel_significancia, 1.96)

    # Calcular parámetros teóricos
    media = tamaño_muestra * (tamaño_muestra + 1) / 4.0
    desviacion = math.sqrt(tamaño_muestra * (tamaño_muestra + 1) * (2 * tamaño_muestra + 1) / 24.0)

    print(f"Parámetros teóricos bajo H₀:")
    print(f"  μ(T⁺) = n(n+1)/4 = {media:.4f}")
    print(f"  σ(T⁺) = √[n(n+1)(2n+1)/24] = {desviacion:.4f}")

    # Para aproximación normal, usamos T+ como estadístico
    estadistico = T_positivo
    
    # Calcular Z observado (con corrección de continuidad)
    if estadistico > media:
        Z = (estadistico - media - 0.5) / desviacion
    else:
        Z = (estadistico - media + 0.5) / desviacion

    print(f"\nEstadístico T⁺: {T_positivo:.2f}")
    print(f"Estadístico T⁻: {T_negativo:.2f}")
    print(f"Z observado (con corrección de continuidad): {Z:.4f}")

    # Comparar con Z crítico
    print(f"\nPrueba {tipo_prueba} con α = {nivel_significancia}:")
    
    if tipo_prueba == 'bilateral':
        print(f"  Región de rechazo: Z ≤ -{Z_CRITICO} o Z ≥ +{Z_CRITICO}")
        rechazar = abs(Z) > Z_CRITICO
    else:  # unilateral
        if direccion == 'mayor':
            print(f"  H₁: La primera condición es mayor")
            print(f"  Región de rechazo: Z ≥ +{Z_CRITICO}")
            rechazar = Z > Z_CRITICO
        else:  # menor
            print(f"  H₁: La primera condición es menor")
            print(f"  Región de rechazo: Z ≤ -{Z_CRITICO}")
            rechazar = Z < -Z_CRITICO

    # Decisión
    if rechazar:
        print(f"\n  |Z| = {abs(Z):.4f} → Estadístico cae en región de rechazo")
        print("Se rechaza H₀")
        print("\nInterpretación: Existe evidencia estadística significativa de una diferencia.")
        return True
    else:
        print(f"\n  |Z| = {abs(Z):.4f} → Estadístico NO cae en región de rechazo")
        print("No se rechaza H₀")
        print("\nInterpretación: No existe evidencia estadística significativa de una diferencia.")
        return False


def test_wilcoxon(muestra1, muestra2, nivel_significancia=0.05, 
                  nombre_muestra1="Primera condición", nombre_muestra2="Segunda condición",
                  tipo_prueba='bilateral', direccion=None, usar_aproximacion_normal=None):
    """
    Realiza la Prueba de Rangos con Signo de Wilcoxon.
    
    Parámetros:
    - muestra1, muestra2: listas de observaciones pareadas
    - nivel_significancia: 0.01, 0.025, 0.05 o 0.10
    - nombre_muestra1, nombre_muestra2: nombres descriptivos
    - tipo_prueba: 'bilateral' o 'unilateral'
    - direccion: 'mayor' o 'menor' (solo para unilateral)
      - 'mayor': H₁ espera que muestra1 > muestra2
      - 'menor': H₁ espera que muestra1 < muestra2
    - usar_aproximacion_normal: True/False/None (None = automático según n)
    """
    print("=" * 80)
    print(f"Test de Wilcoxon: {nombre_muestra1} vs {nombre_muestra2}")
    print("=" * 80)
    
    # Mostrar hipótesis
    print("\nHipótesis planteadas:")
    print(f"H₀: No existe diferencia entre {nombre_muestra1} y {nombre_muestra2}")
    if tipo_prueba == 'bilateral':
        print(f"H₁: Existe diferencia entre {nombre_muestra1} y {nombre_muestra2}")
    else:
        if direccion == 'mayor':
            print(f"H₁: {nombre_muestra1} > {nombre_muestra2}")
        else:
            print(f"H₁: {nombre_muestra1} < {nombre_muestra2}")
    
    print(f"\nNivel de significancia: α = {nivel_significancia}")
    print(f"Tipo de prueba: {tipo_prueba}")

    # PASO 1: Calcular diferencias
    if len(muestra1) != len(muestra2):
        print("ERROR: Las muestras deben tener el mismo tamaño.")
        return None
        
    diferencias = []
    for i in range(len(muestra1)):
        diferencias.append(muestra1[i] - muestra2[i])

    # PASO 2: Eliminar ceros
    diferencias_sin_cero = [d for d in diferencias if abs(d) > EPSILON]
    tamaño_muestra = len(diferencias_sin_cero)

    if tamaño_muestra == 0:
        print("\nERROR: Todas las diferencias son cero, no se puede aplicar el test.")
        return None

    if tamaño_muestra < 3:
        print("\nADVERTENCIA: n < 3, los resultados no son confiables.")

    cantidad_eliminados = len(diferencias) - tamaño_muestra
    print(f"\nDiferencias cero eliminadas: {cantidad_eliminados}")
    print(f"Tamaño efectivo de la muestra: n = {tamaño_muestra}")

    # PASO 3: Calcular valores absolutos y rangos
    valores_absolutos = [abs(d) for d in diferencias_sin_cero]
    rangos = asignar_rangos_con_empates(valores_absolutos)

    # PASO 4: Aplicar signos
    rangos_con_signo = []
    for i in range(tamaño_muestra):
        if diferencias_sin_cero[i] > 0:
            rangos_con_signo.append(rangos[i])
        else:
            rangos_con_signo.append(-rangos[i])

    # PASO 5: Calcular T+ y T-
    suma_rangos_positivos = sum(r for r in rangos_con_signo if r > 0)
    suma_rangos_negativos = sum(abs(r) for r in rangos_con_signo if r < 0)

    print(f"\nValores calculados:")
    print(f"  T⁺ (suma de rangos positivos): {suma_rangos_positivos:.2f}")
    print(f"  T⁻ (suma de rangos negativos): {suma_rangos_negativos:.2f}")
    
    # Verificación
    suma_teorica = tamaño_muestra * (tamaño_muestra + 1) / 2.0
    suma_real = suma_rangos_positivos + suma_rangos_negativos
    print(f"\nVerificación: T⁺ + T⁻ = {suma_real:.2f}, n(n+1)/2 = {suma_teorica:.2f}")
    if abs(suma_real - suma_teorica) < 0.01:
        print("✓ Verificación correcta")
    else:
        print("✗ ERROR en la suma de rangos")

    estadistico_W = min(suma_rangos_positivos, suma_rangos_negativos)
    print(f"\nEstadístico T = min(T⁺, T⁻) = {estadistico_W:.2f}")

    # Interpretación cualitativa
    print(f"\nInterpretación cualitativa:")
    if suma_rangos_negativos > 0:
        relacion = suma_rangos_positivos / suma_rangos_negativos
    else:
        relacion = float('inf')

    if suma_rangos_positivos == 0:
        print(f"  Todas las observaciones favorecen {nombre_muestra2}")
    elif suma_rangos_negativos == 0:
        print(f"  Todas las observaciones favorecen {nombre_muestra1}")
    elif relacion > 2:
        print(f"  Fuerte tendencia hacia {nombre_muestra1}")
    elif relacion < 0.5:
        print(f"  Fuerte tendencia hacia {nombre_muestra2}")
    elif relacion > 1.5:
        print(f"  Tendencia moderada hacia {nombre_muestra1}")
    elif relacion < 0.67:
        print(f"  Tendencia moderada hacia {nombre_muestra2}")
    else:
        print("  Resultados equilibrados, diferencias poco claras")

    # PASO 6: Elegir método y tomar decisión
    if usar_aproximacion_normal is None:
        usar_aproximacion_normal = tamaño_muestra > LIMITE_TABLA_EXACTA
    
    if usar_aproximacion_normal:
        print(f"\n{'─' * 50}")
        print("Método seleccionado: Aproximación por distribución normal")
        print(f"{'─' * 50}")
        resultado = test_wilcoxon_con_aproximacion_normal(
            tamaño_muestra, suma_rangos_positivos, suma_rangos_negativos,
            nivel_significancia, tipo_prueba, direccion
        )
    else:
        print(f"\n{'─' * 50}")
        print("Método seleccionado: Tabla exacta de Wilcoxon")
        print(f"{'─' * 50}")
        resultado = test_wilcoxon_con_tabla_exacta(
            tamaño_muestra, estadistico_W, nivel_significancia, tipo_prueba
        )
    
    print("\n")
    return resultado


def ejecutar_pruebas_automaticas():
    """
    Ejecuta automáticamente varios casos de prueba del Test de Wilcoxon.
    Incluye diferentes niveles de significancia y tipos de prueba.
    """
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " " * 15 + "PRUEBA DE WILCOXON - CASOS DE PRUEBA EXTENDIDOS" + " " * 15 + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    resultados = []
    
    # ============================================================================
    # CASO 1: Ejemplo del libro - Prueba bilateral α=0.05
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 1: Ejemplo Programa de Lectura (bilateral, α=0.05)")
    print("█" * 80)
    
    antes = [6, 8, 10, 5, 7, 9, 6, 8, 7, 9]
    despues = [8, 10, 12, 7, 9, 11, 8, 10, 9, 11]
    
    resultado = test_wilcoxon(
        antes, despues,
        nombre_muestra1="Antes",
        nombre_muestra2="Después",
        nivel_significancia=0.05,
        tipo_prueba='bilateral'
    )
    resultados.append(("Bilateral α=0.05", resultado))
    
    # ============================================================================
    # CASO 2: Prueba unilateral (cola izquierda) α=0.05
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 2: Mismo ejemplo - Prueba unilateral (H₁: Antes < Después)")
    print("█" * 80)
    
    resultado = test_wilcoxon(
        antes, despues,
        nombre_muestra1="Antes",
        nombre_muestra2="Después",
        nivel_significancia=0.05,
        tipo_prueba='unilateral',
        direccion='menor'
    )
    resultados.append(("Unilateral (menor) α=0.05", resultado))
    
    # ============================================================================
    # CASO 3: Prueba con α=0.01
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 3: Mismo ejemplo con α=0.01 (más estricto)")
    print("█" * 80)
    
    resultado = test_wilcoxon(
        antes, despues,
        nombre_muestra1="Antes",
        nombre_muestra2="Después",
        nivel_significancia=0.01,
        tipo_prueba='bilateral'
    )
    resultados.append(("Bilateral α=0.01", resultado))
    
    # ============================================================================
    # CASO 4: Muestra muy pequeña (n=5)
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 4: Muestra pequeña (n=5)")
    print("█" * 80)
    
    m1 = [10, 12, 8, 15, 11]
    m2 = [12, 14, 10, 17, 13]
    
    resultado = test_wilcoxon(
        m1, m2,
        nombre_muestra1="Control",
        nombre_muestra2="Tratamiento",
        nivel_significancia=0.05,
        tipo_prueba='bilateral'
    )
    resultados.append(("Muestra n=5", resultado))
    
    # ============================================================================
    # CASO 5: Muestra grande con aproximación normal
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 5: Muestra grande (n=35) - Aproximación Normal")
    print("█" * 80)
    
    muestra_grande_1 = [38, 42, 35, 45, 40, 39, 44, 37, 41, 43,
                        36, 39, 42, 38, 45, 40, 37, 44, 39, 41,
                        43, 36, 40, 38, 45, 42, 37, 44, 39, 41,
                        40, 43, 38, 42, 39]
    muestra_grande_2 = [41, 45, 38, 48, 43, 42, 47, 40, 44, 46,
                        39, 42, 45, 41, 48, 43, 40, 47, 42, 44,
                        46, 39, 43, 41, 48, 45, 40, 47, 42, 44,
                        43, 46, 41, 45, 42]
    
    resultado = test_wilcoxon(
        muestra_grande_1, muestra_grande_2,
        nombre_muestra1="Antes",
        nombre_muestra2="Después",
        nivel_significancia=0.05,
        tipo_prueba='bilateral',
        usar_aproximacion_normal=True
    )
    resultados.append(("Muestra grande n=35", resultado))
    
    # ============================================================================
    # CASO 6: Caso con empates
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 6: Caso con empates y diferencias cero")
    print("█" * 80)
    
    muestra_empates_1 = [5, 7, 8, 8, 10, 12, 12, 12, 15, 18, 20, 20]
    muestra_empates_2 = [5, 9, 10, 6, 12, 14, 10, 11, 17, 20, 22, 19]
    
    resultado = test_wilcoxon(
        muestra_empates_1, muestra_empates_2,
        nombre_muestra1="Medición A",
        nombre_muestra2="Medición B",
        nivel_significancia=0.05,
        tipo_prueba='bilateral'
    )
    resultados.append(("Con empates", resultado))
    
    # ============================================================================
    # RESUMEN FINAL
    # ============================================================================
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "RESUMEN FINAL" + " " * 35 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print(f"{'Caso de Prueba':<40} {'Resultado':<20}")
    print("-" * 60)
    
    for nombre, resultado in resultados:
        if resultado is None:
            estado = "ERROR"
        elif resultado:
            estado = "H₀ Rechazada ✓"
        else:
            estado = "H₀ No Rechazada"
        print(f"{nombre:<40} {estado:<20}")
    
    print("\n" + "═" * 80)
    print("Todas las pruebas completadas.")
    print("═" * 80)


if __name__ == "__main__":
    ejecutar_pruebas_automaticas()
