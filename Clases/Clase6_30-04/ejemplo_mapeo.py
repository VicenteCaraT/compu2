"""
Ejemplo que muestra el uso de mmap para utilizarlo desde un único proceso para tener un archivo en memoria.
Correr en modo interactivo. En este archivo se dan comandos para jugar en la consola

"""

import mmap
import os

fd = os.open("lorem.txt", os.O_RDWR)

area = mmap.mmap(fd, 0)

area.read(18)

area.write(b'hola, me llamo vicente') #escribe donde se encuentre el puntero

area.tell() #localizacion del puntero
area.seek(0) #relocalizar puntero en 0
fd
"""
con el comando od se puede ver el archivo en bajo nivel. -c para que muestre los caracteres 
od -c <nombre archivo>
"""
