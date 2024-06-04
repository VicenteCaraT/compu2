import threading, queue

# q = queue.LifoQueue()
q = queue.Queue()   # FIFO

def worker():
    while True:
        item = q.get() # toma un elemento de la cola
        print(f'Working on {item}') # imprime en que elemento de la cola esa trabajando
        print(f'Finished {item}') # indica cuando termina con dicho elemento
        q.task_done() # tarea completada

# turn-on the worker thread
th = threading.Thread(target=worker, daemon=True) #creación del hilo, daemon:indica que el hilo se detiene cuando el programa principal termine
th.start() # se inicia el hilo

# send thirty task requests to the worker
for item in range(30):
    print(f'Putting item {item}')
    q.put(item) # se añadan 30 elementos en la cola q
print('All task requests sent\n', end='')

# block until all tasks are done
q.join()
# th.join()
print('All work completed')