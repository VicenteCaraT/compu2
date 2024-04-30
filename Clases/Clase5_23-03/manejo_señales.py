import signal, os, time

def handler(s, f):
    print("Terminando... ")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

print(signal.getsignal(signal.SIGINT))

signal.signal(signal.SIGINT, handler)

print(signal.getsignal(signal.SIGINT))

time.sleep(100)

"""
Esta función se ejecuta cuando se recibe SIGINT. 
Imprime un mensaje y restablece el manejador de SIGINT al 
comportamiento por defecto del sistema (signal.SIG_DFL), 
que terminará el proceso si se recibe otra vez SIGINT.
"""

#desde otra terminal buscar pid y enviar señal -2