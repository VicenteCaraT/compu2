import threading
import time

# Función que será ejecutada por los hilos
def print_numbers():
    for i in range(5):
        print(f"Número: {i}")
        time.sleep(1)

def print_letters():
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(f"Letra: {letter}")
        time.sleep(1)

# Creación de los hilos
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Inicio de los hilos
thread1.start()
thread2.start()

# Espera a que ambos hilos terminen
thread1.join()
thread2.join()

print("Hilos completados.")

# ps -eLf
# para ver los hilos de cada proceso
# en este caso se crean 3 hilos, el hilo principal y los demas creados
# crea hilos de kernel