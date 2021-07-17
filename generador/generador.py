
from typing import Final

from Utils.arbol import ArbolSintaxisAbstracta

from Generador.visitadores import VisitantePython


class Generador:

    
    LIB_ESTANDAR: Final = "from Lib.estandar import *"

    asa            : ArbolSintaxisAbstracta
    visitador      : VisitantePython


    def __init__(self, nuevo_asa: ArbolSintaxisAbstracta):

        self.asa            = nuevo_asa
        self.visitador      = VisitantePython() 

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def generar(self):
        resultado = self.visitador.visitar(self.asa.raiz)
        print(self.LIB_ESTANDAR)
        print(resultado)
