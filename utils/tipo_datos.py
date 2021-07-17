from enum import Enum, auto

class TipoDato(Enum):
    """
    Enum que contiene categorías a utilizar en verificador
    """
    TEXTO = auto()
    NUMERO = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    BOOLEANO = auto()
    CUALQUIERA = auto()
    COMPARADOR_LOGICO = auto()
    NINGUNO = auto()
