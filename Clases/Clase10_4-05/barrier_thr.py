import threading
import time
import random

# Crear una Barrier para 4 hilos
barrier = threading.Barrier(5)

def worker():
    # Realizar alguna tarea antes de la barrera
    print("Tarea antes de la barrera. Hilo: ", threading.current_thread().name + '\n')
    time.sleep(random.randint(0, 1))
    # Esperar a que todos los hilos lleguen a la barrera
    barrier.wait()

    # Realizar alguna tarea después de la barrera
    print("Tarea después de la barrera. Hilo: ", threading.current_thread().name + '\n')

# Crear los hilos que ejecutan la función worker
threads = []
for _ in range(4):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()