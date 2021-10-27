from colores import font_colors as c
from main_generador import Main as main_tablero
from main_juego import Main as main_juego

# Lobby principal del juego. De aqui se inicia el programa
def main():
    print('-------------------------------')
    print(f'{c.AMARILLO}SOPA DE LETRAS{c.RESET}')
    print('Hecho por: Martin Beltramino')
    print('-------------------------------')
    while True:
        print('Menu de opciones: ')
        print(f'{c.PURPURA}1.{c.RESET} Gestion de tableros y usuarios')
        print(f'{c.PURPURA}2.{c.RESET} Jugar')
        print(f'{c.PURPURA}0.{c.RESET} Salir')
        try:
            opcion = int(input('Ingrese opcion: '))
            if opcion == 1:
                main_tablero()
            elif opcion == 2:
                main_juego()
            elif opcion == 0:
                print(f'{c.VERDE}Hasta la proxima!{c.RESET}')
                break
            else:
                print(f'{c.ROJO}Elija la opcion correcta{c.RESET}')
        except ValueError:
            print(f'{c.ROJO}Ingrese un valor de tipo numerico entero{c.RESET}')
        print('-------------------------------')

main()