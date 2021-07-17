# Analizador solo gramática C MAMUTH

from typing import List, NoReturn

from Explorador.explorador import ComponenteLexico


class Analizador:
    """
    Clase encargada de revisar las reglas de gramatica
    en el programa
    """

    componentes_lexicos: List[ComponenteLexico]
    componente_actual: ComponenteLexico
    posicion_componente_actual: int
    cantidad_componentes: int

    def __init__(self, lista_componentes):
        self.componentes_lexicos = lista_componentes
        self.componente_actual = lista_componentes[0]
        self.cantidad_componentes = len(lista_componentes)
        self.posicion_componente_actual = 0

    def analizar(self) -> None:

        self.__analizar_programa()

    def __analizar_programa(self) -> None:
        """
        Programa ::= Comentario Asignación* (Comentario | Funcion)* Principal
        """

        # Esto es porque pueden venir varias asignaciones y funciones
        while (True):

            # Es asignacion
            if self.componente_actual.tipo == 'IDENTIFICADOR':
                self.__analizar_asignacion()

            # Es función
            elif self.componente_actual.valor == 'POV':
                self.__analizar_funcion()

            else:
                break

        # Verifica que venga la función principal obligatoria
        if (self.componente_actual.valor == 'maracuya'):
            self.__analizar_principal()
        else:
            self.__error_verificacion_texto('maracuya')

    def __analizar_asignacion(self) -> None:
        """
        Asignación ::= Identificador anotado
        (Valor | Invocación | ExpresiónMatematica).
        """

        # Identificador obligatorio
        self.__verificar_identificador()

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
            self.__analizar_expresion_matematica()

        # Caso Invocacion
        elif self.componente_actual.tipo == 'INVOCACION':
            self.__analizar_invocacion()

        # Caso Valor
        elif self.componente_actual.tipo in tipos_de_variable:
            self.__analizar_valor()

        # Un punto obligatorio
        self.__verificar('.')

    def __analizar_invocacion(self) -> None:
        """
        Invocación ::= jutsu Identificador(Parámetros)
        """

        self.__verificar_identificador()
        self.__verificar('(')
        self.__analizar_parametros()
        self.__verificar(')')

    def __analizar_funcion(self) -> None:
        """
        Función ::= POV Identificador(Parámetros) xD ConjuntoInstrucciones v:
        """

        # Verifica POV
        self.__verificar('POV')

        # Identificador obligatorio
        self.__verificar_identificador()

        # Verifica parametros
        self.__verificar('(')
        self.__analizar_parametros()
        self.__verificar(')')

        # Verifica corchetes
        self.__verificar('xD')

        # Analizar instruccion
        self.__analizar_conjunto_instrucciones()

        # Verifica corchetes
        self.__verificar('v:')

    def __analizar_principal(self) -> None:
        """
        Principal::= maracuya() xD ConjuntoInstrucciones v:
        """

        # Verifica que sea la principal
        self.__verificar('maracuya')
        self.__verificar('(')
        self.__verificar(')')

        # Verifica corchetes
        self.__verificar('xD')

        # Si es instruccion
        self.__analizar_conjunto_instrucciones()

        # Verifica corchetes
        self.__verificar('v:')

    def __analizar_parametros(self) -> None:
        """
        Parámetros::= Valor (, Valor)*
        """

        # Verifica el primer valor
        self.__analizar_valor()

        # Como puede traer varios parametros se revisa hasta que no hayan comas
        while(self.componente_actual.valor == ','):
            self.__verificar(',')
            self.__analizar_valor()

    def __verificar_identificador(self) -> None:
        """
        Verifica si el tipo del componente léxico actual es de tipo
        IDENTIFICADOR

        Identificador ::= [A-Za-z_][A-Za-z_0-9]+
        """

        # Se verifica el tipo de componente
        self.__verificar_tipo_componente('IDENTIFICADOR')

    def __analizar_instruccion(self) -> None:
        """
        Instrucciones ::= Asignación | Repetir |
                          Condicional | Comentario | Retorno
        """

        # Se verifica que tipo de instrucción se está enviando para validarla
        if self.componente_actual.valor == 'whenCuando':
            self.__analizar_repetir()

        elif self.componente_actual.tipo == 'IDENTIFICADOR':
            self.__analizar_asignacion()

        elif self.componente_actual.valor == 'siuuu':
            self.__analizar_condicional()

        elif self.componente_actual.valor == 'messirve':
            self.__analizar_retorno()

    def __analizar_repetir(self) -> None:
        """
        Repetir ::= whenCuando xD ConjuntoInstrucciones but (ExpCondicional) v:
        """

        # sólo se verifica la estructura de repetición
        self.__verificar('whenCuando')
        self.__verificar('xD')
        self.__analizar_conjunto_instrucciones()
        self.__verificar('but')
        self.__verificar('(')
        self.__analizar_expresion_condicional()
        self.__verificar(')')
        self.__verificar('v:')

    def __analizar_condicional(self) -> None:
        """
        Condicional::= siuuu (ExpCondicional) xD ConjuntoInstrucciones v:
                            (nimodo xD ConjuntoInstrucciones v:)?
        """

        # Se verifica la estructura condicional
        self.__verificar('siuuu')
        self.__verificar('(')
        self.__analizar_expresion_condicional()
        self.__verificar(')')
        self.__verificar('xD')
        self.__analizar_conjunto_instrucciones()
        self.__verificar('v:')

        # Como puede o no traer el else entonces lo validamos
        if self.componente_actual.valor == 'nimodo':
            self.__verificar('nimodo')
            self.__verificar('xD')
            self.__analizar_conjunto_instrucciones()
            self.__verificar('v:')

    def __analizar_conjunto_instrucciones(self) -> None:
        """
        ConjuntoInstrucciones ::= Instruccion+
        """

        # Valida la primera instrucción
        self.__analizar_instruccion()

        # Recorre todas las instrucciones dentro de una función
        # Las envía a verificar una por una
        instrucciones = {'whenCuando', 'siuuu', 'messirve'}
        while self.componente_actual.valor in instrucciones or\
                self.componente_actual.tipo == 'IDENTIFICADOR':

            self.__analizar_instruccion()

    def __analizar_expresion_condicional(self) -> None:
        """
        ExpCondicional ::= Comparación(OperadorLogico Comparación)?
        """

        # Verifica la comparación
        self.__analizar_comparacion()

        # Se valida si trae operador lógico y se manda a verificar
        if self.componente_actual.tipo == 'OPERADOR_LOGICO':
            self.__verificar_operador_logico()
            self.__analizar_comparacion()

    def __analizar_comparacion(self) -> None:
        """
        Comparación::= Valor Comporador Valor
        """

        # Se verifica la estructura de comparación
        self.__analizar_valor()
        self.__verificar_comparador()
        self.__analizar_valor()

    def __analizar_retorno(self) -> None:
        """
        Retorno: := messirve Valor?.
        """

        # Palabra clave obligatoria
        self.__verificar('messirve')

        tipos_de_variable = {'IDENTIFICADOR', 'ENTERO', 'FLOTANTE',
                             'BOOLEANO', 'TEXTO'}

        if self.componente_actual.tipo in tipos_de_variable:
            self.__analizar_valor()

        # Punto obligatorio
        self.__verificar('.')

    def __analizar_valor(self) -> None:
        """
        Valor : := Literal | Identificador
        """

        # Se revisa si corresponde a un identificador o un literal
        if self.componente_actual.tipo == 'IDENTIFICADOR':
            self.__verificar_identificador()

        else:
            self.__analizar_literal()

    def __analizar_literal(self) -> None:
        """
        Literal ::= Texto|Entero|Flotante|Booleano
        """

        # Se verifica el tipo de literal y se manda al
        # verificar correspondiente
        if self.componente_actual.tipo == 'ENTERO':
            self.__verificar_entero()

        elif self.componente_actual.tipo == 'FLOTANTE':
            self.__verificar_flotante()

        elif self.componente_actual.tipo == 'BOOLEANO':
            self.__verificar_booleano()

        elif self.componente_actual.tipo == 'TEXTO':
            self.__verificar_texto()

    def __verificar_entero(self) -> None:
        """
        Entero::= -?[0-9]+
        """

        self.__verificar_tipo_componente('ENTERO')

    def __verificar_flotante(self) -> None:
        """
        Flotante::= -?[0-9]+;[0-9]+
        """

        self.__verificar_tipo_componente('FLOTANTE')

    def __verificar_booleano(self) -> None:
        """
        Booleano::= SIUA|NOUA
        """

        self.__verificar_tipo_componente('BOOLEANO')

    def __verificar_texto(self) -> None:
        """
        Texto ::= ツ.*ツ
        """

        self.__verificar_tipo_componente('TEXTO')

    def __verificar_tipo_componente(self, tipo_componente_esperado) -> None:

        # Error sintactico si no son de tipo equivalentes
        if self.componente_actual.tipo != tipo_componente_esperado:
            self.__error_verificacion_tipo(tipo_componente_esperado)

        self.__siguiente_componente()

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

    def __analizar_expresion_matematica(self) -> None:
        """
        ExpresionMatematica::= Valor (Operador Valor)*
        """

        # Se verifica el primer valor
        self.__analizar_valor()

        # Como pueden o no estar se validan mientras siga un operador
        while(self.componente_actual.tipo == 'OPERADOR'):
            self.__verificar_operador()
            self.__analizar_valor()

    def __verificar_operador(self) -> None:
        """
        Operador::= bobMar | bobStar | bobiDir | bobTiplicar
        """

        self.__verificar_tipo_componente('OPERADOR')

    def __verificar_operador_logico(self) -> None:
        """
        OperadorLogico::= aja | ayno
        """

        self.__verificar_tipo_componente('OPERADOR_LOGICO')

    def __verificar_comparador(self) -> None:
        """
        Comparador ::= chikito | tapotente | panapotente |
                        panachikito | nolocrick | panas
        """

        self.__verificar_tipo_componente('COMPARADOR')

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
              f' (Linea {linea}, Columna {columna})')

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
