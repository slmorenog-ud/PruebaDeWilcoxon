import math

#Valores criticos (alpha = 0.05, dos colas)
TABLA_VALORES_CRITICOS = {
    5: 0, 6: 2, 7: 3, 8: 5, 9: 8, 10: 10,
    11: 13, 12: 17, 13: 21, 14: 25, 15: 30,
    16: 35, 17: 41, 18: 47, 19: 53, 20: 60,
    21: 68, 22: 75, 23: 83, 24: 91, 25: 100,
    26: 110, 27: 119, 28: 130, 29: 141, 30: 152
}

# Constante para definir el límite entre muestra pequeña/mediana/grande
LIMITE_TABLA_EXACTA = 30  # Usaremos tabla exacta hasta n=30

def asignar_rangos_con_empates(valores_absolutos):
    n = len(valores_absolutos)

    # Crear lista de índices para ordenar
    indices = list(range(n))

    # Ordenar los índices según los valores absolutos
    for i in range(n):
        for j in range(i + 1, n):
            if valores_absolutos[indices[i]] > valores_absolutos[indices[j]]:
                indices[i], indices[j] = indices[j], indices[i]

    # Asignar rangos
    rangos = [0] * n
    i = 0

    while i < n:
        # Encontrar cuántos valores son iguales (empates)
        j = i
        while j < n and abs(valores_absolutos[indices[j]] - valores_absolutos[indices[i]]) < 0.0001:
            j += 1
        # Calcular el rango promedio para los empates
        rango_promedio = (i + 1 + j) / 2.0
        # Asignar el rango promedio a todos los empates
        for k in range(i, j):
            rangos[indices[k]] = rango_promedio
        i = j
    return rangos

def test_wilcoxon_con_tabla_exacta(tamaño_muestra, estadistico_W, nivel_significancia):
    print("-" * 50)
    print("Calculo estadistico - Tabla exacta de Wilcoxon")
    print("-" * 50)

    valor_critico = TABLA_VALORES_CRITICOS[tamaño_muestra]

    print(f"Tamaño de muestra: n={tamaño_muestra}")
    print(f"Nivel de significancia: α={nivel_significancia}")
    print(f"Valor crítico: {valor_critico}")
    print(f"W calculado: {estadistico_W:.2f}")
    print()
    print("Regla de decisión: Si W ≤ Valor crítico → Rechazar H0")
    print()

    if estadistico_W <= valor_critico:
        print("Conclusión: Se rechaza H0")
        print("Existe una diferencia significativa entre las dos condiciones.")
        return True
    else:
        print("Conclusión: No se rechaza H0")
        print("No hay evidencia suficiente de una diferencia significativa.")
        return False


def test_wilcoxon_con_aproximacion_normal(tamaño_muestra, estadistico_W, nivel_significancia=0.05):
    print("\n" + "-" * 70)
    print("Calculo estadístico - Aproximación por distribución normal")
    print("-" * 70)

    # Valores críticos Z para α=0.05 (dos colas)
    Z_CRITICO = 1.96  # Valor estándar para 95% confianza

    # 1. Calcular parámetros teóricos
    media = tamaño_muestra * (tamaño_muestra + 1) / 4.0
    desviacion = math.sqrt(tamaño_muestra * (tamaño_muestra + 1) * (2 * tamaño_muestra + 1) / 24.0)

    print(f"Parametros utilizados:")
    print(f"Media: {media:.2f}")
    print(f"Desviación estándar: {desviacion:.2f}")

    # 2. Calcular Z observado (con corrección de continuidad)
    if estadistico_W > media:
        Z = (estadistico_W - media - 0.5) / desviacion
    else:
        Z = (estadistico_W - media + 0.5) / desviacion

    print(f"Z observado: {Z:.4f}")

    # 3. Comparar con Z crítico
    print(f"\nComparación con valor critico(α = {nivel_significancia}):")
    print(f"   Z crítico (dos colas): ±{Z_CRITICO}")
    print(f"   Región de rechazo: Z ≤ -{Z_CRITICO}  o  Z ≥ +{Z_CRITICO}")

    # 4. Decisión basada en Z
    if abs(Z) > Z_CRITICO:
        print(f"\n   |{Z:.4f}| > {Z_CRITICO} → Estadístico cae en región de rechazo")
        print("Se rechaza H0")
        resultado = True
    else:
        print(f"\n   |{Z:.4f}| ≤ {Z_CRITICO} → Estadístico cae en región de no rechazo")
        print("No se rechaza H0")
        resultado = False

    # 5. Interpretación
    print(f"\nInterpretación:")
    if resultado:
        print("Existe evidencia estadística significativa de una diferencia entre las dos condiciones.")
    else:
        print("No existe evidencia estadística significativa de una diferencia entre las dos condiciones.")

    return resultado


