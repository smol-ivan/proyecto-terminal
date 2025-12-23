import numpy as np
import random

from models import Particula
from utils import get_matriz_covarianza

INERCIA = 0.7


def funcion_objetivo(
    posicion,
    retornos_medios,
    matriz_covarianza,
    modo,
    valor_objetivo=None,
    penalizacion=1e6,
):
    """
    Calcula el valor de la funcion objetivo para una posicion dada.

    Args:
        posicion (np.array): Vector de pesos de los activos en el portafolio.
        retornos_medios (np.array): Retornos medios de los activos.
        matriz_covarianza (np.array): Matriz de covarianza de los activos.
        modo (str): 'minimizar_riesgo' o 'maximizar_ganancia'.
        valor_objetivo(float, optional): El retorno minimo esperado o el reisgo maximo permitido.
        penalizacion (float, optional): Un factor de penalizacion
    """
    retorno_portafolio = np.dot(posicion, retornos_medios)
    varianza_portafolio = np.dot(posicion.T, np.dot(matriz_covarianza, posicion))

    if modo == "minimizar_riesgo":
        # Minimizar el reisgo sujeto a un retorno minimo esperado
        objetivo = varianza_portafolio
        if valor_objetivo is not None:
            if retorno_portafolio < valor_objetivo:
                objetivo += penalizacion * (valor_objetivo - retorno_portafolio) ** 2
        return objetivo
    elif modo == "maximizar_ganancia":
        # Maximizar la ganancia sujeto a un riesgo maximo
        objetivo = -retorno_portafolio
        if valor_objetivo is not None:
            if varianza_portafolio > valor_objetivo:
                objetivo += penalizacion * (varianza_portafolio - valor_objetivo) ** 2
        return objetivo
    elif modo == "minimizar_varianza":
        return varianza_portafolio
    else:
        raise ValueError("Modo incorrecto")


def actualizar_velocidad(
    particula, best_global_pos, cfg, retornos_medios, matriz_covarianza
):
    """Actualiza la velocidad y la posicion de una particula"""
    r1 = random.random()
    r2 = random.random()

    inercia = INERCIA * particula.velocidad
    comp_cognitivo = cfg.c1 * r1 * (particula.best_personal_pos - particula.posicion)
    comp_social = cfg.c2 * r2 * (best_global_pos - particula.posicion)

    particula.velocidad = inercia + comp_cognitivo + comp_social
    particula.posicion += particula.velocidad
    particula.posicion = normalizar(particula.posicion)

    # Evaluar nueva posicion
    nuevo_valor = funcion_objetivo(
        particula.posicion, retornos_medios, matriz_covarianza, cfg.modo
    )

    # Actualizar mejor posicion personal
    if nuevo_valor < particula.best_personal_val:
        particula.best_personal_val = nuevo_valor
        particula.best_personal_pos = particula.posicion.copy()


def inicializar_poblacion(
    n_activos, n_poblacion, retornos_medios, matriz_covarianza, modo
):
    poblacion = []
    for _ in range(n_poblacion):
        posicion = np.random.rand(n_activos)
        posicion = normalizar(posicion)
        velocidad = np.zeros(n_activos)
        valor_inicial = funcion_objetivo(
            posicion, retornos_medios, matriz_covarianza, modo
        )
        poblacion.append(Particula(posicion, velocidad, valor_inicial))
    return poblacion


def encontrar_mejor_particula(poblacion):
    if not poblacion:
        return None, float("inf")

    mejor_particula = min(poblacion, key=lambda p: p.best_personal_val)
    return mejor_particula.best_personal_pos, mejor_particula.best_personal_val


def normalizar(posicion):
    # Poner los pesos negativos a cero
    posicion = np.maximum(0, posicion)

    # Normalizar cada peso
    suma_total = np.sum(posicion)
    if suma_total > 0:
        posicion /= suma_total

    return posicion


def pso(cfg, n_activos, activos, correlaciones):
    # Precalculo de matriz de covarianza y retornos medios
    matriz_covarianza = get_matriz_covarianza(n_activos, activos, correlaciones)
    retornos_medios = np.array([float(a.mean_return) for a in activos])

    poblacion = inicializar_poblacion(
        n_activos,
        cfg.n_poblacion,
        retornos_medios,
        matriz_covarianza,
        cfg.modo,
    )
    best_global_position, best_global_val = encontrar_mejor_particula(poblacion)

    # Historial de puntos (riesgo, retorno) por iteración
    historial = []

    for i in range(cfg.max_iter):
        for particula in poblacion:
            actualizar_velocidad(
                particula,
                best_global_position,
                cfg,
                retornos_medios,
                matriz_covarianza,
            )

        best_iter_position, best_iter_val = encontrar_mejor_particula(poblacion)

        # Actualizar si es necesario el valor global
        if best_iter_val > best_global_val:
            best_global_position = best_iter_position
            best_global_val = best_iter_val

        # Guardar puntos de esta iteracion al historial
        for p in poblacion:
            retorno = float(np.dot(p.posicion, retornos_medios))
            riesgo = float(np.dot(p.posicion.T, np.dot(matriz_covarianza, p.posicion)))
            historial.append((riesgo, retorno))

    return best_global_position, best_global_val, poblacion, historial
