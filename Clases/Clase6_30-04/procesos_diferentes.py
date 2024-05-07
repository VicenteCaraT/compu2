import multiprocessing

def proceso_1(mem_compartida, size):
    mensaje = b"Hola, soy el proceso 1!"
    mem_compartida.value = mensaje[:size]
    print(f"Proceso 1 ha escrito: {mensaje.decode()}")

def proceso_2(mem_compartida, size):
    mensaje = mem_compartida.value
    print(f"Proceso 2 ha recibido: {mensaje.decode()}")

if __name__ == "__main__":
    size = 200
    mem_compartida = multiprocessing.Array('c', b' ' * size, lock=True)
    
    p1 = multiprocessing.Process(target=proceso_1, args=(mem_compartida, size))
    p2 = multiprocessing.Process(target=proceso_2, args=(mem_compartida, size))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()