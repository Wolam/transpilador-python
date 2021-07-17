from typing import List, NoReturn

from Utils.arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from Utils.registro import Registro
from Utils.tipo_datos import TipoDato


class TablaSimbolos:
    """ 
    Almacena información auxiliar para decorar el árbol de sintáxis
    abstracta con información de tipo y alcance.

    La estructura de simbolos es una lista de registros
    """

    simbolos: List[Registro]
    profundidad: int

    def __init__(self) -> None:
        """
        Constructor para inicializar la clase TablaSimbolos
        """

        self.simbolos = []
        self.profundidad = 0

    def nuevo_bloque(self):
        """
        Inicia un bloque de alcance
        """

        self.profundidad += 1

    def eliminar_bloque(self) -> None:
        """
        Termina un bloque de alcance y  elimina todos los
        registros de la tabla que corresponden a ese bloque
        """

        for registro in self.simbolos:
            if registro.get_profundidad() == self.profundidad:
                self.simbolos.remove(registro)

        self.profundidad -= 1

    def nuevo_registro(self, nodo: Nodo) -> None:
        """
        Introduce un nuevo registro a la tabla de simbolos
        """

        registro = Registro(self.profundidad, nodo)

        self.simbolos.append(registro)

    def verificar_existencia(self, nombre: str, atributos: dict) -> Registro:
        """
        Verifica si un identificador existe como variable/función local
        """
        for registro in self.simbolos:

            # si es local
            if registro.get_nombre() == nombre and \
                    registro.get_profundidad() <= self.profundidad:

                return registro

        self.__error_identificador_inexistente(nombre, atributos)

    def __error_identificador_inexistente(self,nombre : str, atributos: dict) -> NoReturn:
        """
        Encargado de tirar error si el identificador no existe con anterioridad
        """

        print(f'El siguiente identificador no está declarado: {nombre!r} ' +
              f'(Linea: {atributos.get("linea")}, Columna: {atributos.get("columna")})')

        raise NameError('Error de existencia de identificador en el verificador')


    def __str__(self) -> None:
        """
        Impresión de tabla símbolos
        """

        #f'{self.tipo:30} --> {self.valor:10} \
        #(Linea: {self.linea} , Columna: {self.columna})'

        resultado = f'TABLA DE SIMBOLOS\n\n'
        for registro in self.simbolos:
            tabulacion = "   "*registro.get_profundidad()
            resultado += f'{tabulacion}|__{str(registro)}\n'
            

        return resultado


