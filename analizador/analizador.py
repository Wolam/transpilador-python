from typing import List, NoReturn

from Explorador.explorador import ComponenteLexico
from Utils.arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo


class Analizador:
    """
    Clase encargada de revisar las reglas de gramatica
    en el programa con el uso del arbol de sintaxis y el
    algoritmo de descenso recursivo.
    """

    componentes_lexicos: List[ComponenteLexico]
    componente_actual: ComponenteLexico
    ast: ArbolSintaxisAbstracta
    cantidad_componentes: int
    posicion_componente_actual: int

    def __init__(self, lista_componentes):

        self.componentes_lexicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posicion_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.ast = ArbolSintaxisAbstracta()

    def imprimir_ast(self) -> None:
        """
        Imprime el árbol de sintáxis abstracta
        """

        if self.ast.raiz is None:
            print([])
        else:
            self.ast.imprimir_preorden()

    def analizar(self) -> None:
        self.ast.raiz = self.__analizar_programa()

    def __analizar_programa(self) -> Nodo:
        """
        Programa ::= Comentario Asignación* (Comentario | Funcion)* Principal
        """

        nodos_nuevos = []

        # Esto es porque pueden venir varias asignaciones y funciones
        while (True):

            # Es asignacion
            if self.componente_actual.tipo == 'IDENTIFICADOR':
                nodos_nuevos += [self.__analizar_asignacion()]

            # Es función
            elif self.componente_actual.valor == 'POV':
                nodos_nuevos += [self.__analizar_funcion()]

            else:
                break

        # Verifica que venga la función principal obligatoria
        if (self.componente_actual.valor == 'maracuya'):
            nodos_nuevos += [self.__analizar_principal()]
        else:
            self.__error_verificacion_texto('maracuya')

        return Nodo(TipoNodo.PROGRAMA, nodos=nodos_nuevos)

    def __analizar_asignacion(self) -> Nodo:
        """
        Asignación ::= Identificador anotado
        (Valor | Invocación | ExpresiónMatematica).
        """

        nodos_nuevos = []

        # Identificador obligatorio
        nodos_nuevos += [self.__verificar_identificador()]

        # anotado obligatorio
        self.__verificar('anotado')

        # Verifica si trae un valor, una invocación o una expresión
        # matemática como la expresión, la invocación y el valor
        # pueden iniciar por un identificador se revisa el
        # siguiente componente para las validaciones

        tipos_de_variable = {'ENTERO', 'FLOTANTE', 'BOOLEANO',
                             'TEXTO', 'IDENTIFICADOR'}

        # Caso Expresión Matemática
        if self.componente_actual.valor == '#':
            nodos_nuevos += [self.__analizar_expresion_matematica()]

        # Caso Invocacion
        elif self.componente_actual.tipo == 'INVOCACION':
            nodos_nuevos += [self.__analizar_invocacion()]

        # Caso Valor
        elif self.componente_actual.tipo in tipos_de_variable:
            nodos_nuevos += [self.__analizar_valor()]

        # Un punto obligatorio
        self.__verificar('.')

        return Nodo(TipoNodo.ASIGNACION, nodos=nodos_nuevos)

    def __analizar_invocacion(self) -> Nodo:
        """
        Invocación ::= jutsu Identificador(Parámetros?)
        """

        nodos_nuevos = []

        # verifica jutsu
        self.__verificar('jutsu')
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        if self.componente_actual.tipo != "PUNTUACION":
            nodos_nuevos += [self.__analizar_parametros_funcion()]
        self.__verificar(')')

        return Nodo(TipoNodo.INVOCACION,
                    contenido=nodos_nuevos[0].contenido, nodos=nodos_nuevos)

    def __analizar_funcion(self) -> Nodo:
        """
        Función ::= POV Identificador(Parámetros?) xD ConjuntoInstrucciones v:
        """

        nodos_nuevos = []

        # Verifica POV
        self.__verificar('POV')

        # Identificador obligatorio
        nodos_nuevos += [self.__verificar_identificador()]

        # Verifica parametros
        self.__verificar('(')
        if self.componente_actual.tipo != "PUNTUACION":
            nodos_nuevos += [self.__analizar_parametros_funcion()]
        self.__verificar(')')

        # Verifica corchetes
        self.__verificar('xD')

        # Analizar instruccion
        nodos_nuevos += [self.__analizar_conjunto_instrucciones()]

        # Verifica corchetes
        self.__verificar('v:')

        return Nodo(TipoNodo.FUNCION,
                    contenido=nodos_nuevos[0].contenido, nodos=nodos_nuevos)

    def __analizar_principal(self) -> Nodo:
        """
        Principal::= maracuya() xD ConjuntoInstrucciones v:
        """

        nodos_nuevos = []
        atributos_nuevos = self.componente_actual.get_atributos()

        # Verifica que sea la principal
        self.__verificar('maracuya')
        self.__verificar('(')
        self.__verificar(')')

        # Verifica corchetes
        self.__verificar('xD')

        # Si es instruccion
        nodos_nuevos += [self.__analizar_conjunto_instrucciones()]

        # Verifica corchetes
        self.__verificar('v:')

        return Nodo(TipoNodo.PRINCIPAL, nodos=nodos_nuevos,
                    atributos=atributos_nuevos)

    def __analizar_parametros_funcion(self) -> Nodo:
        """
        ParámetrosFuncion::= Identificador (, Identificador)*
        """

        nodos_nuevos = []

        # Verifica el primer valor
        nodos_nuevos += [self.__verificar_identificador()]

        # Como puede traer varios parametros se revisa hasta que no hayan comas
        while(self.componente_actual.valor == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__verificar_identificador()]

        return Nodo(TipoNodo.PARAMETROS_FUNCION, nodos=nodos_nuevos)

    def __analizar_parametros_invocacion(self) -> Nodo:
        """
        ParámetrosInvocacion::= Valor (, Valor)*
        """

        nodos_nuevos = []

        # Verifica el primer valor
        nodos_nuevos += [self.__analizar_valor()]

        # Como puede traer varios parametros se revisa hasta que no hayan comas
        while(self.componente_actual.valor == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__analizar_valor()]

        return Nodo(TipoNodo.PARAMETROS_INVOCACION, nodos=nodos_nuevos)

    def __verificar_identificador(self) -> Nodo:
        """
        Verifica si el tipo del componente léxico actual es de tipo
        IDENTIFICADOR

        Identificador ::= [A-Za-z_][A-Za-z_0-9]+
        """

        # Se verifica el tipo de componente
        self.__verificar_tipo_componente('IDENTIFICADOR')
        nodo = Nodo(TipoNodo.IDENTIFICADOR,
                    contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())

        self.__siguiente_componente()
        return nodo

    def __analizar_instruccion(self) -> Nodo:
        """
        Instrucciones ::= Asignación | Repetir |
                          Condicional | Comentario | Retorno
        """

        nodos_nuevos = []

        # Se verifica que tipo de instrucción se está enviando para validarla
        if self.componente_actual.valor == 'whenCuando':
            nodos_nuevos += [self.__analizar_repetir()]

        elif self.componente_actual.tipo == 'IDENTIFICADOR':
            nodos_nuevos += [self.__analizar_asignacion()]

        elif self.componente_actual.valor == 'siuuu':
            nodos_nuevos += [self.__analizar_condicional()]

        elif self.componente_actual.valor == 'messirve':
            nodos_nuevos += [self.__analizar_retorno()]

        return Nodo(TipoNodo.INSTRUCCION, nodos=nodos_nuevos)

    def __analizar_repetir(self) -> Nodo:
        """
        Repetir ::= whenCuando xD ConjuntoInstrucciones but (ExpCondicional) v:
        """

        nodos_nuevos = []

        # sólo se verifica la estructura de repetición
        self.__verificar('whenCuando')
        self.__verificar('xD')
        nodos_nuevos += [self.__analizar_conjunto_instrucciones()]
        self.__verificar('but')
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_expresion_condicional()]
        self.__verificar(')')
        self.__verificar('v:')
        return Nodo(TipoNodo.REPETIR, nodos=nodos_nuevos)

    def __analizar_condicional(self) -> Nodo:
        """
        Condicional::= Siuuu Nimodo?
        """

        nodos_nuevos = []

        # analiza el siuuu
        nodos_nuevos += [self.__analizar_siuuu()]

        # Como puede o no traer el else entonces lo validamos
        if self.componente_actual.valor == 'nimodo':
            nodos_nuevos += [self.__analizar_nimodo()]

        return Nodo(TipoNodo.CONDICIONAL, nodos=nodos_nuevos)

    def __analizar_siuuu(self):
        """
        Siuuu::= siuuu (ExpCondicional) xD Conjunto Instrucciones v:
        """
        
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('siuuu')
        self.__verificar('(')        
        nodos_nuevos += [self.__analizar_expresion_condicional()]
        self.__verificar(')')
        self.__verificar('xD')
        nodos_nuevos += [self.__analizar_conjunto_instrucciones()]
        self.__verificar('v:')

        return Nodo(TipoNodo.SIUUU, nodos=nodos_nuevos)

    def __analizar_nimodo(self):
        """
        Nimodo::=  nimodo xD ConjuntoInstrucciones v:
        """

        nodos_nuevos = []

        self.__verificar('nimodo')
        self.__verificar('xD')
        nodos_nuevos += [self.__analizar_conjunto_instrucciones()]
        self.__verificar('v:')

        return Nodo(TipoNodo.NIMODO, nodos=nodos_nuevos)


    def __analizar_conjunto_instrucciones(self) -> Nodo:
        """
        ConjuntoInstrucciones ::= Instruccion+
        """

        nodos_nuevos = []

        # Valida la primera instrucción
        nodos_nuevos += [self.__analizar_instruccion()]

        # Recorre todas las instrucciones dentro de una función
        # Las envía a verificar una por una
        instrucciones = {'whenCuando', 'siuuu', 'messirve'}
        while self.componente_actual.valor in instrucciones or\
                self.componente_actual.tipo == 'IDENTIFICADOR':

            nodos_nuevos += [self.__analizar_instruccion()]

        return Nodo(TipoNodo.CONJUNTO_INSTRUCCIONES, nodos=nodos_nuevos)

    def __analizar_expresion_condicional(self) -> Nodo:
        """
        ExpCondicional ::= Comparación(OperadorLogico Comparación)?
        """

        nodos_nuevos = []

        # Verifica la comparación
        nodos_nuevos += [self.__analizar_comparacion()]

        # Se valida si trae operador lógico y se manda a verificar
        if self.componente_actual.tipo == 'OPERADOR_LOGICO':
            nodos_nuevos += [self.__verificar_operador_logico()]
            nodos_nuevos += [self.__analizar_comparacion()]

        return Nodo(TipoNodo.EXPRESION_CONDICIONAL, nodos=nodos_nuevos)

    def __analizar_comparacion(self) -> Nodo:
        """
        Comparación::= Valor Comporador Valor
        """

        nodos_nuevos = []

        # Se verifica la estructura de comparación
        nodos_nuevos += [self.__analizar_valor()]
        nodos_nuevos += [self.__verificar_comparador()]
        nodos_nuevos += [self.__analizar_valor()]
        return Nodo(TipoNodo.COMPARACION, nodos=nodos_nuevos)

    def __analizar_retorno(self) -> Nodo:
        """
        Retorno: := messirve Valor?.
        """

        nodos_nuevos = []

        # Palabra clave obligatoria
        self.__verificar('messirve')

        tipos_de_variable = {'IDENTIFICADOR', 'ENTERO', 'FLOTANTE',
                             'BOOLEANO', 'TEXTO'}

        if self.componente_actual.tipo in tipos_de_variable:
            nodos_nuevos += [self.__analizar_valor()]

        # Punto obligatorio
        self.__verificar('.')
        return Nodo(TipoNodo.RETORNO, nodos=nodos_nuevos)

    def __analizar_valor(self) -> Nodo:
        """
        Valor : := Literal | Identificador
        """

        # Se revisa si corresponde a un identificador o un literal
        if self.componente_actual.tipo == 'IDENTIFICADOR':
            nodo = self.__verificar_identificador()

        else:
            nodo = self.__analizar_literal()

        return nodo

    def __analizar_literal(self) -> Nodo:
        """
        Literal ::= Texto|Entero|Flotante|Booleano
        """

        # Se verifica el tipo de literal y se manda al
        # verificar correspondiente
        if self.componente_actual.tipo == 'ENTERO':
            nodo = self.__verificar_entero()

        elif self.componente_actual.tipo == 'FLOTANTE':
            nodo = self.__verificar_flotante()

        elif self.componente_actual.tipo == 'BOOLEANO':
            nodo = self.__verificar_booleano()

        elif self.componente_actual.tipo == 'TEXTO':
            nodo = self.__verificar_texto()

        return nodo

    def __verificar_entero(self) -> Nodo:
        """
        Entero::= -?[0-9]+
        """

        self.__verificar_tipo_componente('ENTERO')

        nodo = Nodo(TipoNodo.ENTERO, contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar_flotante(self) -> Nodo:
        """
        Flotante::= -?[0-9]+;[0-9]+
        """

        self.__verificar_tipo_componente('FLOTANTE')

        nodo = Nodo(TipoNodo.FLOTANTE, contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar_booleano(self) -> Nodo:
        """
        Booleano::= SIUA|NOUA
        """

        self.__verificar_tipo_componente('BOOLEANO')

        nodo = Nodo(TipoNodo.BOOLEANO, contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar_texto(self) -> Nodo:
        """
        Texto ::= ツ.*ツ
        """

        self.__verificar_tipo_componente('TEXTO')

        nodo = Nodo(TipoNodo.TEXTO, contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar_tipo_componente(self, tipo_componente_esperado) -> None:

        # Error sintactico si no son de tipo equivalentes
        if self.componente_actual.tipo != tipo_componente_esperado:
            self.__error_verificacion_tipo(tipo_componente_esperado)

    def __siguiente_componente(self) -> None:
        """
        Pasa al siguiente componente léxico de la lista
        """

        # Recorre los componentes hasta llegar a su cantidad máxima
        self.posicion_componente_actual += 1

        if self.posicion_componente_actual >= self.cantidad_componentes:
            return

        self.componente_actual =\
            self.componentes_lexicos[self.posicion_componente_actual]

    def __analizar_expresion_matematica(self) -> Nodo:
        """
        ExpresionMatematica::= #Valor (Operador Valor)*#
        """

        nodos_nuevos = []

        self.__verificar('#')

        # Se verifica el primer valor
        nodos_nuevos += [self.__analizar_valor()]

        # Como pueden o no estar se validan mientras siga un operador
        while(self.componente_actual.tipo == 'OPERADOR'):

            nodos_nuevos += [self.__verificar_operador()]
            nodos_nuevos += [self.__analizar_valor()]

        self.__verificar('#')

        return Nodo(TipoNodo.EXPRESION_MATEMATICA, nodos=nodos_nuevos)

    def __verificar_operador(self) -> Nodo:
        """
        Operador::= bobMar | bobStar | bobiDir | bobTiplicar
        """

        self.__verificar_tipo_componente('OPERADOR')

        nodo = Nodo(TipoNodo.OPERADOR, contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar_operador_logico(self) -> Nodo:
        """
        OperadorLogico::= aja | ayno
        """

        self.__verificar_tipo_componente('OPERADOR_LOGICO')

        nodo = Nodo(TipoNodo.OPERADOR_LOGICO,
                    contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
                    
        self.__siguiente_componente()

        return nodo

    def __verificar_comparador(self) -> Nodo:
        """
        Comparador ::= chikito | tapotente | panapotente |
                        panachikito | nolocrick | panas
        """

        self.__verificar_tipo_componente('COMPARADOR')

        nodo = Nodo(TipoNodo.COMPARADOR,
                    contenido=self.componente_actual.valor,
                    atributos=self.componente_actual.get_atributos())
        self.__siguiente_componente()

        return nodo

    def __verificar(self, texto_esperado: str) -> None:
        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """

        # Error sintactico si no tienen el mismo contenido
        if self.componente_actual.valor != texto_esperado:
            self.__error_verificacion_texto(texto_esperado)

        self.__siguiente_componente()

    def __error_verificacion_texto(self, texto_esperado: str) -> NoReturn:
        """
        Levanta un error de sintaxis si no empareja un texto esperado
        con el texto del componenete actual
        """

        texto_encontrado = self.componente_actual.valor
        linea, columna = self.componente_actual.get_atributos().values()
        print(f'Texto esperado: {texto_esperado!r} ' +
              f'texto encontrado : {texto_encontrado!r} ' +
              f'(Linea {linea}, Columna {columna})')

        raise SyntaxError('Error de verificacion de texto en analizador')

    def __error_verificacion_tipo(self, tipo_esperado: str) -> NoReturn:
        """
        Levanta un error de sintaxis si no empareja un tipo esperado
        con el tipo del componente actual
        """

        tipo_encontrado = self.componente_actual.tipo
        linea, columna = self.componente_actual.get_atributos().values()
        print(f'Tipo esperado: {tipo_esperado!r} ' +
              f'tipo encontrado : {tipo_encontrado!r} ' +
              f'(Linea {linea}, Columna {columna})')

        raise SyntaxError('Error de verificacion de tipos en analizador')
