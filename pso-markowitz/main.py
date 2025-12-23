import argparse
import numpy as np
from datetime import datetime

from models import Configuration
from utils import leer_prueba, get_matriz_covarianza
from pso import pso
import plotting


def main():
    parser = argparse.ArgumentParser(description="PSO Markowitz - visualizador")
    parser.add_argument(
        "--out", type=str, default=None, help="Ruta CSV para guardar poblacion final"
    )
    parser.add_argument(
        "--img",
        type=str,
        default="pareto_plot.png",
        help="Ruta para guardar imagen PNG (default: pareto_plot.png)",
    )
    args = parser.parse_args()

    dp = leer_prueba("data-files/port1.txt")

    cfg = Configuration()
    cfg.max_iter = 50
    cfg.n_poblacion = 10
    cfg.c1 = 1.5
    cfg.c2 = 1.5
    cfg.modo = "minimizar_riesgo"
    cfg.retorno_deseado = 0.7

    best_pos, best_val, poblacion, historial = pso(
        cfg, dp.n_activos, dp.activos, dp.correlaciones
    )

    print("Mejor solucion encontrada:")
    print(best_pos)
    print("Valor de la funcion objetivo:")
    print(best_val)
    print("Poblacion final:")
    for p in poblacion:
        print(p.posicion, p.best_personal_val)

    # Preparar datos para trazado
    matriz_covarianza = get_matriz_covarianza(
        dp.n_activos, dp.activos, dp.correlaciones
    )
    retornos_medios = np.array([float(a.mean_return) for a in dp.activos])

    if args.out:
        import csv

        with open(args.out, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [f"peso_{i}" for i in range(dp.n_activos)] + ["return", "risk"]
            )
            for p in poblacion:
                retorno = float(np.dot(p.posicion, retornos_medios))
                var = float(np.dot(p.posicion.T, np.dot(matriz_covarianza, p.posicion)))
                writer.writerow(list(p.posicion) + [retorno, var])
        print(f"Poblacion guardada en {args.out}")

    # Generar y guardar grafico
    plotting.plot_population_with_history(
        poblacion,
        historial,
        retornos_medios,
        matriz_covarianza,
        best_pos=best_pos,
        savefile=args.img,
    )
    print(f"Frente de Pareto visualizado y guardado en {args.img}")


if __name__ == "__main__":
    main()