class Visitante:
    """
    Clase que contiene los método para visitar cada uno de
    los sectores de la gramática en el árbol y rellenar
    con el tipo de dato
    """

    tabla_simbolos: TablaSimbolos
    dic_tipos_nodo: dict

    def __init__(self, tabla_simbolos):
        """
        Constructor para inicializar la clase visitante
        """

        self.tabla_simbolos = tabla_simbolos

        #diccionario para asignar el tipo de nodo con su respectiva función
        self.dic_tipos_nodo = {
            TipoNodo.PROGRAMA: self.__visitar_programa, TipoNodo.ASIGNACION: self.__visitar_asignacion,
            TipoNodo.EXPRESION_MATEMATICA: self.__visitar_expresion_matematica, TipoNodo.FUNCION: self.__visitar_funcion,
            TipoNodo.INVOCACION: self.__visitar_invocacion, TipoNodo.COMPARACION: self.__visitar_comparacion,
            TipoNodo.PARAMETROS_INVOCACION: self.__visitar_parametros_invocacion, TipoNodo.PARAMETROS_FUNCION: self.__visitar_parametros_funcion,
            TipoNodo.INSTRUCCION: self.__visitar_instruccion, TipoNodo.REPETIR: self.__visitar_repetir, TipoNodo.CONDICIONAL: self.__visitar_condicional,
            TipoNodo.SIUUU: self.__visitar_siuuu, TipoNodo.NIMODO: self.__visitar_nimodo, TipoNodo.OPERADOR_LOGICO: self.__visitar_operador_logico,
            TipoNodo.COMPARADOR: self.__visitar_comparador, TipoNodo.RETORNO: self.__visitar_retorno, TipoNodo.PRINCIPAL: self.__visitar_principal,
            TipoNodo.CONJUNTO_INSTRUCCIONES: self.__visitar_conjunto_instrucciones, TipoNodo.OPERADOR: self.__visitar_operador,
            TipoNodo.TEXTO: self.__visitar_texto, TipoNodo.ENTERO: self.__visitar_entero, TipoNodo.FLOTANTE: self.__visitar_flotante,
            TipoNodo.IDENTIFICADOR: self.__visitar_identificador, TipoNodo.EXPRESION_CONDICIONAL: self.__visitar_expresion_condicional,
            TipoNodo.BOOLEANO: self.__visitar_booleano
        }

    def visitar(self, nodo: Nodo) -> None:
        """
        Se utiliza el diccionario para visitar al sector del árbol correspondiente,
        dependiendo del nodo que le entre, a esa función se llama

        self.dic_tipos_nodo[TipoNodo.PROGRAMA] = self.__visitar_programa
        """

        self.dic_tipos_nodo[nodo.tipo](nodo)

    def __visitar_programa(self, nodo_actual: Nodo) -> None:
        """
        Programa ::= Comentario Asignación* (Comentario | Funcion)* Principal
        """

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

    def __visitar_asignacion(self, nodo_actual: Nodo) -> None:
        """
        Asignación ::= Identificador anotado (Valor | Invocación | ExpresionMatematica)
        """

        if nodo_actual.nodos[1].tipo == TipoNodo.IDENTIFICADOR:
            registro = self.tabla_simbolos.verificar_existencia(
                    nodo_actual.nodos[1].contenido, nodo_actual.nodos[1].atributos)

        self.tabla_simbolos.nuevo_registro(nodo_actual.nodos[0])

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

        nodo_actual.nodos[0].atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

    def __visitar_expresion_matematica(self, nodo_actual: Nodo) -> None:
        """
        ExpresionMatematica::= #Valor (Operador Valor)*#
        """

        for nodo in nodo_actual.nodos:

            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(
                    nodo.contenido, nodo.atributos)
                if registro.get_referencia().atributos.get("tipo") != TipoDato.NUMERO and registro.get_referencia().atributos.get('tipo') != TipoDato.CUALQUIERA:
                    self.__error_expresion_matematica_identificador(registro)
            else:
                if nodo.tipo != TipoNodo.ENTERO and nodo.tipo != TipoNodo.OPERADOR:
                   self.__error_expresion_matematica_literal(nodo)


            self.visitar(nodo)
        
        nodo_actual.atributos['tipo'] = TipoDato.NUMERO

    def __visitar_funcion(self, nodo_actual: Nodo) -> None:
        """
        Función ::= POV Identificador(Parámetros?) xD ConjuntoInstrucciones v:
        """

        self.tabla_simbolos.nuevo_registro(nodo_actual)

        self.tabla_simbolos.nuevo_bloque()

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        self.tabla_simbolos.eliminar_bloque()

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[2].atributos['tipo']

    def __visitar_invocacion(self, nodo_actual: Nodo) -> None:
        """
        Invocación ::= jutsu Identificador(Parámetros?)
        """
        registro = self.tabla_simbolos.verificar_existencia(
            nodo_actual.nodos[0].contenido, nodo_actual.nodos[0].atributos)
            
        if registro.get_referencia().tipo != TipoNodo.FUNCION:
            self.__error_invocacion(registro)

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = registro.get_referencia(
        ).atributos['tipo']

    def __visitar_parametros_invocacion(self, nodo_actual: Nodo) -> None:
        """
        Parámetros::= Valor (, Valor)*
        """

        for nodo in nodo_actual.nodos:

            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(
                    nodo.contenido, nodo.atributos)

            elif nodo.tipo == TipoNodo.FUNCION:
                self.__error_parametros(nodo.contenido)

            self.visitar(nodo)

    def __visitar_parametros_funcion(self, nodo_actual: Nodo) -> None:
        """
        Parámetros::= Identificador (, Identificador)*
        """

        for nodo in nodo_actual.nodos:
            self.tabla_simbolos.nuevo_registro(nodo)
            self.visitar(nodo)

    def __visitar_instruccion(self, nodo_actual: Nodo) -> None:
        """
        Instruccion ::= Asignación | Repetir | Condicional | Comentario | Retorno
        """

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)
            nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitar_repetir(self, nodo_actual: Nodo) -> None:
        """
        Repetir ::= whenCuando   xD ConjuntoInstrucciones but (ExpCondicional) v:
        """

        self.tabla_simbolos.nuevo_bloque()

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        self.tabla_simbolos.eliminar_bloque()

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']

    def __visitar_condicional(self, nodo_actual: Nodo) -> None:
        """
        Condicional::= Siuuu Nimodo?
        """

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = TipoDato.CUALQUIERA

    def __visitar_siuuu(self, nodo_actual: Nodo) -> None:
        """
        Siuuu::= siuuu (ExpCondicional) xD Conjunto Instrucciones v:
        """

        self.tabla_simbolos.nuevo_bloque()

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        self.tabla_simbolos.eliminar_bloque()

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

    def __visitar_nimodo(self, nodo_actual: Nodo) -> None:
        """
        Nimodo::=  nimodo xD ConjuntoInstrucciones v:
        """

        self.tabla_simbolos.nuevo_bloque()

        self.visitar(nodo_actual.nodos[0])

        self.tabla_simbolos.eliminar_bloque()

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']

    def __visitar_expresion_condicional(self, nodo_actual: Nodo) -> None:
        """
        ExpCondicional ::= Comparación(OperadorLogico Comparación)? 
        """
        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = TipoDato.BOOLEANO

    def __visitar_comparacion(self, nodo_actual: Nodo) -> None:
        """
        Comparación::= Valor Comparador Valor
        """

        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(
                    nodo.contenido, nodo.atributos)

            self.visitar(nodo)

        valor_izquierda = nodo_actual.nodos[0]
        comparador = nodo_actual.nodos[1]
        valor_derecha = nodo_actual.nodos[2]

        if valor_izquierda.atributos['tipo'] == valor_derecha.atributos['tipo']:
            comparador.atributos['tipo'] = valor_izquierda.atributos['tipo']

            nodo_actual.atributos['tipo'] = TipoDato.BOOLEANO

        elif valor_izquierda.atributos['tipo'] == TipoDato.CUALQUIERA or \
                valor_derecha.atributos['tipo'] == TipoDato.CUALQUIERA:

            comparador.atributos['tipo'] = TipoDato.CUALQUIERA

            nodo_actual.atributos['tipo'] = TipoDato.CUALQUIERA

        else:
            self.__error_comparacion(valor_izquierda, valor_derecha)

    def __visitar_retorno(self, nodo_actual: Nodo) -> None:
        """
        Retorno: := messirve Valor?
        """

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        if nodo_actual.nodos == []:
            nodo_actual.atributos['tipo'] = TipoDato.NINGUNO

        else:

            for nodo in nodo_actual.nodos:

                self.visitar(nodo)

                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    # Se verifica que el identificador exista
                    registro = self.tabla_simbolos.verificar_existencia(
                        nodo.contenido, nodo.atributos)

                    # se guarda el tipo de dato del retorno
                    nodo_actual.atributos['tipo'] = registro.get_referencia(
                    ).atributos['tipo']

                else:
                    # Se verifica el tipo del literal
                    nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitar_principal(self, nodo_actual: Nodo) -> None:
        """
        Principal::= maracuya() xD ConjuntoInstrucciones v:
        """
        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']

    def __visitar_conjunto_instrucciones(self, nodo_actual: Nodo) -> None:
        """
        ConjuntoInstrucciones ::= Instruccion+
        """

        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

        nodo_actual.atributos['tipo'] = TipoDato.NINGUNO

        for nodo in nodo_actual.nodos:
            if nodo.atributos['tipo'] != TipoDato.NINGUNO:
                nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitar_operador(self, nodo_actual: Nodo) -> None:
        """
        Operador::= bobMar | bobStar | bobiDir | bobTiplicar
        """

        nodo_actual.atributos['tipo'] = TipoDato.NUMERO

    def __visitar_booleano(self, nodo_actual: Nodo) -> None:
        """
        Booleano::= SIUA|NOUA
        """

        nodo_actual.atributos['tipo'] = TipoDato.BOOLEANO

    def __visitar_operador_logico(self, nodo_actual: Nodo) -> None:
        """
        Operador logico ::= (aja | ayno)
        """

        nodo_actual.atributos['tipo'] = TipoDato.COMPARADOR_LOGICO

    def __visitar_comparador(self, nodo_actual: Nodo) -> None:
        """
        Comparador ::= chikito | tapotente | panapotente | panachikito | nolocrick | panas
        """

        if nodo_actual.contenido not in {'panas', 'nolocrick'}:
            nodo_actual.atributos['tipo'] = TipoDato.NUMERO

        else:
            nodo_actual.atributos['tipo'] = TipoDato.CUALQUIERA

    def __visitar_texto(self, nodo_actual: Nodo) -> None:
        """
        Texto ::= ツ.*ツ
        """

        nodo_actual.atributos['tipo'] = TipoDato.TEXTO

    def __visitar_entero(self, nodo_actual: Nodo) -> None:
        """
        Entero ::= -?[0-9]+
        """
        
        nodo_actual.atributos['tipo'] = TipoDato.NUMERO

    def __visitar_flotante(self, nodo_actual: Nodo) -> None:
        """
        Flotante ::= -?[0-9]+;[0-9]+
        """

        nodo_actual.atributos['tipo'] = TipoDato.FLOTANTE

    def __visitar_identificador(self, nodo_actual: Nodo) -> None:
        """
        Identificador ::= [A-Za-z_][A-Za-z_0-9]+
        """
        nodo_actual.atributos['tipo'] = TipoDato.CUALQUIERA

    def __error_invocacion(self, registro: Registro) -> NoReturn:
        """
        Levanta un error de tipo si se usa una variable como funcion
        """

        variable = registro.get_referencia().contenido
        print(f'Se utiliza variable {variable!r} para invocacion de funcion')

        raise TypeError("Error de tipos en verificador")
    
    def __error_expresion_matematica_identificador(self, registro: Registro) -> NoReturn:
        """
        Levanta un error de tipo si no se utiliza un entero en una expresión matemática
        """

        variable = registro.get_referencia().contenido
        print(f'El identificador {variable!r} no es de tipo entero')

        raise TypeError("Error de tipos en verificador")
    
    def __error_expresion_matematica_literal(self, nodo: Nodo) -> NoReturn:
        """
        Levanta un error de tipo si no se utiliza un entero en una expresión matemática
        """

        variable = nodo.contenido
        print(f'{variable!r} no es de tipo entero')

        raise TypeError("Error de tipos en verificador")

    def __error_parametros(self, nodo: Nodo) -> NoReturn:
        """
        Levanta un error de tipo si se usa una funcion como parametro
        """

        funcion = nodo.contenido
        print(f'Se utiliza funcion {funcion!r} en los parametros')

        raise TypeError("Error de tipos en verificador")

    def __error_comparacion(self, comparador: Nodo,
                            variable_izquierda: Nodo,
                            variable_derecha: Nodo) -> NoReturn:
        """
        Levanta un error de tipo si se realiza una comparacion
        entre tipos diferentes de variables
        """

        tipo_izquierda = variable_izquierda.atributos['tipo']
        tipo_derecha = variable_derecha.atributos['tipo']

        print(f'La comparacion con {comparador.contenido!r} ' +
              f'no se puede dar entre tipos {tipo_izquierda!r} ' +
              f'y {tipo_derecha!r}')

        raise TypeError("Error de tipos en verificador")


