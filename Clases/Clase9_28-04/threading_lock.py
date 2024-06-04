import threading

# Recurso compartido
counter = 0
lock = threading.Lock()

def increment_counter():
    global counter
    for _ in range(1000):
        lock.acquire()
        counter += 1
        lock.release()

# Creación de los hilos
threads = []
for _ in range(10):
    thread = threading.Thread(target=increment_counter)
    threads.append(thread)
    thread.start()

# Espera a que todos los hilos terminen
for thread in threads:
    thread.join()

print(f"Valor final del contador: {counter}")