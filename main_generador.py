# Importar carpetas
from colores import font_colors as c
# Importar librerias propias de Python
import random,string,csv
from os import scandir, remove

class Main():
    def __init__(self):
        # Menu principal del sistema de gestion
        print('-------------------------------')
        print(f'{c.AMARILLO}Menu principal de gestion de sopas de letras y usuarios:{c.RESET}')
        while True:
            print('Menu de opciones:')
            print(f'{c.PURPURA}1.{c.RESET} Crear nuevo tablero')
            print(f'{c.PURPURA}2.{c.RESET} Crear nuevo jugador')
            print(f'{c.PURPURA}3.{c.RESET} Ver lista de tableros')
            print(f'{c.PURPURA}4.{c.RESET} Ver lista de jugadores')
            print(f'{c.PURPURA}5.{c.RESET} Eliminar un tablero')
            print(f'{c.PURPURA}6.{c.RESET} Eliminar un jugador')
            print(f'{c.PURPURA}0.{c.RESET} Salir')
            try:
                opcion = int(input('Ingrese opcion: '))
                if opcion == 1:
                    Generar.crear_tablero()
                elif opcion == 2:
                    Generar.crear_jugador()
                elif opcion == 3:
                    Obtener_Datos.obtener_datos_tableros(Obtener_Datos, 'tableros/tablas')
                elif opcion == 4:
                    Obtener_Datos.mostrar_jugadores(Obtener_Datos)
                elif opcion == 5:
                    Generar.borrar_tablero('tableros/tablas')
                elif opcion == 6:
                    Generar.borrar_jugador()
                elif opcion == 0:
                    print(f'{c.VERDE}Volviendo al menu{c.RESET}')
                    break
                else:
                    print(f'{c.ROJO}Elija la opcion correcta{c.RESET}')
            except ValueError:
                print(f'{c.ROJO}Ingrese un valor de tipo numerico entero{c.RESET}')
            print('-------------------------------')

