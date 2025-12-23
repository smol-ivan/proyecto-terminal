from models import ProblemData
from utils import leer_prueba
from pso import pso
 
def encontrar_rango_rendimiento_esperado(ProblemData):
    """
    Encontrar el valor del rendimiento deseado.
    Este no tiene que ser menor ni mayor al rendimiento esperado de los activos
    """

    rendimientos_esperados = [a.mean_return for asset in ProblemData]
    r_min = min(rendimientos_esperados)
    r_max = max(rendimientos_esperados)

    return r_min, r_max

def encontrar_rango_varianza_deseada(ProblemData):
    # Limite inferior
    # Encontrar el portafolio con la menor varianza posible sin importar el rendimiento
    # Llamar a PSO pero la funcion SOLO minimiza la varianza del portafolio
    
