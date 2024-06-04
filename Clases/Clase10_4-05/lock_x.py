import threading
import time
import random
import matplotlib.pyplot as plt

x = 1
lock = threading.Lock()
path = []

def forward():
    global x
    flag = False
    lock.acquire()
    for i in range(10):
        flag = True
        time.sleep(random.randint(0, 1)/100) #Simula una tarea
        path.append(x)
        
        x *= 2
        
    if flag:
        print('Soy el hilo ', threading.current_thread().name, 'y he realizado la tarea.')
    else:
        print('Soy el hilo ', threading.current_thread().name, 'y esta vez no me tocó hacer nada...')
    lock.release()
    
def backward():
    global x
    flag = False
    lock.acquire()
    for i in range(10):
        flag = True
        time.sleep(random.randint(0, 1)/100) #Simula una tarea
        path.append(x)
        
        x /= 2
        
    if flag:
        print('Soy el hilo ', threading.current_thread().name, 'y he realizado la tarea.')
    else:
        print('Soy el hilo ', threading.current_thread().name, 'y esta vez no me tocó hacer nada...')
    lock.release()



# Crear dos hilos que calculen el problema
thread1 = threading.Thread(target=forward, name='Alan')
thread2 = threading.Thread(target=backward, name='John')

# Iniciar los hilos
thread2.start()
thread1.start()


# Esperar a que los hilos terminen
thread1.join()
thread2.join()

# Imprimir el valor final del contador
print("El resultado es:", x)

plt.plot(range(len(path)), path, '--bo')
plt.grid(True)
plt.show()