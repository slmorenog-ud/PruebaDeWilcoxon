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


def elegir_metodo_estadistico(tamaño_muestra, LIMITE_TABLA_EXACTA=30):
    print(f"{'-' * 45}")
    print("Selección del método estadístico adecuado")
    print(f"{'-' * 45}")

    print(f"Tamaño de muestra efectivo: n={tamaño_muestra}")

    # Caso 1: n ≤ 25 → Tabla exacta (siempre)
    if tamaño_muestra <= 25:
        print("Método seleccionado: Tabla de Wilcoxon")
        return "tabla_exacta"

    # Caso 2: 26 ≤ n ≤ LIMITE_TABLA_EXACTA → Usuario decide
    elif tamaño_muestra <= LIMITE_TABLA_EXACTA:
        print("Opción 1: Tabla de Wilcoxon")
        print("Opción 2: Aproximación por distribución normal")

        while True:
            eleccion = input("\nSeleccione método (1=Tabla exacta, 2=Aproximación normal): ").strip()
            if eleccion == "1":
                return "tabla_exacta"
            elif eleccion == "2":
                return "aproximacion_normal"
            else:
                print("Ingreso una opción no valida.")

    # Caso 3: n > LIMITE_TABLA_EXACTA → Solo aproximación normal
    else:
        print("Método seleccionado: Aproximación por distribución normal")
        return "aproximacion_normal"


def test_wilcoxon(productividad_sin_musica, productividad_con_rock, nivel_significancia=0.05):
    print("-" * 40)
    print("Test de Wilcoxon para muestras relacionadas")
    print("-" * 40)
    print("Hipotesis planteadas:")
    print("H0: No existe diferencia entre las dos condiciones")
    print("H1: Existe diferencia entre las dos condiciones")

    # PASO 1: Calcular diferencias
    diferencias = []
    for i in range(len(productividad_sin_musica)):
        diferencia = productividad_sin_musica[i] - productividad_con_rock[i]
        diferencias.append(diferencia)

    # PASO 2: Eliminar ceros
    diferencias_sin_cero = [d for d in diferencias if d != 0]
    tamaño_muestra = len(diferencias_sin_cero)

    if tamaño_muestra == 0:
        print("\nLas diferencias obtenidas son de 0, no se puede aplicar el test de Wilcoxon.")
        return

    if tamaño_muestra < 5:
        print("\nLa muestra resultante es muy pequeña, por lo tanto, los resultados obtenidos pueden no son confiables")

    cantidad_eliminados = len(diferencias) - tamaño_muestra
    print(f"\nDiferencias cero eliminadas: {cantidad_eliminados}")
    print(f"Tamaño efectivo final de la muestra: {tamaño_muestra}")

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

    estadistico_W = min(suma_rangos_positivos, suma_rangos_negativos)
    print(f"T (Suma menor valor): {estadistico_W:.2f}")

    # Interpretación cualitativa
    print(f"\nInterpretacion cualitativa:")
    relacion = suma_rangos_positivos / suma_rangos_negativos if suma_rangos_negativos != 0 else float('inf')

    if suma_rangos_positivos == 0:
        print("Todas las observaciones favorecen la segunda condición")
    elif suma_rangos_negativos == 0:
        print("Todas las observaciones favorecen la primera condición")
    elif relacion > 2:
        print("Fuerte tendencia hacia la primera condición")
    elif relacion < 0.5:
        print("Fuerte tendencia hacia la segunda condición")
    elif relacion > 1.5:
        print("Tendencia moderada hacia la primera condición")
    elif relacion < 0.67:
        print("Tendencia moderada hacia la segunda condición")
    else:
        print("Resultados equilibrados, lo cual produce diferencias poco claras")

    # PASO 6: Elegir metodo estadístico y tomar decisión
    metodo = elegir_metodo_estadistico(tamaño_muestra)

    if metodo == "tabla_exacta":
        test_wilcoxon_con_tabla_exacta(tamaño_muestra, estadistico_W, nivel_significancia)
    else:
        test_wilcoxon_con_aproximacion_normal(tamaño_muestra, estadistico_W, nivel_significancia)

# Función para leer datos del usuario (igual que antes)
def leer_muestra(nombre_muestra):
    while True:
        print(f"{nombre_muestra}")
        entrada = input("> ").replace(',', ' ')
        partes = entrada.split()

        numeros = []
        for parte in partes:
            try:
                numero = float(parte)
                if numero < 0:
                    print("Revise que ninguno de los datos sea negativo.")
                    break
                numeros.append(numero)
            except:
                print("ERROR: Ingrese números válidos.")
                break
        else:
            if numeros:
                return numeros
        print("Intente nuevamente.")


def menu_principal():
    print("Test de Wilcoxon para muestras relacionadas")

    while True:
        print("-" * 50)
        print("Menú Principal")
        print("1. Ingresar mis propios datos")
        print("2. Ejemplo: 10 observaciones (muestra pequeña)")
        print("3. Ejemplo: 27 observaciones (muestra mediana)")
        print("4. Ejemplo: 35 observaciones (muestra grande)")
        print("5. Salir")
        print("-" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("-" * 20)
            print("Registro de datos")
            print("-" * 20)

            sin_musica = leer_muestra("Valores de la primera condición:")
            con_rock = leer_muestra("Valores de la segunda condición:")

            if len(sin_musica) == len(con_rock):
                test_wilcoxon(sin_musica, con_rock)
            else:
                print("Debe ingresar muestras del mismo tamaño.")

        elif opcion == "2":
            print("\n" + "-" * 20)
            print("Ejemplo: 10 observaciones")
            print("-" * 20)

            sin_musica = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
            con_rock = [12, 14, 13, 15, 11, 16, 12, 14, 13, 15]
            test_wilcoxon(sin_musica, con_rock)

        elif opcion == "3":
            print("\n" + "-" * 20)
            print("Ejemplo: 27 observaciones")
            print("-" * 20)

            sin_musica = [14, 16, 15, 18, 17, 19, 15, 16, 17, 20, 18, 19,
                          16, 17, 15, 21, 19, 18, 17, 16, 20, 19, 18, 17,
                          16, 15, 14]
            con_rock = [16, 14, 17, 20, 15, 22, 17, 14, 19, 22, 20,
                        21, 18, 19, 17, 23, 21, 20, 19, 18, 22, 21,
                        20, 19, 18, 17, 16]
            test_wilcoxon(sin_musica, con_rock)

        elif opcion == "4":
            print("\n" + "-" * 20)
            print("Ejemplo: 35 observaciones")
            print("-" * 70)

            sin_musica = [38, 42, 35, 45, 40, 39, 44, 37, 41, 43,
                          36, 39, 42, 38, 45, 40, 37, 44, 39, 41,
                          43, 36, 40, 38, 45, 42, 37, 44, 39, 41,
                          40, 43, 38, 42, 39]
            con_rock = [41, 45, 38, 48, 43, 42, 47, 40, 44, 46,
                        39, 42, 45, 41, 48, 43, 40, 47, 42, 44,
                        46, 39, 43, 41, 48, 45, 40, 47, 42, 44,
                        43, 46, 41, 45, 42]
            test_wilcoxon(sin_musica, con_rock)

        elif opcion == "5":
            print("\n" + "-" * 20)
            print("Finalizando el programa...")
            print("-" * 20)
            break

        else:
            print("\nOpción no valida.")

# Ejecutar el programa
if __name__ == "__main__":
    menu_principal()
