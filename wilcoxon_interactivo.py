import math

# Tolerancia para comparaciones de punto flotante
EPSILON = 0.0001

# Tabla de valores críticos de Wilcoxon
# Formato: TABLA[n][alpha][tipo_prueba]
# tipo_prueba: 'bilateral' o 'unilateral'
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
    'bilateral': {0.01: 2.576, 0.025: 2.241, 0.05: 1.96, 0.10: 1.645},
    'unilateral': {0.01: 2.326, 0.025: 1.96, 0.05: 1.645, 0.10: 1.282}
}

LIMITE_TABLA_EXACTA = 30


def asignar_rangos_con_empates(valores_absolutos):
    """Asigna rangos manejando empates con rango promedio."""
    n = len(valores_absolutos)
    indices = list(range(n))

    for i in range(n):
        for j in range(i + 1, n):
            if valores_absolutos[indices[i]] > valores_absolutos[indices[j]]:
                indices[i], indices[j] = indices[j], indices[i]

    rangos = [0] * n
    i = 0

    while i < n:
        j = i
        while j < n and abs(valores_absolutos[indices[j]] - valores_absolutos[indices[i]]) < EPSILON:
            j += 1
        rango_promedio = (i + 1 + j) / 2.0
        for k in range(i, j):
            rangos[indices[k]] = rango_promedio
        i = j
    return rangos


def test_wilcoxon_con_tabla_exacta(tamaño_muestra, estadistico_W, nivel_significancia, tipo_prueba='bilateral'):
    """Decisión estadística usando tabla exacta."""
    print("-" * 50)
    print("Cálculo estadístico - Tabla exacta de Wilcoxon")
    print("-" * 50)

    if tamaño_muestra not in TABLA_VALORES_CRITICOS:
        print(f"ERROR: n={tamaño_muestra} no está en la tabla.")
        return None
    
    if nivel_significancia not in TABLA_VALORES_CRITICOS[tamaño_muestra]:
        alphas = list(TABLA_VALORES_CRITICOS[tamaño_muestra].keys())
        print(f"ERROR: α={nivel_significancia} no disponible. Disponibles: {alphas}")
        return None
    
    valor_critico = TABLA_VALORES_CRITICOS[tamaño_muestra][nivel_significancia][tipo_prueba]
    
    if valor_critico is None:
        print(f"No existe valor crítico para esta combinación.")
        return None

    print(f"n={tamaño_muestra}, α={nivel_significancia}, prueba {tipo_prueba}")
    print(f"Valor crítico T₀ = {valor_critico}")
    print(f"W calculado = {estadistico_W:.2f}")
    print()
    print("Regla: Si W ≤ T₀ → Rechazar H₀")
    print()

    if estadistico_W <= valor_critico:
        print("✓ Se rechaza H₀: Diferencia significativa")
        return True
    else:
        print("✗ No se rechaza H₀: Sin diferencia significativa")
        return False


def test_wilcoxon_con_aproximacion_normal(tamaño_muestra, T_positivo, T_negativo, 
                                          nivel_significancia=0.05, tipo_prueba='bilateral', direccion=None):
    """Decisión estadística usando aproximación normal."""
    print("\n" + "-" * 70)
    print("Cálculo estadístico - Aproximación normal")
    print("-" * 70)

    Z_CRITICO = Z_CRITICOS[tipo_prueba].get(nivel_significancia, 1.96)

    media = tamaño_muestra * (tamaño_muestra + 1) / 4.0
    desviacion = math.sqrt(tamaño_muestra * (tamaño_muestra + 1) * (2 * tamaño_muestra + 1) / 24.0)

    print(f"μ(T⁺) = {media:.4f}, σ(T⁺) = {desviacion:.4f}")

    estadistico = T_positivo
    if estadistico > media:
        Z = (estadistico - media - 0.5) / desviacion
    else:
        Z = (estadistico - media + 0.5) / desviacion

    print(f"T⁺ = {T_positivo:.2f}, T⁻ = {T_negativo:.2f}")
    print(f"Z = {Z:.4f}")

    print(f"\nPrueba {tipo_prueba}, α = {nivel_significancia}")
    
    if tipo_prueba == 'bilateral':
        print(f"Región de rechazo: |Z| > {Z_CRITICO}")
        rechazar = abs(Z) > Z_CRITICO
    else:
        if direccion == 'mayor':
            print(f"Región de rechazo: Z > {Z_CRITICO}")
            rechazar = Z > Z_CRITICO
        else:
            print(f"Región de rechazo: Z < -{Z_CRITICO}")
            rechazar = Z < -Z_CRITICO

    if rechazar:
        print("✓ Se rechaza H₀")
        return True
    else:
        print("✗ No se rechaza H₀")
        return False


