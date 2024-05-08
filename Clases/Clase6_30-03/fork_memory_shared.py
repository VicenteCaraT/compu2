"""
hacer que dos procesos hablen entre si a traves de una memoria compartida
"""
import mmap
import os
import time

#tamaño de la memoria compartida en bytes
mem_size = 64

#To map anonymous memory, -1 should be passed as the fileno along with the length.
#MAP_ANONYMOUS : al ser una reginón de memoria anónima, no esta asociada a ningun archivo
#MAP_SHARED : indica que es una memoria compartida
mem = mmap.mmap(-1, mmap.MAP_ANONYMOUS, mmap.MAP_SHARED) #MAP_PRIVATE (memoria privada)

pid = os.fork()

#proceso padre
if pid != 0:
    print(f"Padre pid <{os.getpid()}> esta escribiendo...")
    mem.write(b"Hola, yo soy tu padre!!.") # el padre escribe en memoria
    os.waitpid(pid, 0) # espera a que el hijo termine
    
    mem.seek(0) # posiciona puntero L/E en el inicio de la memoria
    msj_hijo = mem.read(mem_size) # se lee el msj del hijo
    print(f"Mensaje recibido por el hijo: {msj_hijo.decode()}") 
    
    mem.close() # cierra el recurso
#proceso hijo
else:
    time.sleep(1) # espera por si a caso
    mem.seek(0) # posiciona el puntero L/E en el inicio de la memoria
    msj_padre = mem.read(mem_size) # lee el msj del padre
    print(f"Mensaje recibido por el padre: {msj_padre.decode()}")
    
    print(f"Hijo pid <{os.getpid()}> esta respondiendo...")
    mem.seek(0) # vuelve al inicio de la memoria
    mem.write(b"NOOOOOO...") # escribe msj al padre
    
    mem.close() # cierra recurso
    
    
    