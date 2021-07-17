from copy import deepcopy
from enum import Enum, auto
from typing import List

from Utils.tipo_datos import TipoDato


class TipoNodo(Enum):
    """
    Describe el tipo de nodo del árbol  
    """

    PROGRAMA = auto()
    ASIGNACION = auto()
    FUNCION = auto()
    PRINCIPAL = auto()
    COMPARACION = auto()
    PARAMETROS_INVOCACION = auto()
    PARAMETROS_FUNCION = auto()
    IDENTIFICADOR = auto()
    CONJUNTO_INSTRUCCIONES = auto()
    INSTRUCCION = auto()
    REPETIR = auto()
    CONDICIONAL = auto()
    SIUUU = auto()
    NIMODO = auto()
    EXPRESION_CONDICIONAL = auto()
    RETORNO = auto()
    TEXTO = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    BOOLEANO = auto()
    EXPRESION_MATEMATICA = auto()
    OPERADOR = auto()
    OPERADOR_LOGICO = auto()
    COMPARADOR = auto()
    INVOCACION = auto()


class Nodo:
    """
    Clase que almacena la informacion de un componente lexico
    para que puedan ser agregados al arbol de sintaxis abstracta.
    """

    tipo: TipoNodo
    nodos: List['Nodo']
    contenido: str
    atributos: dict

    def __init__(self, tipo, contenido=None, nodos=[], atributos={}):
        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos
        self.atributos = deepcopy(atributos)
    
    # Metodo pendiente a revisar
    def visitar(self, visitante):
        return visitante.visitar(self)

    def __str__(self):
        """
        Formato para imprimir el nodo y su contenido
        """

        # Colocar la información del nombre del nodo
        res = f'{self.tipo.name}'

        # Colocar el contenido de texto del nodo
        if self.contenido is not None:
            res += f'  {self.contenido!r}'

        # Coloca los atributos de forma (llave : valor)
        if self.atributos != {}:
            for (llave,valor) in self.atributos.items():
                if isinstance(valor,TipoDato): valor = valor.name
                res += ' (%s : %s) ' % (llave,valor)
            res += '\n'          

        return res


class ArbolSintaxisAbstracta:
    """
    Clase encargada de almacenar todos los nodos del programa
    para realizar aplicar el analisis de descenso recursivo.
    """

    raiz: Nodo

    def imprimir_preorden(self) -> None:
        """
        Imprimir el preorden siempre toma la raiz del arbol
        """
        
        self.__preorden(self.raiz)

    def imprimir_nodo(self, nodo: Nodo, nivel: int) -> None:
        """
        Mostrar el nodo con un tabulado dado por el nivel
        """

        tabulado = ' ' * nivel * 3 + "|__" if self.raiz is not nodo else ""
        print(f'{tabulado}{nodo}')

    def __preorden(self, nodo: Nodo, nivel=0) -> None:
        """
        Imprimir los nodos con un tabulado especifico
            <Nodo Padre>
                    |_  <Nodo Hijo 1>
                    |_  <Nodo Hijo N>
        """
        self.imprimir_nodo(nodo, nivel)

        if nodo is not None:
            for nodo in nodo.nodos:
                self.__preorden(nodo, nivel=nivel+1)
