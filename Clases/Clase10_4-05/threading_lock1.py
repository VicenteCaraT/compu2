import threading
import time
import random

# Creamos una instancia de Lock
lock = threading.Lock()

# Variable compartida entre hilos
text = ''

# Función que incrementa el contador de forma segura
def complete_text():
    global text
    # Bloqueamos el acceso al contador
    lock.acquire()
    try:
        print(threading.current_thread())
        # Sección crítica: incrementamos el contador
        for l in threading.current_thread().name:
            text += l
            time.sleep(random.randint(0, 1)/100)
        text += '\n'
    finally:
        # Liberamos el bloqueo
        lock.release()
        pass

# Creamos varios hilos que incrementan el contador
threads = []
for _ in range(5):
    t = threading.Thread(target=complete_text)
    threads.append(t)
    t.start()

# Esperamos a que todos los hilos terminen
for t in threads:
    t.join()

# Imprimimos el resultado final
print("Text:\n", text)