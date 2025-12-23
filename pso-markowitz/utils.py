import numpy as np

from models import Asset, ProblemData


def get_matriz_covarianza(n_activos, activos, correlaciones):
    matriz_covarianza = np.zeros((n_activos, n_activos))
    desviaciones = np.array([float(a.standard_deviation) for a in activos])

    for i in range(n_activos):
        for j in range(n_activos):
            if i == j:
                matriz_covarianza[i, j] = desviaciones[i] ** 2
            else:
                correlacion = correlaciones.get((i + 1, j + 1), 0)
                matriz_covarianza[i, j] = (
                    desviaciones[i] * desviaciones[j] * correlacion
                )

    return matriz_covarianza


def leer_prueba(filepath):
    """
    Return
    n_activos -> int
    activos -> [Asset]
    correlaciones -> dict
    """
    with open(filepath) as f:
        # Definicion de activos
        n_activos = int(f.readline())
        activos = []
        correlaciones = {}

        # Lista de activos
        for i in range(n_activos):
            linea = f.readline().split()
            # linea = [Rendimiento promedio, desviacion estandar]
            activo = Asset(linea[0], linea[1], i + 1)
            activos.append(activo)

        # Correlaciones
        while True:
            line = f.readline().split()
            if not line:
                print("Archivo leido por completo")
                break

            # linea = [id_activo_i, id_activo_j, correlacion]
            i, j, value = int(line[0]), int(line[1]), float(line[2])

            correlaciones[(i, j)] = value
            correlaciones[(j, i)] = value

        data = ProblemData(n_activos, activos, correlaciones)

        return data
