import os
import time

fifo_path = "/tmp/my_fifo"

while True:
    with open(fifo_path, 'w') as fifo:
        time.sleep(3)
        fifo.write("Hola desde escritor")