def test_wilcoxon(muestra1, muestra2, nivel_significancia=0.05, 
                  nombre_muestra1="Primera condición", nombre_muestra2="Segunda condición",
                  usar_aproximacion_normal=False):
    print("=" * 80)
    print(f"Test de Wilcoxon: {nombre_muestra1} vs {nombre_muestra2}")
    print("=" * 80)
    print("Hipotesis planteadas:")
    print(f"H0: No existe diferencia entre {nombre_muestra1} y {nombre_muestra2}")
    print(f"H1: Existe diferencia entre {nombre_muestra1} y {nombre_muestra2}")

    # PASO 1: Calcular diferencias
    diferencias = []
    for i in range(len(muestra1)):
        diferencia = muestra1[i] - muestra2[i]
        diferencias.append(diferencia)

    # PASO 2: Eliminar ceros
    diferencias_sin_cero = [d for d in diferencias if abs(d) > 0.0001]
    tamaño_muestra = len(diferencias_sin_cero)

    if tamaño_muestra == 0:
        print("\nLas diferencias obtenidas son de 0, no se puede aplicar el test de Wilcoxon.")
        return None

    if tamaño_muestra < 5:
        print("\nADVERTENCIA: La muestra resultante es muy pequeña, los resultados pueden no ser confiables")

    cantidad_eliminados = len(diferencias) - tamaño_muestra
    print(f"\nDiferencias cero eliminadas: {cantidad_eliminados}")
    print(f"Tamaño efectivo final de la muestra: n={tamaño_muestra}")

    # PASO 3: Calcular valores absolutos y rangos
    valores_absolutos = [abs(d) for d in diferencias_sin_cero]
    rangos = asignar_rangos_con_empates(valores_absolutos)

    # PASO 4: Aplicar signos
    rangos_con_signo = []
    for i in range(tamaño_muestra):
        rango_con_signo = rangos[i] if diferencias_sin_cero[i] > 0 else -rangos[i]
        rangos_con_signo.append(rango_con_signo)

    # PASO 5: Calcular W+ y W-
    suma_rangos_positivos = sum(r for r in rangos_con_signo if r > 0)
    suma_rangos_negativos = sum(abs(r) for r in rangos_con_signo if r < 0)

    print(f"\nValores calculados:")
    print(f"T+ (suma de rangos positivos): {suma_rangos_positivos:.2f}")
    print(f"T- (suma de rangos negativos): {suma_rangos_negativos:.2f}")
    
    # Verificación: T+ + T- = n(n+1)/2
    suma_teorica = tamaño_muestra * (tamaño_muestra + 1) / 2.0
    suma_real = suma_rangos_positivos + suma_rangos_negativos
    print(f"\nVerificación: T+ + T- = {suma_real:.2f}, n(n+1)/2 = {suma_teorica:.2f}")
    if abs(suma_real - suma_teorica) < 0.01:
        print("✓ Verificación correcta")
    else:
        print("✗ ERROR: La suma no coincide")

    estadistico_W = min(suma_rangos_positivos, suma_rangos_negativos)
    print(f"\nT (Estadístico de prueba - menor valor): {estadistico_W:.2f}")

    # Interpretación cualitativa
    print(f"\nInterpretacion cualitativa:")
    relacion = suma_rangos_positivos / suma_rangos_negativos if suma_rangos_negativos != 0 else float('inf')

    if suma_rangos_positivos == 0:
        print(f"Todas las observaciones favorecen {nombre_muestra2}")
    elif suma_rangos_negativos == 0:
        print(f"Todas las observaciones favorecen {nombre_muestra1}")
    elif relacion > 2:
        print(f"Fuerte tendencia hacia {nombre_muestra1}")
    elif relacion < 0.5:
        print(f"Fuerte tendencia hacia {nombre_muestra2}")
    elif relacion > 1.5:
        print(f"Tendencia moderada hacia {nombre_muestra1}")
    elif relacion < 0.67:
        print(f"Tendencia moderada hacia {nombre_muestra2}")
    else:
        print("Resultados equilibrados, lo cual produce diferencias poco claras")

    # PASO 6: Elegir metodo estadístico y tomar decisión
    if usar_aproximacion_normal or tamaño_muestra > LIMITE_TABLA_EXACTA:
        metodo = "aproximacion_normal"
        print(f"\n{'─' * 45}")
        print("Método seleccionado: Aproximación por distribución normal")
        print(f"{'─' * 45}")
    else:
        metodo = "tabla_exacta"
        print(f"\n{'─' * 45}")
        print("Método seleccionado: Tabla de Wilcoxon")
        print(f"{'─' * 45}")

    if metodo == "tabla_exacta":
        resultado = test_wilcoxon_con_tabla_exacta(tamaño_muestra, estadistico_W, nivel_significancia)
    else:
        resultado = test_wilcoxon_con_aproximacion_normal(tamaño_muestra, estadistico_W, nivel_significancia)
    
    print("\n")
    return resultado


