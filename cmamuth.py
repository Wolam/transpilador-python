# Archivo principal que tiene el compilador de C-Mamuth

import os
import sys
from argparse import ArgumentParser

from Analizador.analizador import Analizador
from Explorador.explorador import Explorador
from Generador.generador import Generador
from Utils import archivos as utils
from Verificador.verificador import Verificador

parser = ArgumentParser(
    description='Intérprete para el lenguaje C-Mamuth')

parser.add_argument('--explorar', '-e', dest='explorar', action='store_true',
                    help='''Ejecutar el interprete hasta el explorador unicamente
                mostrando componentes''')

parser.add_argument('--analizar', '-a', dest='analizar', action='store_true',
                    help='''Ejecutar el interprete hasta el analizador
                unicamente mostrando arbol''')

parser.add_argument('--verificar', '-v', dest='verificar', action='store_true',
                    help='''Ejecutar el interprete hasta el verificador
                mostrando arbol y tabla de simbolos''')

parser.add_argument('--generar', '-g', dest='generar', action='store_true',
                    help='''Ejecutar el interprete para generar código de cmamuth en python''')

parser.add_argument('archivo',
                    help='Archivo de código fuente .cm')

args = parser.parse_args()


def cmamuth() -> None:

    try:
        texto = utils.cargar_archivo(args.archivo)
        explorador = Explorador(texto)
        explorador.explorar()
        
        if args.explorar:
            explorador.imprimir_componentes()
            sys.exit(os.EX_OK)
    
        analizador = Analizador(explorador.componentes)
        analizador.analizar()

        if args.analizar:
            analizador.imprimir_ast()
            sys.exit(os.EX_OK)

        verificador = Verificador(analizador.ast)
        tabla_simbolos = verificador.verificar()

        if args.verificar: 
            print(tabla_simbolos)
            verificador.imprimir_ast()
            sys.exit(os.EX_OK)
        
        if args.generar:
            generador = Generador(verificador.ast)
            generador.generar()
            sys.exit(os.EX_OK)


    except SyntaxError as se:
        sys.exit(se)
    
    except TypeError as te:
        sys.exit(te)

    except NameError as ne:
        sys.exit(ne)
    
    except FileNotFoundError:
        sys.exit(f'Archivo .cm invalido {args.archivo!r}')


if __name__ == '__main__':
    cmamuth()