def elegir_metodo_estadistico(tamaño_muestra):
    """Permite al usuario elegir el método para muestras medianas."""
    print(f"{'-' * 45}")
    print("Selección del método estadístico")
    print(f"{'-' * 45}")
    print(f"n = {tamaño_muestra}")

    if tamaño_muestra <= 25:
        print("Método: Tabla exacta de Wilcoxon")
        return "tabla_exacta"
    elif tamaño_muestra <= LIMITE_TABLA_EXACTA:
        print("1. Tabla de Wilcoxon")
        print("2. Aproximación normal")
        while True:
            opcion = input("Seleccione (1/2): ").strip()
            if opcion == "1":
                return "tabla_exacta"
            elif opcion == "2":
                return "aproximacion_normal"
            print("Opción no válida.")
    else:
        print("Método: Aproximación normal")
        return "aproximacion_normal"


def seleccionar_parametros():
    """Permite al usuario seleccionar nivel de significancia y tipo de prueba."""
    print("\n" + "-" * 45)
    print("Configuración de la prueba")
    print("-" * 45)
    
    # Seleccionar nivel de significancia
    print("\nNivel de significancia (α):")
    print("1. α = 0.01")
    print("2. α = 0.025")
    print("3. α = 0.05 (predeterminado)")
    print("4. α = 0.10")
    
    while True:
        opcion = input("Seleccione (1-4) [3]: ").strip()
        if opcion == "" or opcion == "3":
            alpha = 0.05
            break
        elif opcion == "1":
            alpha = 0.01
            break
        elif opcion == "2":
            alpha = 0.025
            break
        elif opcion == "4":
            alpha = 0.10
            break
        print("Opción no válida.")
    
    # Seleccionar tipo de prueba
    print("\nTipo de prueba:")
    print("1. Bilateral (H₁: μ₁ ≠ μ₂) (predeterminado)")
    print("2. Unilateral derecha (H₁: μ₁ > μ₂)")
    print("3. Unilateral izquierda (H₁: μ₁ < μ₂)")
    
    direccion = None
    while True:
        opcion = input("Seleccione (1-3) [1]: ").strip()
        if opcion == "" or opcion == "1":
            tipo = 'bilateral'
            break
        elif opcion == "2":
            tipo = 'unilateral'
            direccion = 'mayor'
            break
        elif opcion == "3":
            tipo = 'unilateral'
            direccion = 'menor'
            break
        print("Opción no válida.")
    
    return alpha, tipo, direccion


def test_wilcoxon(muestra1, muestra2, nivel_significancia=0.05,
                  tipo_prueba='bilateral', direccion=None):
    """Realiza la Prueba de Rangos con Signo de Wilcoxon."""
    print("=" * 80)
    print("Test de Wilcoxon para muestras relacionadas")
    print("=" * 80)
    
    print("\nHipótesis:")
    print("H₀: No existe diferencia entre las condiciones")
    if tipo_prueba == 'bilateral':
        print("H₁: Existe diferencia entre las condiciones")
    elif direccion == 'mayor':
        print("H₁: Primera condición > Segunda condición")
    else:
        print("H₁: Primera condición < Segunda condición")
    
    print(f"\nα = {nivel_significancia}, Prueba {tipo_prueba}")

    # Calcular diferencias
    diferencias = [muestra1[i] - muestra2[i] for i in range(len(muestra1))]

    # Eliminar ceros
    diferencias_sin_cero = [d for d in diferencias if abs(d) > EPSILON]
    tamaño_muestra = len(diferencias_sin_cero)

    if tamaño_muestra == 0:
        print("\nERROR: Todas las diferencias son cero.")
        return None

    if tamaño_muestra < 3:
        print("\nADVERTENCIA: n < 3, resultados no confiables.")

    eliminados = len(diferencias) - tamaño_muestra
    print(f"\nDiferencias cero eliminadas: {eliminados}")
    print(f"n efectivo = {tamaño_muestra}")

    # Calcular rangos
    valores_absolutos = [abs(d) for d in diferencias_sin_cero]
    rangos = asignar_rangos_con_empates(valores_absolutos)

    # Aplicar signos
    rangos_con_signo = []
    for i in range(tamaño_muestra):
        if diferencias_sin_cero[i] > 0:
            rangos_con_signo.append(rangos[i])
        else:
            rangos_con_signo.append(-rangos[i])

    # Calcular T+ y T-
    T_positivo = sum(r for r in rangos_con_signo if r > 0)
    T_negativo = sum(abs(r) for r in rangos_con_signo if r < 0)

    print(f"\nT⁺ = {T_positivo:.2f}")
    print(f"T⁻ = {T_negativo:.2f}")
    
    # Verificación
    suma_teorica = tamaño_muestra * (tamaño_muestra + 1) / 2.0
    print(f"Verificación: T⁺ + T⁻ = {T_positivo + T_negativo:.2f} = {suma_teorica:.2f} ✓")

    estadistico_W = min(T_positivo, T_negativo)
    print(f"\nT = min(T⁺, T⁻) = {estadistico_W:.2f}")

    # Elegir método
    metodo = elegir_metodo_estadistico(tamaño_muestra)

    if metodo == "tabla_exacta":
        resultado = test_wilcoxon_con_tabla_exacta(
            tamaño_muestra, estadistico_W, nivel_significancia, tipo_prueba
        )
    else:
        resultado = test_wilcoxon_con_aproximacion_normal(
            tamaño_muestra, T_positivo, T_negativo, nivel_significancia, tipo_prueba, direccion
        )
    
    return resultado


