import threading
import time

# Crear un BoundedSemaphore con un límite de 3 permisos
semaphore = threading.BoundedSemaphore(3)

def worker():
    # Adquirir el semáforo
    semaphore.acquire()
    try:
        # Realizar alguna tarea crítica
        time.sleep(2)
        print("Realizando tarea crítica")
    finally:
        # Liberar el semáforo
        semaphore.release()
        # semaphore.release()
        # semaphore.release()
        # semaphore.release()
        # semaphore.release()
        # semaphore.release()
        # semaphore.release()

# Crear varios hilos que ejecutan la función worker
threads = []
for _ in range(7):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()