class Generar():
    def crear_tablero():
        print(f'{c.AMARILLO}Creacion de tablero: {c.RESET}')
        while True:
            try:
                len_tabla = int(input(f'{c.CELESTE}Ingrese el tamaño de la sopa: {c.RESET}'))
                if len_tabla>=15:
                    break
                print(f'{c.ROJO}El tamaño tiene que ser menor o igual a 15{c.RESET}')
            except ValueError:
                print(f'{c.ROJO}Ingrese un valor numerico{c.RESET}')
        lista_palabras = []
        cantidad_letras = int(len_tabla/3)
        for pos in range(cantidad_letras):
            while True:
                try:
                    palabra_aux = input(f'{c.CELESTE}Ingrese la palabra a cargar, tiene que tener menos de {c.VERDE}{cantidad_letras}{c.CELESTE} palabras {c.VERDE}[{pos+1}/{cantidad_letras}]:{c.RESET} ')
                    if len(palabra_aux)<cantidad_letras:
                        lista_palabras.append(palabra_aux.lower())
                        break
                    print(f'{c.ROJO}La palabra a cargar tiene que ser menor o igual a {cantidad_letras}{c.RESET}')
                except TypeError:
                    print(f'{c.ROJO}Solo puede ingresar numeros{c.ROJO}')             
        while True:
            nombre_csv = input(f'{c.CELESTE}Ingrese el nombre del archivo (sin el .csv): {c.RESET}')
            if len(nombre_csv)<30:
                break
            print('El nombre tiene que ser menor a 30')
        print('-------------------------------')
        print(f'{c.AMARILLO}Info previa:{c.RESET}')
        print(f'{c.CELESTE}Tamaño del tablero(Ancho y Largo): {c.VERDE}{len_tabla}{c.RESET}')
        print(f'{c.CELESTE}Lista de palabras:{c.RESET}')
        for palabra in lista_palabras:
            print(f'- {c.VERDE}{palabra}{c.RESET}')
        print(f'{c.CELESTE}Nombre del .csv: {c.VERDE}{nombre_csv}{c.RESET}')
        val = input('La informacion es correcta? (s/n): ')
        if (val.lower() == 's'):
            Escritor.escribir_tablero(len_tabla,lista_palabras,nombre_csv)

    def crear_jugador():
        print('-------------------------------')
        print(f'{c.AMARILLO}Creacion de jugador{c.RESET}')
        user = input(f'{c.CELESTE}Ingrese el nombre de usuario: {c.RESET}')
        clave = input(f'{c.CELESTE}Ingrese la contraseña: {c.RESET}')
        validar = input(f'{c.PURPURA}Escriba {c.CELESTE}SI{c.PURPURA} para confirmar: {c.RESET}')
        usuarios_aux = []
        if validar.lower() == 'si':
            arch = open('tableros/usuarios.csv','r+',newline='')
            next(arch, None)
            with arch:
                lector = csv.reader(arch)
                for linea in lector:
                    usuarios_aux.append(linea)
            arch = open('tableros/usuarios.csv', 'w+', newline='')
            with arch:
                lector = csv.DictWriter(arch, fieldnames=['usuario', 'clave', 'monedas'])
                lector.writeheader()
                for linea in usuarios_aux:
                    lector.writerow({'usuario': linea[0], 'clave': linea[1], 'monedas': linea[2]})
                lector.writerow({'usuario': user, 'clave': clave, 'monedas': 0})
            print(f'{c.VERDE}Usuario creado con exito{c.RESET}')
        else:
            print(f'{c.ROJO}Creacion de jugador cancelada{c.RESET}')

    def borrar_tablero(ruta):
        datos = [arch.name for arch in scandir(ruta) if arch.is_file()]
        print('-------------------------------')
        print(f'{c.AMARILLO}Sopas de letras: {c.RESET}')
        id_texto = 0
        datos_limpios = []
        for nombre in datos:
            texto = nombre.replace('.csv','')
            print(f'{c.CELESTE}{id_texto}.{c.RESET} {texto}')
            datos_limpios.append(texto)
            id_texto = id_texto + 1
        try:
            borrar = int(input('Ingrese el numero de codigo del archivo que desee borrar: '))
            print(f'Esta por borrar el archivo {c.CELESTE}{datos_limpios[borrar]}{c.RESET}')
            validar = input(f'Escriba {c.ROJO}CONFIRMAR{c.RESET} para borrarlo: ')
            if validar.upper() == 'CONFIRMAR':
                remove(f'Sopa de letras/tableros/tablas/{datos_limpios[borrar]}.csv')
                remove(f'Sopa de letras/tableros/soluciones/{datos_limpios[borrar]}_solucion.csv')
                print(f'{c.VERDE}Tablero eliminado{c.RESET}')
            else:
                print(f'{c.ROJO}Eliminacion de tablero cancelado{c.RESET}')
        except ValueError:
            print(f'{c.ROJO}Ingrese un dato numerico{c.RESET}')
        except IndexError:
            print(f'{c.ROJO}Ingrese un Index valido{c.RESET}')
    
    def borrar_jugador():
        user = input(f'{c.CELESTE}Ingrese el usuario a eliminar: {c.RESET}')
        clave = input(f'{c.CELESTE}Ingrese su contraseña: {c.RESET}')
        validar = input(f'{c.CELESTE}Escriba {c.ROJO}CONFIRMAR{c.CELESTE} si esta seguro: {c.RESET}')
        usuarios_aux = []
        confirmador = False
        if validar.lower() == 'confirmar':
            arch = open('tableros/usuarios.csv', 'r+', newline='')
            next(arch, None)
            with arch:
                linea = csv.reader(arch)
                for info in linea:
                    if info[0] == user and info[1] == clave:
                        print(f'{c.PURPURA}Usuario encontrado{c.RESET}')
                        confirmador = True
                    else:
                        usuarios_aux.append(info)
            if not confirmador:
                print(f'{c.ROJO}No se encontro ningun usuario con esos datos{c.RESET}')
            else:
                arch = open('tableros/usuarios.csv', 'w+', newline='')
                with arch:
                    linea = csv.DictWriter(arch, fieldnames=['usuario', 'clave', 'monedas'])
                    linea.writeheader()
                    for info in usuarios_aux:
                        linea.writerow({'usuario': info[0], 'clave': info[1], 'monedas': info[2]})
                print(f'{c.ROJO}Usuario eliminado con exito{c.RESET}')
        else:
            print(f'{c.ROJO}Eliminacion de usuario cancelada{c.RESET}')


