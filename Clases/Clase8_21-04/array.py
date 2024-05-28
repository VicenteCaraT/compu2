"""
Array (class)
Es un tipo de memoria compartida en el modulo multiprocessing de python, 
permite crear y manipular arrays que pueden ser compartidos entre procesos.

Args:
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
typecode_or_type determines the type of the elements of the returned array: it is either a ctypes type or a one character typecode
then it determines the length of the array, and the array will be initially zeroed. Otherwise, size_or_initializer is a sequence which is used to initialize the array and whose length determines the length of the array.
If lock is True (the default) then a new lock object is created to synchronize access to the value. 
If lock is a Lock or RLock object then that will be used to synchronize access to the value.
Array('tipo de dato':int, 'tamaño de lista o una lista':int|list).

Al ser de acceso concurrente se debe aplicar una sincronización para evitar la condición de carrera.
"""

from multiprocessing import Process, Array

def simple_array_example(arr, i): # toma el array compartido y el indice
    arr[i] = arr[i] ** 2 # se eleva al cuadrado la posicion i
    print(f'Array en proceso {i}: {arr[:]}') # imprime el array y el proceso

if __name__ == '__main__':
    shared_array = Array('i', range(5))  # Array de enteros 'i' es un tipo de dato
    processes = [Process(target=simple_array_example, args=(shared_array, i)) for i in range(5)] # se crea una lista de procesos y cada proceso ejecuta el target

    for p in processes: # se inician los procesos
        p.start()
    for p in processes: # se espera a que los procesos terminen
        p.join()

    print(f'Array final: {shared_array[:]}') # imprime el array final