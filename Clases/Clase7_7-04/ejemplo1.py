import mmap
import os
import time

mem_size = 64
mem = mmap.mmap(-1, mmap.MAP_ANONYMOUS | mmap.MAP_SHARED)

pid = os.fork()

if pid != 0:
    print(f"Padre pid <{os.getpid()}> esta escribiendo...")
    mem.write(b"Hola, yo soy tu abuelo!!.")
    os.waitpid(pid, 0)
    
    mem.seek(0)
    msj_nieto = mem.read(mem_size)
    print(f"Mensaje recibido por el nieto: {msj_nieto.decode()}") 
    
    mem.close()

else:
    pid_nieto = os.fork()
    if pid_nieto != 0:
        print("Creando un hijo...")
        os.waitpid(pid_nieto, 0)
    else:
        time.sleep(1)
        mem.seek(0) 
        msj_abuelo = mem.read(mem_size)
        print(f"Mensaje recibido por el abuelo: {msj_abuelo.decode()}")
        
        print(f"Nieto pid <{os.getpid()}> esta respondiendo...")
        
        mem.seek(0) 
        mem.write(b"Hola soy tu nieto.....")
        
        mem.close()