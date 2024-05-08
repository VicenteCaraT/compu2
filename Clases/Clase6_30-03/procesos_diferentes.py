import multiprocessing 
import os 
import time

def proceso_1(mem_compartida, size):
    mensaje = b"Hola, soy el proceso 1!"  # msj a escribir
    
    #Data can be stored in a shared memory map using Value or Array. 
    mem_compartida.value = mensaje[:size]  # se escribe el msj en el array
    print(f"Proceso 1 {os.getpid()} ha escrito: {mensaje.decode()}")

def proceso_2(mem_compartida, size):
    mensaje = mem_compartida.value  # se lee el msj
    print(f"Proceso 2 {os.getpid()} ha recibido: {mensaje.decode()}")

# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    size = 200  # tamaño de la memoria compartida
    # se crea array compartido
    #c: indica tipo de dato que se va a almacenar en el array (bytes)
    #b ' ' * size :espacios en blanco  
    #bloqueo para que un solo proceso acceda al array
    mem_compartida = multiprocessing.Array('c', b' ' * size, lock=True)
    
    #se crean 2 procesos para cada función
    #target: funcion del proceso
    #args: argunemtos que se le van a dar a la funcion
    p1 = multiprocessing.Process(target=proceso_1, args=(mem_compartida, size))
    p2 = multiprocessing.Process(target=proceso_2, args=(mem_compartida, size))
    
    # se iniciam los procesos
    p1.start()
    p2.start()
    
    # terminan los procesos
    p1.join()
    p2.join()
    

#tambien se pueden comunicar a traves de un archivo