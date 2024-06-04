import threading, random
import numpy as np

def consumer(condition):
    global buffer
    print(threading.current_thread().name, 'Esperando a que finalice el cálculo... ')
    with condition:
        condition.wait()
        print('Elementos:', len(buffer))
        b = np.asarray(buffer)
        print('Suma de los cuadrados:', np.sum(b**2))

def producer(condition):
    global buffer
    print(threading.current_thread().name, 'Generando números... ')
    with condition:
        while len(buffer) <= 100:
            n = random.randint(1, 100)
            if n %2:
                buffer.append(n)
                
        print('Números impares generados')
        condition.notify_all()
        
buffer = []
condition = threading.Condition()
thread1 = threading.Thread(name='hilo1', target=consumer, args=(condition,))                      
thread2 = threading.Thread(name='hilo2', target=producer, args=(condition,))

thread1.start()
thread2.start()