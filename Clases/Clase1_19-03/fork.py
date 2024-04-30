import os
import time

def main():
    print(f'Proceso padre PID: {os.getpid()}')

    pid = os.fork()
    print(pid) #Imprime el pid que recibe el padre al llamar a fork y el hijo no realia ningun fork, por lo cual devuelve 0

    if pid == 0:
        #Hereda la mayoría de los atributos del proceso padre, incluyendo el código en ejecución, las variables, el entorno de ejecución y los descriptores de archivo abiertos.
        #codigo que ejecuta el hijo
        print(f'Este es el proceso hijo, PID: {os.getpid()}')
        time.sleep(3)
        print('Termina el hijo')
    elif pid > 0:
        #codigo que ejecuta el padre
        print(f'Este es el proceso padre, PID todavia: {os.getpid()}')
        os.wait() #padre espera a que el hijo termine
        print('Termian el padre')
    else:
        print('fork fallo')

if __name__ == '__main__':
    main()