class Escritor():
    def escribir_tablero(medida, palabras, nombre_csv):
        ubicacion = {}
        tabla = [["" for _ in range(medida)] for _ in range(medida)]
        for palabra in palabras:
            ubicacion[palabra] = {}
            selec = random.choice(['Horizontal', 'Vertical'])
            inicial_pos_x = random.randint(0, medida - len(palabra))
            inicial_pos_y = random.randint(0, medida - len(palabra))
            ubicacion[palabra]['x_inicial'] = inicial_pos_x
            ubicacion[palabra]['y_inicial'] = inicial_pos_y
            validar = True
            if selec == 'Horizontal':
                while True:
                    for letra in palabra:
                        if tabla[inicial_pos_x][inicial_pos_y] == "":
                            inicial_pos_x += 1
                        else:
                            validar = False
                    if not validar:
                        inicial_pos_x = random.randint(0,medida - len(palabra))
                        inicial_pos_y = random.randint(0,medida - len(palabra))
                        ubicacion[palabra]['x_inicial'] = inicial_pos_x
                        ubicacion[palabra]['y_inicial'] = inicial_pos_y
                        validar = True
                    else:
                        inicial_pos_x -= len(palabra)
                        for letra in palabra:
                            tabla[inicial_pos_x][inicial_pos_y] = letra
                            inicial_pos_x += 1
                        ubicacion[palabra]['x_final'] = inicial_pos_x
                        ubicacion[palabra]['y_final'] = inicial_pos_y
                        break
            if selec == 'Vertical':
                while True:
                    for letra in palabra:
                        if tabla[inicial_pos_x][inicial_pos_y] == "":
                            inicial_pos_y += 1
                        else:
                            validar = False
                    if not validar:
                        inicial_pos_x = random.randint(0,medida - len(palabra))
                        inicial_pos_y = random.randint(0,medida - len(palabra))
                        ubicacion[palabra]['x_inicial'] = inicial_pos_x
                        ubicacion[palabra]['y_inicial'] = inicial_pos_y
                        validar = True
                    else:
                        inicial_pos_y -= len(palabra)
                        for letra in palabra:
                            tabla[inicial_pos_x][inicial_pos_y] = letra
                            inicial_pos_y += 1
                        ubicacion[palabra]['x_final'] = inicial_pos_x
                        ubicacion[palabra]['y_final'] = inicial_pos_y
                        break
        for i in range(0, medida):
            for j in range(0, medida):
                if tabla[i][j] == "":
                    tabla[i][j] = random.choice(string.ascii_lowercase)
        arch = open('tableros/tablas/' + str(nombre_csv) + '.csv','w+',newline='')
        with arch:
            escritor = csv.writer(arch)
            for pos in tabla:
                escritor.writerow(pos)
        arch_solucion = open('tableros/soluciones/' + str(nombre_csv) + '_solucion.csv','w+',newline='')
        with arch_solucion:
            escritor = csv.DictWriter(arch_solucion, fieldnames=['palabra','x_inicial','y_inicial','x_final','y_final'])
            escritor.writeheader()
            for palabra in palabras:
                escritor.writerow({'palabra': palabra,
                'x_inicial': ubicacion[palabra]['x_inicial'],
                'y_inicial': ubicacion[palabra]['y_inicial'],
                'x_final': ubicacion[palabra]['x_final'],
                'y_final': ubicacion[palabra]['y_final']})
        print(f'{c.VERDE}Tablero generado con exito{c.RESET}')

class Obtener_Datos():
    def __init__(self) -> None:
        pass
    def obtener_datos_tableros(self, ruta):  
        while True:
            datos = [arch.name for arch in scandir(ruta) if arch.is_file()]
            print('-------------------------------')
            print(f'{c.AMARILLO}Lista de sopas de letras: {c.RESET}')
            id_texto = 0
            datos_limpios = []
            for nombre in datos:
                texto = nombre.replace('.csv','')
                print(f'{c.CELESTE}{id_texto}.{c.RESET} {texto}')
                datos_limpios.append(texto)
                id_texto = id_texto + 1
            visualizar = input('Desea visualizar algún tablero? (s/n): ')
            if visualizar.lower() == 'n':
                print(f'{c.VERDE}Volviendo al menu de tableros{c.RESET}')
                break
            elif visualizar.lower() == 's':
                try:
                    visualizar = int(input('Escriba la posicion del archivo que busca visualizar: '))
                    self.mostrar_tablero(self, datos_limpios[visualizar])
                except ValueError:
                    print(f'{c.ROJO}Ingrese valores numericos{c.RESET}')
                except IndexError:
                    print(f'{c.ROJO}Index equivocado, vuelva a intentar{c.RESET}')

    def mostrar_tablero(self, nombre):
        print('-------------------------------')
        print(f'{c.AMARILLO}Presentando el tablero: {c.CELESTE}{nombre}{c.RESET}')
        print('')
        tabla = open('tableros/tablas/' + nombre + '.csv', 'r+', newline='')
        with tabla:
            lector = csv.reader(tabla)
            for fila in lector:
                print(*fila, sep=' | ')
        print('')
        print(f'{c.AMARILLO}Respuestas y posiciones:{c.RESET}')
        tabla = open('tableros/soluciones/' + nombre + '_solucion.csv', 'r+', newline='')
        next(tabla, None)
        with tabla:
            lector = csv.reader(tabla)
            for fila in lector:
                print(f'{c.CELESTE}- Palabra: {c.RESET}{fila[0]}')
                print(f'{c.CELESTE}Pos X inicial: {c.RESET}{fila[1]}')
                print(f'{c.CELESTE}Pos Y inicial: {c.RESET}{fila[2]}')   
                print(f'{c.CELESTE}Pos X final: {c.RESET}{fila[3]}')
                print(f'{c.CELESTE}Pos Y final: {c.RESET}{fila[4]}')   
                input('Presione ENTER para continuar leyendo')
    
    def mostrar_jugadores(self):
        print('-------------------------------')
        print(f'{c.AMARILLO}Mostrando lista de jugadores: {c.RESET}')
        arch = open('tableros/usuarios.csv', 'r+', newline='')
        next(arch, None)
        with arch:
            lector = csv.reader(arch)
            for linea in lector:
                print(f'{c.CELESTE}- Usuario: {c.RESET}{linea[0]}')
                print(f'{c.CELESTE}. Clave: {c.RESET}{linea[1]}')
                print(f'{c.CELESTE}. Monedas: {c.RESET}{linea[2]}')
                print('')
        input(f'{c.VERDE}Presione Enter para continuar{c.RESET}')