def ejecutar_pruebas_automaticas():
    """
    Ejecuta automáticamente varios casos de prueba del Test de Wilcoxon.
    Optimizado para Google Colab (sin input()).
    """
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " " * 20 + "PRUEBA DE WILCOXON - CASOS DE PRUEBA" + " " * 22 + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    resultados = []
    
    # ============================================================================
    # CASO 1: Ejemplo 15.8 del libro de Wackerly et al. (2008)
    # Programa de lectura - Comparación antes y después
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 1: Ejemplo 15.8 - Programa de Lectura (Wackerly et al., 2008)")
    print("█" * 80)
    print("Descripción: Puntuaciones de comprensión de lectura antes y después")
    print("de un programa de entrenamiento especial.")
    print()
    
    # Datos del Ejemplo 15.8
    antes = [6, 8, 10, 5, 7, 9, 6, 8, 7, 9]
    despues = [8, 10, 12, 7, 9, 11, 8, 10, 9, 11]
    
    resultado = test_wilcoxon(
        antes, despues,
        nombre_muestra1="Antes del programa",
        nombre_muestra2="Después del programa",
        usar_aproximacion_normal=False
    )
    resultados.append(("Ejemplo 15.8 - Programa de Lectura", resultado))
    
    # ============================================================================
    # CASO 2: Muestra pequeña (n=10)
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 2: Muestra Pequeña (n=10)")
    print("█" * 80)
    print("Descripción: Productividad con y sin intervención (n=10)")
    print()
    
    muestra_pequeña_1 = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
    muestra_pequeña_2 = [12, 14, 13, 15, 11, 16, 12, 14, 13, 15]
    
    resultado = test_wilcoxon(
        muestra_pequeña_1, muestra_pequeña_2,
        nombre_muestra1="Sin intervención",
        nombre_muestra2="Con intervención",
        usar_aproximacion_normal=False
    )
    resultados.append(("Muestra Pequeña (n=10)", resultado))
    
    # ============================================================================
    # CASO 3: Muestra grande (n=35) - Aproximación normal
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 3: Muestra Grande (n=35) - Aproximación Normal")
    print("█" * 80)
    print("Descripción: Mediciones antes y después de un tratamiento (n=35)")
    print()
    
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
        nombre_muestra1="Antes del tratamiento",
        nombre_muestra2="Después del tratamiento",
        usar_aproximacion_normal=True
    )
    resultados.append(("Muestra Grande (n=35)", resultado))
    
    # ============================================================================
    # CASO 4: Caso con empates y diferencias cero
    # ============================================================================
    print("\n" + "█" * 80)
    print("█ CASO 4: Caso con Empates y Diferencias Cero")
    print("█" * 80)
    print("Descripción: Datos con valores repetidos y algunas diferencias cero")
    print()
    
    # Datos diseñados para tener empates y ceros
    muestra_empates_1 = [5, 7, 8, 8, 10, 12, 12, 12, 15, 18, 20, 20]
    muestra_empates_2 = [5, 9, 10, 6, 12, 14, 10, 11, 17, 20, 22, 19]
    
    resultado = test_wilcoxon(
        muestra_empates_1, muestra_empates_2,
        nombre_muestra1="Medición A",
        nombre_muestra2="Medición B",
        usar_aproximacion_normal=False
    )
    resultados.append(("Caso con Empates", resultado))
    
    # ============================================================================
    # RESUMEN FINAL
    # ============================================================================
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "RESUMEN FINAL" + " " * 35 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print(f"{'Caso de Prueba':<45} {'Resultado':<20}")
    print("-" * 70)
    
    for nombre, resultado in resultados:
        if resultado is None:
            estado = "ERROR"
        elif resultado:
            estado = "H0 Rechazada ✓"
        else:
            estado = "H0 No Rechazada"
        print(f"{nombre:<45} {estado:<20}")
    
    print("\n" + "═" * 80)
    print("Todas las pruebas completadas exitosamente.")
    print("═" * 80)


if __name__ == "__main__":
    ejecutar_pruebas_automaticas()