def leer_muestra(nombre):
    """Lee una muestra del usuario."""
    while True:
        print(f"{nombre}")
        entrada = input("> ").replace(',', ' ')
        partes = entrada.split()

        numeros = []
        valido = True
        for parte in partes:
            try:
                numeros.append(float(parte))
            except ValueError:
                print("ERROR: Ingrese solo números.")
                valido = False
                break
        
        if valido and numeros:
            return numeros
        print("Intente nuevamente.")


def menu_principal():
    """Menú principal interactivo."""
    print("\n" + "=" * 60)
    print("  PRUEBA DE RANGOS CON SIGNO DE WILCOXON")
    print("  (Versión extendida con múltiples configuraciones)")
    print("=" * 60)

    while True:
        print("\n" + "-" * 50)
        print("Menú Principal")
        print("-" * 50)
        print("1. Ingresar mis propios datos")
        print("2. Ejemplo: n=10 (bilateral, α=0.05)")
        print("3. Ejemplo: n=10 (unilateral, α=0.05)")
        print("4. Ejemplo: n=10 (bilateral, α=0.01)")
        print("5. Ejemplo: n=27 (muestra mediana)")
        print("6. Ejemplo: n=35 (aproximación normal)")
        print("7. Salir")
        print("-" * 50)

        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            muestra1 = leer_muestra("Primera condición:")
            muestra2 = leer_muestra("Segunda condición:")
            
            if len(muestra1) != len(muestra2):
                print("ERROR: Las muestras deben tener el mismo tamaño.")
                continue
            
            alpha, tipo, direccion = seleccionar_parametros()
            test_wilcoxon(muestra1, muestra2, alpha, tipo, direccion)

        elif opcion == "2":
            print("\n--- Ejemplo: Bilateral, α=0.05 ---")
            m1 = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
            m2 = [12, 14, 13, 15, 11, 16, 12, 14, 13, 15]
            test_wilcoxon(m1, m2, 0.05, 'bilateral')

        elif opcion == "3":
            print("\n--- Ejemplo: Unilateral (H₁: m1 < m2), α=0.05 ---")
            m1 = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
            m2 = [12, 14, 13, 15, 11, 16, 12, 14, 13, 15]
            test_wilcoxon(m1, m2, 0.05, 'unilateral', 'menor')

        elif opcion == "4":
            print("\n--- Ejemplo: Bilateral, α=0.01 ---")
            m1 = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
            m2 = [12, 14, 13, 15, 11, 16, 12, 14, 13, 15]
            test_wilcoxon(m1, m2, 0.01, 'bilateral')

        elif opcion == "5":
            print("\n--- Ejemplo: n=27 ---")
            m1 = [14, 16, 15, 18, 17, 19, 15, 16, 17, 20, 18, 19,
                  16, 17, 15, 21, 19, 18, 17, 16, 20, 19, 18, 17,
                  16, 15, 14]
            m2 = [16, 14, 17, 20, 15, 22, 17, 14, 19, 22, 20,
                  21, 18, 19, 17, 23, 21, 20, 19, 18, 22, 21,
                  20, 19, 18, 17, 16]
            test_wilcoxon(m1, m2, 0.05, 'bilateral')

        elif opcion == "6":
            print("\n--- Ejemplo: n=35 (Aproximación normal) ---")
            m1 = [38, 42, 35, 45, 40, 39, 44, 37, 41, 43,
                  36, 39, 42, 38, 45, 40, 37, 44, 39, 41,
                  43, 36, 40, 38, 45, 42, 37, 44, 39, 41,
                  40, 43, 38, 42, 39]
            m2 = [41, 45, 38, 48, 43, 42, 47, 40, 44, 46,
                  39, 42, 45, 41, 48, 43, 40, 47, 42, 44,
                  46, 39, 43, 41, 48, 45, 40, 47, 42, 44,
                  43, 46, 41, 45, 42]
            test_wilcoxon(m1, m2, 0.05, 'bilateral')

        elif opcion == "7":
            print("\nFinalizando...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_principal()
