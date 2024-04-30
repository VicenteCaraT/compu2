import os

fifo_path = '/tmp/my_fifo'

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

while True:
    with open(fifo_path, 'r') as fifo:
        message = fifo.readline()
        print(f"Mensaje en FIFO: {message}")

#tarea crear bucle para que se lea la fifo en bucle los echo o escritura.
#hacer que procesos simultaneos escriban en la fifo

#un lector en bucle 2 o mas ecritores simultaneos

#un echo hola_mundo >1 "path"