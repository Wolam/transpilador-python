from Utils.arbol import Nodo

class Registro:
    """
    Almacenar la informacion auxiliar especifica de una variable
    con el fin de revisar su alcance en el programa. 
    """

    nombre: str
    profundidad: int
    referencia: Nodo

    def __init__(self, profundidad, referencia) -> None:
        """
        Constructor para clase de registro
        """
        self.nombre = referencia.contenido
        self.profundidad = profundidad
        self.referencia = referencia

    def __str__(self) -> str:
        """
        Formato opcional del registro si es necesario de imprimir en la
        tabla de simbolos
        """

        return f'nombre: {self.nombre:20} \
            profundidad:  {self.profundidad}, referencia: {self.referencia}'

    def get_nombre(self) -> str: 
        return self.nombre

    def get_profundidad(self) -> int:
        return self.profundidad

    def get_referencia(self) -> Nodo:
        return self.referencia
