import os
import time

pipe = "/home/usuario/Documentos/mi_fifo"
        
def lector():
    pipe_lectura = open(file=pipe, mode="r")
    
    while True:
        contador_leido = pipe_lectura.readline()[:-1]
        print("Lector obtiene: " + contador_leido)

def escritor():
    pipe_escritura = os.open(path=pipe, flags=os.O_WRONLY)
    contador = 0
    
    while True:
        os.write(pipe_escritura, b"Numero %d\n" % contador)
        contador = contador + 1
        time.sleep(0.5)