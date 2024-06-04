import threading
import time


# Crear un semáforo con un contador inicial. Cambiar el contador para ver los distintos resultados.
semaphore = threading.Semaphore(1)

def worker():
    # Adquirir el semáforo
    semaphore.acquire()
    try:
        # Realizar alguna tarea crítica
        time.sleep(2)
        print("Realizando tarea crítica ")
    finally:
        # Liberar el semáforo
        semaphore.release()

# Crear varios hilos que ejecutan la función worker
threads = []
for _ in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()