from colores import font_colors as c

import csv, random
from os import scandir


class Main(object):
    def __init__(self):
        #Menu principal del juego, validar usuarios
        print('-------------------------------')
        print(f'{c.AMARILLO}Ingreso de usuarios{c.RESET}')
        usuario = input(f'{c.CELESTE}Ingrese su usuario: {c.RESET}')
        clave = input(f'{c.CELESTE}Ingrese su clave: {c.RESET}')
        print(f'{c.AMARILLO}Buscando en la lista de jugadores: {c.RESET}')
        jugador = []
        validar = False
        arch = open('tableros/usuarios.csv', 'r+', newline='')
        next(arch, None)
        with arch:
            lector = csv.reader(arch)
            for linea in lector:
                if usuario == linea[0] and clave == linea[1]:
                    validar = True
                    jugador.append(linea)
                    print(f'{c.VERDE}Usuario valido. Iniciando sesion{c.RESET}')
        if validar:
            Juego.menu(Juego, jugador)
        else:
            print(f'{c.ROJO}El usuario o la clave es incorrecta{c.RESET}')

class Juego():
    def menu(self, jugador):
        print('-------------------------------')
        print(f'{c.PURPURA}Bienvenido {c.CELESTE}{jugador[0][0]}{c.PURPURA}!{c.RESET}')
        print(f'{c.PURPURA}Tiene disponible {c.CELESTE}{jugador[0][2]}{c.PURPURA} puntos{c.RESET}')
        validar = input(f'Desea iniciar un juego? Escriba {c.PURPURA}SI{c.RESET} para empezar: ')
        if validar.lower() == 'si':
            print(f'{c.VERDE}Iniciando juego{c.RESET}')
            print('')
            self.obtener_tabla(self, jugador)
        else:
            print(f'{c.ROJO}Volviendo al menu{c.RESET}')

    def obtener_tabla(self, jugador):
        datos = [arch.name for arch in scandir('tableros/tablas') if arch.is_file()]
        tabla_elegida = random.choice(datos)
        self.mostrar_tablero(Juego, tabla_elegida, jugador)
    
    def mostrar_tablero(self, tabla_elegida, jugador):
        self.tabla_elegida = tabla_elegida
        tabla = []
        arch = open('tableros/tablas/' + self.tabla_elegida, 'r+', newline='')
        with arch:
            tabla = csv.reader(arch)
            for fila in tabla:
                print(*fila, sep=' | ')
        self.jugar(Juego, tabla_elegida, jugador)

    def jugar(self, tabla_elegida, jugador):
        nombre_tabla = tabla_elegida.replace('.csv','')
        tabla = []
        temporal = []
        info_tabla = []
        validar = False
        arch = open('tableros/tablas/' + tabla_elegida, 'r+', newline='')
        with arch:
            lector = csv.reader(arch)
            for linea in lector:
                tabla.append(linea)
        arch = open('tableros/soluciones/' + nombre_tabla + '_solucion.csv', 'r+', newline='')
        next(arch, None)
        with arch:
            lector = csv.reader(arch)
            for linea in lector:
                for espacio in linea:
                    temporal.append(espacio)
                temporal.append(False)
                info_tabla.append(temporal)
                temporal = []
        while True:
            print('-------------------------------')
            print(f'{c.AMARILLO}Menu de juego:{c.RESET}')
            print(f'{c.PURPURA}Escriba {c.ROJO}HELP{c.PURPURA} si desea activar la ayuda{c.RESET}')
            print(f'{c.PURPURA}Perdera {c.ROJO}3{c.PURPURA} monedas al activarlo')
            palabra = input(f'{c.CELESTE}Escriba la palabra que encontro: {c.RESET}')
            if palabra.lower() == 'help':
                if int(jugador[0][2]) >= 3:
                    palabras_libres = []
                    for data_tabla in info_tabla:
                        if data_tabla[5] == False:
                            palabras_libres.append(data_tabla[0])
                    palabra_marcada = random.choice(palabras_libres)
                    for data_tabla in info_tabla:
                        if data_tabla[0] == palabra_marcada:
                            temp = f'{c.ROJO}{data_tabla[0][0].upper()}{c.RESET}'
                            tabla[int(data_tabla[1])][int(data_tabla[2])] = temp
                            jugador[0][2] = int(jugador[0][2]) - 3
                            print(f'{c.VERDE}Pista comprada, suerte!{c.RESET}')
                            print(f'{c.CELESTE}Ahora tiene {c.PURPURA}{jugador[0][2]}{c.CELESTE} monedas{c.RESET}')
                else:
                    print(f'{c.ROJO}No cuenta con las monedas suficientes{c.RESET}')
            contador = 0
            for data_tabla in info_tabla:
                if data_tabla[0] == palabra:
                    print(f'{c.VERDE}La palabra existe! +1 punto{c.RESET}')
                    validar = True
                    jugador[0][2] = int(jugador[0][2]) + 1
                    data_tabla[5] = True
                    pos_y = int(data_tabla[2])
                    pos_x = int(data_tabla[1])
                    for letra in data_tabla[0]:
                        res = f'{c.CELESTE}{letra.upper()}{c.RESET}'
                        tabla[pos_x][pos_y] = res
                        adivinar_x = int(data_tabla[1]) - int(data_tabla[3])
                        if adivinar_x == 0:
                            pos_y = pos_y + 1
                        else:
                            pos_x = pos_x + 1
                    break
            for linea in tabla:
                print(*linea, sep=' | ')
            for data_tabla in info_tabla:
                if data_tabla[5] == True:
                    contador += 1
            aux_usuarios = []
            arch = open('tableros/usuarios.csv', 'r+', newline='')
            next(arch, None)
            with arch:
                lector = csv.reader(arch)
                for linea in lector:
                    aux_usuarios.append(linea)
            if validar:
                arch = open('tableros/usuarios.csv', 'w+', newline='')
                with arch:
                    lector = csv.DictWriter(arch, fieldnames=['usuario', 'clave', 'monedas'])
                    lector.writeheader()
                    for linea in aux_usuarios:
                        if linea[0] == jugador[0][0]:
                            linea[2] = int(jugador[0][2])
                            print(f'{c.PURPURA}Actualmente posee {c.CELESTE}{linea[2]}{c.PURPURA} monedas!{c.RESET}')
                            validar = False
                    for linea in aux_usuarios:
                        lector.writerow({'usuario': linea[0],
                        'clave': linea[1], 'monedas': linea[2]})
            if contador == len(info_tabla):
                print(f'{c.ROJO}Tabla finalizada! Felicitaciones!!{c.RESET}')
                break
                        