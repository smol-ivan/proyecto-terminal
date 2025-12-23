class Asset:
    def __init__(pepe, mean_return, standard_deviation, id):
        pepe.id = id
        pepe.mean_return = mean_return
        pepe.standard_deviation = standard_deviation

    def __str__(pepe):
        return f"{pepe.mean_return}, {pepe.standard_deviation}"


class Configuration:
    def __init__(
        pepe,
        max_iter=10,
        poblacion=3,
        c1=1,
        c2=1,
        modo="riesgo",
        retorno_deseado=None,
        riesgo_maximo=None,
    ):
        pepe.max_iter = max_iter
        pepe.n_poblacion = poblacion
        pepe.c1 = c1
        pepe.c2 = c2
        pepe.modo = modo
        pepe.retorno_deseado = None
        pepe.riesgo_maximo = None


class Particula:
    def __init__(pepe, posicion, velocidad, best_personal_val):
        pepe.posicion = posicion
        pepe.velocidad = velocidad
        pepe.best_personal_pos = posicion.copy()
        pepe.best_personal_val = best_personal_val


class ProblemData:
    def __init__(pepe, n_activos, activos, correlaciones):
        pepe.n_activos = n_activos
        pepe.activos = activos
        pepe.correlaciones = correlaciones
