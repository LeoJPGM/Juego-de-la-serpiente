import os
import time
import random
import msvcrt
import sys

# Dimensiones del tablero
ANCHO = 40
ALTO = 20

# Direcciones
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)

class Serpiente:
    def __init__(self):
        self.cuerpo = [(ANCHO // 2, ALTO // 2)]
        self.direccion = DERECHA
        self.crecer = False
        
    def mover(self):
        cabeza = self.cuerpo[0]
        nueva_cabeza = (cabeza[0] + self.direccion[0], cabeza[1] + self.direccion[1])
        
        # Verificar colisión con paredes
        if (nueva_cabeza[0] < 0 or nueva_cabeza[0] >= ANCHO or 
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= ALTO):
            return False
        
        # Verificar colisión consigo misma
        if nueva_cabeza in self.cuerpo:
            return False
        
        self.cuerpo.insert(0, nueva_cabeza)
        
        if not self.crecer:
            self.cuerpo.pop()
        else:
            self.crecer = False
            
        return True
    
    def cambiar_direccion(self, nueva_direccion):
        # Evitar que la serpiente se mueva en dirección opuesta
        if (self.direccion[0] + nueva_direccion[0] != 0 or 
            self.direccion[1] + nueva_direccion[1] != 0):
            self.direccion = nueva_direccion
    
    def comer(self):
        self.crecer = True

class Juego:
    def __init__(self):
        self.serpiente = Serpiente()
        self.comida = self.generar_comida()
        self.puntuacion = 0
        self.game_over = False
        
    def generar_comida(self):
        while True:
            comida = (random.randint(0, ANCHO - 1), random.randint(0, ALTO - 1))
            if comida not in self.serpiente.cuerpo:
                return comida
    
    def actualizar(self):
        if not self.serpiente.mover():
            self.game_over = True
            return
        
        # Verificar si comió
        if self.serpiente.cuerpo[0] == self.comida:
            self.serpiente.comer()
            self.comida = self.generar_comida()
            self.puntuacion += 10
    
    def dibujar(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Crear tablero
        tablero = [[' ' for _ in range(ANCHO)] for _ in range(ALTO)]
        
        # Dibujar serpiente
        for i, (x, y) in enumerate(self.serpiente.cuerpo):
            if i == 0:
                tablero[y][x] = 'O'  # Cabeza
            else:
                tablero[y][x] = 'o'  # Cuerpo
        
        # Dibujar comida
        tablero[self.comida[1]][self.comida[0]] = '*'
        
        # Borde superior
        print('┌' + '─' * ANCHO + '┐')
        
        # Dibujar tablero
        for fila in tablero:
            print('│' + ''.join(fila) + '│')
        
        # Borde inferior
        print('└' + '─' * ANCHO + '┘')
        
        # Mostrar puntuación
        print(f'\nPuntuación: {self.puntuacion}')
        print('Usa las flechas o WASD para moverte. Presiona ESC para salir.')
    
    def leer_tecla(self):
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            
            # Teclas de flecha (retornan dos bytes)
            if tecla == b'\xe0':
                tecla = msvcrt.getch()
                if tecla == b'H':  # Flecha arriba
                    return ARRIBA
                elif tecla == b'P':  # Flecha abajo
                    return ABAJO
                elif tecla == b'K':  # Flecha izquierda
                    return IZQUIERDA
                elif tecla == b'M':  # Flecha derecha
                    return DERECHA
            
            # Teclas WASD
            elif tecla == b'w' or tecla == b'W':
                return ARRIBA
            elif tecla == b's' or tecla == b'S':
                return ABAJO
            elif tecla == b'a' or tecla == b'A':
                return IZQUIERDA
            elif tecla == b'd' or tecla == b'D':
                return DERECHA
            
            # ESC para salir
            elif tecla == b'\x1b':
                return 'ESC'
        
        return None
    
    def ejecutar(self):
        while not self.game_over:
            self.dibujar()
            
            # Leer entrada del usuario
            tecla = self.leer_tecla()
            if tecla == 'ESC':
                print("\n¡Juego terminado!")
                return
            elif tecla:
                self.serpiente.cambiar_direccion(tecla)
            
            # Actualizar juego
            self.actualizar()
            
            # Velocidad del juego
            time.sleep(0.1)
        
        # Pantalla de Game Over
        self.dibujar()
        print('\n╔════════════════════════╗')
        print('║     GAME OVER!         ║')
        print(f'║  Puntuación: {self.puntuacion:3d}       ║')
        print('╚════════════════════════╝')

def main():
    print("¡Bienvenido al Juego de la Serpiente!")
    print("\nInstrucciones:")
    print("- Usa las flechas o WASD para moverte")
    print("- Come la comida (*) para crecer")
    print("- No choques con las paredes ni contigo mismo")
    print("- Presiona ESC para salir")
    print("\nPresiona cualquier tecla para comenzar...")
    msvcrt.getch()
    
    juego = Juego()
    juego.ejecutar()

if __name__ == "__main__":
    main()
