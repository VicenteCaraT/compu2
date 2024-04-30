import os
import time


pipe_name = '/tmp/pipe_test'


def child():
    pipeout = os.open(pipe_name, os.O_WRONLY)
    counter = 0

    while True:
        os.write(pipeout, b'Number %03d\n' % counter)         
        counter = (counter+1) % 5
        time.sleep(1)


def child_v2():
    pipeout = open(pipe_name, 'w')
    counter = 0

    while True:
        pipeout.write('Number %03d\n' % counter)
        counter = (counter+1) % 5
        pipeout.flush()
        time.sleep(1)


def parent():
    pipein = open(pipe_name, 'r')

    while True:
        line = pipein.readline()[:-1]
        print('Parent %d got "%s" al %s' % (os.getpid(), line, time.time()))


if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)


pid = os.fork()

if pid != 0:
    parent()
else:
    child_v2()
    
    """
<Versión 1 (child)>: Abre la tubería en modo escritura, escribe una cadena de texto que incluye un contador 
que se reinicia después de alcanzar 5, y espera un segundo entre cada escritura.

<Versión 2 (child_v2)>: Similar a la versión 1 pero utilizando la sintaxis de manejo de archivos de alto nivel 
de Python (open() en lugar de os.open()), e incorpora flush() para asegurar que el contenido se escribe en la tubería sin retrasos.
    """