"""
hacer que dos procesos hablen entre si a traves de una memoria compartida
"""
import mmap
import os

#tamaño de la región de memoria compartida en bytes
mem_size = 64

#To map anonymous memory, -1 should be passed as the fileno along with the length.
#MAP_ANONYMOUS : al ser una reginón de memoria anónima, no esta asociada a ningun archivo
#MAP_SHARED : indica que es una memoria compartida
mem = mmap.mmap(-1, mmap.MAP_ANONYMOUS | mmap.MAP_SHARED)

#se escribe en la memoria
#b: indica cadena tipo byte
mem.write(b"Prueba de IPC, memoria compartida")

#se establece el puntero de L/E en el inicio de la memoria y lee toda la region de 64 bytes
mem.seek(0)
data = mem.read(mem_size)
print(data)

#se libera el recurso
mem.close()