class Verificador:
    """
    Clase encargada de invocar a la clase visitante
    para aplicar el patron visitante para cada uno
    de los nodos en el arbol de sintaxis abstracta
    """

    ast: ArbolSintaxisAbstracta
    visitador: Visitante
    tabla_simbolos: TablaSimbolos

    def __init__(self, nuevo_ast: ArbolSintaxisAbstracta):
        """
        Constructor de clase verificador
        """
        self.ast = nuevo_ast
        self.tabla_simbolos = TablaSimbolos()
        self.visitador = Visitante(self.tabla_simbolos)
        self.__cargar_ambiente_estandar()

    def imprimir_ast(self):
        """
        Imprime el árbol de sintáxis abstracta
        """

        if self.ast.raiz is None:
            print([])
        else:
            self.ast.imprimir_preorden()

    def verificar(self) -> str:
        """
        Se encarga de llamar a visitar
        imprime el estado final de la tabla de símbolos
        """
        self.visitador.visitar(self.ast.raiz)
        return self.tabla_simbolos
    
    def __cargar_ambiente_estandar(self) -> None:
        """
        Determina funciones estándar del lenguaje cmamuth
        """

        funciones_estandar = [ ('curcuma', TipoDato.TEXTO), 
            ('nel', TipoDato.NUMERO), ('intnt', TipoDato.BOOLEANO), 
            ('me_perdonas', TipoDato.NINGUNO), ('aber', TipoDato.NINGUNO),
            ('duren', TipoDato.TEXTO), ('corona', TipoDato.TEXTO),
            ('amimir', TipoDato.NINGUNO) , ('f_en_el_chat',TipoDato.NINGUNO),
            ('lolazo',TipoDato.ENTERO)]

        for nombre, tipo in  funciones_estandar:
            nodo = Nodo(TipoNodo.FUNCION, contenido=nombre, atributos= {'tipo': tipo})
            self.tabla_simbolos.nuevo_registro(nodo)
