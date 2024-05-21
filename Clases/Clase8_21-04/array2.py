from multiprocessing import Process, Array
import time

#clase de array compartido
class SharedArrayResource:
    def __init__(self, array):
        self.array = array

    def modify_array(self, index, value):
        with self.array.get_lock():  # Asegurar acceso exclusivo
            self.array[index] = value # se modifica el array en el indice con el valor
            print(f'Array modificado en índice {index}: {self.array[:]}')

#funcion que ejecuta cada proceso
def complex_array_example(resource, i):
    for idx in range(len(resource.array)): # itera sobre los indices del array
        time.sleep(0.1 * i)  # Diferente tiempo de espera para cada proceso
        resource.modify_array(idx, i * idx) #llama al método modify_array y le da como argumento el indice y el valor

if __name__ == '__main__':
    shared_array = Array('i', [0] * 5)  # Array de enteros inicializado a ceros
    resource = SharedArrayResource(shared_array) #instancia un objeto
    processes = [Process(target=complex_array_example, args=(resource, i)) for i in range(5)] # crea una lista de procesos

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f'Array final: {shared_array[:]}')