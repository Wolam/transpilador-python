from Utils.arbol import Nodo, TipoNodo

class VisitantePython:

    tabuladores = 0

    def __init__(self):
        """
        Constructor para inicializar la clase visitante
        """

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

        return self.dic_tipos_nodo[nodo.tipo](nodo)
    
    def __visitar_programa(self, nodo_actual: Nodo) -> str:
        """
        Programa ::= Comentario Asignación* (Comentario | Funcion)* Principal
        """

        instrucciones = []
        # Se ignoran los comentarios

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))
        
        return '\n'.join(instrucciones) 
    
    def __visitar_asignacion(self, nodo_actual: Nodo) -> str:
        """
        Asignación ::= Identificador anotado (Valor | Invocación | ExpresionMatematica).
        """

        resultado = """{} = {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0],instrucciones[1])
    
    def __visitar_expresion_matematica(self, nodo_actual: Nodo) -> str:
        """
        ExpresionMatematica::= #Valor (Operador Valor)*#
        """

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return ' '.join(instrucciones)
    
    def __visitar_funcion(self, nodo_actual: Nodo) -> str:
        """
        Función ::= POV Identificador(Parámetros?) xD ConjuntoInstrucciones v:
        """

        resultado = """\ndef {}({}):\n{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        if len(instrucciones) == 2:
            return resultado.format(instrucciones[0],"",'\n'.join(instrucciones[1]))

        return resultado.format(instrucciones[0],instrucciones[1], '\n'.join(instrucciones[2]))


    def __visitar_invocacion(self, nodo_actual: Nodo) -> str:
        """
        Invocación ::= jutsu Identificador(Parámetros?)
        """

        resultado = """{}({})"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        if len(instrucciones) == 1:
            return resultado.format(instrucciones[0],"")

        return resultado.format(instrucciones[0], instrucciones[1])
    
    def __visitar_parametros_invocacion(self, nodo_actual: Nodo) -> str:
        """
        ParámetrosInvocacion::= Valor (, Valor)*
        """
        parametros = []

        for nodo in nodo_actual.nodos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0:
            return ','.join(parametros)

        else:
            return ''

    def __visitar_parametros_funcion(self, nodo_actual: Nodo) -> str:
        """
        ParámetrosFuncion::= Identificador (, Identificador)*
        """

        parametros = []

        for nodo in nodo_actual.nodos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0:
            return ','.join(parametros)

        else:
            return ''     
    def __visitar_instruccion(self, nodo_actual: Nodo) -> str :
        """
        Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )
        """

        valor = ""

        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return valor

    def __visitar_repetir(self, nodo_actual: Nodo) -> str:
        """
        Repetir ::= whenCuando xD ConjuntoInstrucciones but (ExpCondicional) v:
        """

        resultado = """while {}:\n{}"""

        instrucciones = []

        # Visita la condición
        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[1],'\n'.join(instrucciones[0]))

    def __visitar_condicional(self, nodo_actual: Nodo) -> str:
        """
        Condicional::= Siuuu Nimodo?
        """

        resultado = """{}{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], '')
 
    def __visitar_siuuu(self, nodo_actual: Nodo) -> str:
        """
        Siuuu::= siuuu (ExpCondicional) xD ConjuntoInstrucciones v:
        """

        resultado = """if {}:\n{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0],'\n'.join(instrucciones[1]))

    def __visitar_nimodo(self, nodo_actual: Nodo) -> str:
        """
        Nimodo::=  nimodo xD ConjuntoInstrucciones v:
        """

        resultado = """else:\n  {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return resultado.format('\n'.join(instrucciones[0]))
    
    def __visitar_expresion_condicional(self, nodo_actual: Nodo) -> str:
        """
        ExpCondicional ::= Comparación(OperadorLogico Comparación)?
        """

        resultado = """{} {} {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        if len(instrucciones) == 1:
            return resultado.format(instrucciones[0],'', '')
        else:
            return resultado.format(instrucciones[0],instrucciones[1],instrucciones[2])

    def __visitar_comparacion(self, nodo_actual: Nodo) -> str:
        """
        Comparación::= Valor Comparador Valor
        """
        resultado = '{} {} {}'

        elementos = []

        #Si valor es IDENTIFICADOR se verifica que exista
        for nodo in nodo_actual.nodos:
            elementos.append(nodo.visitar(self))
        
        return resultado.format(elementos[0], elementos[1], elementos[2])
    
    def __visitar_retorno(self, nodo_actual: Nodo) -> str:
        """
        Retorno: := messirve Valor?
        """
        resultado = 'return {}'
        valor = ''

        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return resultado.format(valor)

    def __visitar_principal(self, nodo_actual: Nodo) -> None:
        """
        Principal::= maracuya() xD ConjuntoInstrucciones v:
        """
        #Solo visita un bloque de instrucciones

        resultado = """\ndef principal():\n{}\n

if __name__ == '__main__':
    principal()
"""
        instrucciones = []
        
        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]
        
        return resultado.format("\n".join(instrucciones[0]))

    def __visitar_conjunto_instrucciones(self, nodo_actual: Nodo):
        """
        ConjuntoInstrucciones ::= Instruccion+
        """
        self.tabuladores += 2

        instrucciones = []

        #Se visitan todas las instrucciones
        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        instrucciones_tabuladas = []

        for instruccion in instrucciones:
            instrucciones_tabuladas += [self.__retornar_tabuladores() + instruccion]
        
        self.tabuladores -= 2

        return instrucciones_tabuladas
       

    def __visitar_operador(self, nodo_actual: Nodo) -> str:
        """
        Operador::= bobMar | bobStar | bobiDir | bobTiplicar
        """

        if nodo_actual.contenido == 'bobMar':
            return '+'

        elif nodo_actual.contenido == 'bobStar':
            return '-'
        
        elif nodo_actual.contenido == 'bobTiplicar':
            return '*'
        
        else:
            return '/'

    def __visitar_booleano(self, nodo_actual: Nodo) -> str:
        """
        Booleano::= SIUA|NOUA
        """

        if nodo_actual.contenido == 'SIUA':
            return 'True'
        
        else:
            return 'False'

    def __visitar_operador_logico(self, nodo_actual: Nodo) -> str:
        """
        Operador logico ::= (aja | ayno)
        """

        if nodo_actual.contenido == 'aja':
            return 'and'
        
        else:
            return 'or'
    
    def __visitar_comparador(self, nodo_actual: Nodo) -> str:
        """
        Comparador ::= chikito | tapotente | panapotente | panachikito | nolocrick | panas
        """

        if nodo_actual.contenido == 'tapotente':
            return '>'

        elif nodo_actual.contenido == 'chikito':
            return '<'

        elif nodo_actual.contenido == 'panas':
            return '=='

        elif nodo_actual.contenido == 'nolocrick':
            return '!='

        elif nodo_actual.contenido == 'panachikito':
            return '<='

        elif nodo_actual.contenido == 'panapotente':
            return '>='
        else:
            return 'yo'

    def __visitar_texto(self, nodo_actual: Nodo) -> str:
        """
        Texto ::= ツ.*ツ
        """
        return nodo_actual.contenido.replace('ツ', '"')

    def __visitar_entero(self, nodo_actual: Nodo) -> str:
        """
        Entero::= -?[0-9]+
        """
        return nodo_actual.contenido

    def __visitar_flotante(self, nodo_actual: Nodo) -> str:
        """
        Flotante::= -?[0-9]+;[0-9]+
        """
        return nodo_actual.contenido.replace(';', '.')
        

    def __visitar_identificador(self, nodo_actual: Nodo) -> str:
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        return nodo_actual.contenido

    def __retornar_tabuladores(self):
        return " " * self.tabuladores
