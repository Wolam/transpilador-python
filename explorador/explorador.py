import re
from enum import Enum
from typing import List, NamedTuple


class DescriptorComponente(Enum):
    """
    Esta clase contiene el enum con los descriptores de
    componentes del compilador
    """
    
    ERROR_ID = r'[0-9;]+[_A-Za-z]+'
    COMENTARIO = r'muchoTexto:.*'  # Comentarios del lenguaje
    TEXTO = r'ツ.*ツ'  # Tipos de dato string
    PUNTUACION = r'(xD|v:|\(|\)|\.|\,|\#)'  # Parámetros y fin de expresiones
    FLOTANTE = r'(-?[0-9]+;[0-9]+)'  # Numeros punto flotante
    ENTERO = r'(-?[0-9]+)'  # Tipos entero negativos o positivos
    IDENTIFICADOR = r'[A-Za-z_][A-Za-z_0-9]*'  # Identificadores alfanumericos
    NUEVALINEA = r'\n'         # Fines de linea en lenguaje
    ESPACIO = r'[ \t]+'       # Omitir espacios o tabs
    ERROR = r'.'         # Cualquier otro carácter

    # Diccionario con los identificadores reservados del lenguaje
    RESERVADOS = {
        'PALABRA_CLAVE': {'POV', 'maracuya', 'messirve'},
        'OPERADOR': {'bobMar', 'bobStar', 'bobiDir', 'bobTiplicar'},
        'COMPARADOR': {'chikito', 'tapotente', 'panachikito',
                       'panapotente', 'nolocrick', 'panas'},
        'OPERADOR_LOGICO': {'aja', 'ayno'},
        'CONDICIONAL': {'siuuu', 'nimodo'},
        'CICLO': {'whenCuando', 'but'},
        'ASIGNACION': {'anotado'},
        'INVOCACION': {'jutsu'},
        'BOOLEANO': {'SIUA','NOUA'}
    }

    def __str__(self):
        """
        Devuelve el descriptor con su nombre de grupo
        """

        return f'(?P<{self.name}>{self.value})'


class ComponenteLexico(NamedTuple):
    """
    Clase que almacena información del componente léxico
    """

    tipo: str
    valor: str
    linea: int
    columna: int

    def __str__(self):
        """
        Formato para imprimir el componente léxico
        """

        componente = f'{self.tipo:30} --> {self.valor:10} \
                        (Linea: {self.linea} , Columna: {self.columna})'
        return componente

    def get_atributos(self) -> dict:
        """
        Devuelve atributos del componente léxico en un diccionario
        """

        return {'linea':self.linea, 
                'columna':self.columna}


class Explorador:
    """
    Clase encargada de llevar a cabo la exploración,
    y separa el código en componentes léxicos
    """

    texto: str
    componentes: List[ComponenteLexico]
    cantidad_errores: int

    def __init__(self, contenido_archivo: str):
        self.texto = contenido_archivo
        self.componentes = []
        self.cantidad_errores = 0

    def imprimir_componentes(self) -> None:
        """
        Imprime los componentes junto con su número de línea y columna
        """

        for componente in self.componentes:
            print(componente)

    def explorar(self) -> None:
        """
        Define los componentes léxicos tokenizando el texto
        """

        self.componentes = self.__tokenizar_componentes()
        if self.cantidad_errores > 0:
            raise SyntaxError(f'{self.cantidad_errores} ' +
                              f'Error(es) en explorador')

    def __tokenizar_componentes(self) -> List[ComponenteLexico]:
        """
        Toma el texto y los procesa extrayendo los componentes léxicos
        """

        componentes = []
        num_linea = 1
        inicio_linea = 0

        # concatenar los regexp en un string a exepcion del dicc de reservados
        regexps = '|'.join(str(desc)
                           for desc in list(DescriptorComponente)
                           if desc != DescriptorComponente.RESERVADOS)

        # recorre el texto y va emparejando con la expresiones regulares
        for coincidencia in re.finditer(regexps, self.texto):
            tipo_coincidencia = coincidencia.lastgroup
            valor = coincidencia.group()
            columna = coincidencia.start() - inicio_linea + 1

        # verifica si hay un cambio de línea para continuar con la siguente
            if tipo_coincidencia == 'NUEVALINEA':
                inicio_linea = coincidencia.end()
                num_linea += 1
                continue

        # ignora los espacios y comentarios
            elif tipo_coincidencia == 'ESPACIO' or \
                    tipo_coincidencia == 'COMENTARIO':
                continue

        # asignar el tipo de indentificador si es reservado
            elif tipo_coincidencia == 'IDENTIFICADOR':
                tipo_coincidencia = self.__asignar_coincidencia_tipo_id(valor)

        # devuelve error en caso que no sea ningún componente léxico valido
            elif tipo_coincidencia.startswith('ERROR'):
                self.__error_componente(valor, num_linea, columna)

            componentes.append(
                ComponenteLexico(tipo_coincidencia, valor, num_linea, columna))

        return componentes

    def __asignar_coincidencia_tipo_id(self, valor: str) -> str:
        """
        El valor se refiere a una coincidencia de tipo identificador

        Busca la coincidencia en el diccionario de identificadores
        reservados y lo retorna el tipo de identificador correspondiente
        (por defecto es IDENTIFICADOR)
        """

        predeterminado = "IDENTIFICADOR"
        miembro_resv = DescriptorComponente.RESERVADOS
        dicc_resv = miembro_resv.value.items()
        for tipo_id_resv, valores_resv in dicc_resv:
            # si es un identificador reservado devolver su tipo
            if valor in valores_resv:
                return tipo_id_resv
        return predeterminado

    def __error_componente(self, valor: str,
                           linea: int, columna: int) -> None:
        """
        Imprime un error de componente lexico si no empareja un valor con
        algún componente y levanta la bandera de error
        """

        self.cantidad_errores += 1
        print(f'Componente no identificado: {valor!r} ' +
              f'(Linea {linea}, Columna {columna})')
