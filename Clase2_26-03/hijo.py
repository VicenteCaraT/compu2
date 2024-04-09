import os, time

time.sleep(5) #añadido para ver el proceso
print('SOY EL HIJO INDEPENDIENTE (PID: %d -- SOY EL ABUELO PPID: %d)' % (os.getpid(), os.getppid()))


# PREGUNTA: porque el ppid luego es el bash?
# RESPUESTA: el ppid es el padre del proceso padre del hijo y el abuelo del hijo, por eso el ppid es el abuelo (el bash)
# al ejecutar dicho exec el PID entre el padre y el hijo es igual "watch fax | grep python3"
#PREGUNTA: Porque el PID del hijo es igual a la del padre
#RESPUESTA: El padre y el hijo tendrán el mismo PID ya que el hijo se ejecuta modificando el binario del padre.