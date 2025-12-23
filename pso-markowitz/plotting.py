import numpy as np
import matplotlib.pyplot as plt


def _compute_points(poblacion, retornos_medios, matriz_covarianza):
    risks = []
    returns = []
    for p in poblacion:
        r = float(np.dot(p.posicion, retornos_medios))
        v = float(np.dot(p.posicion.T, np.dot(matriz_covarianza, p.posicion)))
        returns.append(r)
        risks.append(v)
    return np.array(risks), np.array(returns)


def _pareto_mask(risks, returns):
    # Minimizar riesgo, maximizar retorno
    n = len(risks)
    mask = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # j domina i si riesgo_j <= riesgo_i y retorno_j >= retorno_i y al menos uno estricto
            if (risks[j] <= risks[i] and returns[j] >= returns[i]) and (
                (risks[j] < risks[i]) or (returns[j] > returns[i])
            ):
                mask[i] = False
                break
    return mask


def plot_population_with_history(
    poblacion,
    historial,
    retornos_medios,
    matriz_covarianza,
    best_pos=None,
    savefile=None,
):
    """Traza riesgo vs retorno: historial de toda la evolución + frente de Pareto acumulado.

    Args:
        poblacion (list): lista de Particula (poblacion final)
        historial (list): lista de tuplas (riesgo, retorno) de todas las iteraciones
        retornos_medios (np.array): vector de retornos medios
        matriz_covarianza (np.array): matriz de covarianza
        best_pos (np.array, optional): posición del mejor individuo global
        savefile (str, optional): ruta para guardar la figura
    """
    # Convertir historial a arrays
    if historial:
        hist_risks, hist_returns = zip(*historial)
        hist_risks = np.array(hist_risks)
        hist_returns = np.array(hist_returns)
    else:
        hist_risks = np.array([])
        hist_returns = np.array([])

    # Calcular puntos de la población final
    final_risks, final_returns = _compute_points(
        poblacion, retornos_medios, matriz_covarianza
    )

    # Frente de Pareto del historial acumulado
    all_risks = (
        np.concatenate([hist_risks, final_risks])
        if len(hist_risks) > 0
        else final_risks
    )
    all_returns = (
        np.concatenate([hist_returns, final_returns])
        if len(hist_returns) > 0
        else final_returns
    )
    pareto_mask = _pareto_mask(all_risks, all_returns)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Historial de toda la evolución (color claro)
    if len(hist_risks) > 0:
        ax.scatter(
            hist_risks,
            hist_returns,
            c="lightblue",
            alpha=0.3,
            s=20,
            label="Historial (todas iteraciones)",
        )

    # Población final (color más fuerte)
    ax.scatter(
        final_risks, final_returns, c="C0", alpha=0.7, s=50, label="Poblacion final"
    )

    # Frente de Pareto acumulado (borde rojo)
    ax.scatter(
        all_risks[pareto_mask],
        all_returns[pareto_mask],
        facecolors="none",
        edgecolors="red",
        s=100,
        linewidth=2,
        label="Frente de Pareto (acumulado)",
    )

    # Mejor solución global (estrella dorada)
    if best_pos is not None:
        best_r = float(np.dot(best_pos, retornos_medios))
        best_v = float(np.dot(best_pos.T, np.dot(matriz_covarianza, best_pos)))
        ax.scatter(
            [best_v],
            [best_r],
            c="gold",
            edgecolors="darkred",
            s=200,
            marker="*",
            label="Mejor global",
            zorder=5,
        )

    ax.set_xlabel("Riesgo (varianza)", fontsize=11)
    ax.set_ylabel("Retorno esperado", fontsize=11)
    ax.set_title(
        "Frontera Eficiente (PSO Markowitz) - Riesgo vs Retorno",
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if savefile:
        plt.savefig(savefile, dpi=150, bbox_inches="tight")
        print(f"Grafico guardado en {savefile}")

    return fig


def plot_population(
    poblacion,
    retornos_medios,
    matriz_covarianza,
    best_pos=None,
    show=True,
    savefile=None,
):
    """Traza riesgo vs retorno para la población final (compatibilidad hacia atrás).

    Args:
        poblacion (list): lista de Particula
        retornos_medios (np.array): vector de retornos medios
        matriz_covarianza (np.array): matriz de covarianza
        best_pos (np.array, optional): posición del mejor individuo global
        show (bool, optional): si True muestra la figura en pantalla
        savefile (str, optional): ruta para guardar la figura
    """
    risks, returns = _compute_points(poblacion, retornos_medios, matriz_covarianza)
    mask = _pareto_mask(risks, returns)

    plt.figure(figsize=(8, 6))
    plt.scatter(risks, returns, c="C0", label="Poblacion")
    # Front de Pareto marcado con borde
    plt.scatter(
        risks[mask],
        returns[mask],
        facecolors="none",
        edgecolors="r",
        s=100,
        label="Pareto front",
    )

    if best_pos is not None:
        best_r = float(np.dot(best_pos, retornos_medios))
        best_v = float(np.dot(best_pos.T, np.dot(matriz_covarianza, best_pos)))
        plt.scatter(
            [best_v],
            [best_r],
            c="gold",
            edgecolors="k",
            s=140,
            marker="*",
            label="Mejor global",
        )

    plt.xlabel("Riesgo (varianza)")
    plt.ylabel("Retorno esperado")
    plt.title("Riesgo vs Retorno - Poblacion final")
    plt.legend()
    plt.grid(True)

    if savefile:
        plt.tight_layout()
        plt.savefig(savefile, dpi=150)
        print(f"Grafico guardado en {savefile}")

    if show:
        plt.show()
