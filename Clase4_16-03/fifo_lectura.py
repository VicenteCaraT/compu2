import os

fifo_path = "/tmp/my_fifo"

#with open(fifo_path, 'r') as fifo:
#    message = fifo.read()
#    print(f"Mensaje FIFO: {message}")

while True:
    with open(fifo_path, 'r') as fifo:
        message = fifo.readline()
        print(f"Mensaje en FIFO: {message}")

#tarea crear bucle para que se lea la fifo en bucle los echo o escritura.
#hacer que procesos simultaneos escriban en la fifo

#un lector en bucle 2 o mas ecritores simultaneos

#un echo hola_mundo >1 "path"