from os import system
import random
import time

def mostrar_pista(carril_1, carril_2, carril_3):
  print(carril_1)
  print(carril_2)
  print(carril_3)

def modificar_carril(carril, posicion_caracol):
  time.sleep(0.2)
  caracol = carril[posicion_caracol] + carril[posicion_caracol+1]
  recorrido = carril[:posicion_caracol] + "_"
  por_recorrer = carril[posicion_caracol+3:] 
  return recorrido + caracol + por_recorrer

def obtener_movimiento():
  movimiento = random.randint(0, 2)
  return movimiento

def verifica_ganador(carril):
  return carril[len(carril) - 4] == "Ÿ"
    
def principal():
  carril_1 = "@Ÿ_______________________________________________________________________________________________________________________l^l"
  carril_2 = "@Ÿ_______________________________________________________________________________________________________________________l^l"
  carril_3 = "@Ÿ_______________________________________________________________________________________________________________________l^l"

  posicion_caracol_1, posicion_caracol_2, posicion_caracol_3 = 0,0,0

  estado_1, estado_2, estado_3 = False, False, False
  while (estado_1 == False and estado_2 == False and estado_3 == False):
    system('clear')
    mostrar_pista(carril_1, carril_2, carril_3)
    movimiento = obtener_movimiento()
    if movimiento == 0:
      carril_1 = modificar_carril(carril_1, posicion_caracol_1)
      posicion_caracol_1+=1
    elif movimiento == 1: 
      carril_2 = modificar_carril(carril_2, posicion_caracol_2)
      posicion_caracol_2+=1
    else: 
      carril_3 = modificar_carril(carril_3, posicion_caracol_3)
      posicion_caracol_3+=1

    estado_1 = verifica_ganador(carril_1)
    estado_2 = verifica_ganador(carril_2)
    estado_3 = verifica_ganador(carril_3)

  system('clear')
  mostrar_pista(carril_1, carril_2, carril_3)
  return "\nfelicidades tenemos un ganador!!!!!!"

print(principal())