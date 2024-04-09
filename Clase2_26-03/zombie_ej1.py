
import subprocess
import os
import time

# Crear un proceso hijo que termina inmediatamente
pid = os.fork()
if pid == 0:
    # Proceso hijo
    print("Este es el proceso hijo, terminando ahora.")
    os._exit(0) # salida forzada
else:
    # Proceso padre
    print(f"Este es el proceso padre, dejando al hijo {pid} como zombi.")
    time.sleep(20)  # Simular trabajo para dejar al hijo como zombi
    print("El proceso padre ha terminado, el hijo debería ser adoptado por init.")

# Nota: Este código debe ser ejecutado en un entorno seguro, ya que crea un proceso zombi.
# Una manera de matar un proceso zombie es matando el proceso padre
# con el cmd "kill -9 PID"
# Para encontrar estos procesos Zombies se utiliza "ps aux | grep 'Z", o "ps aux | grep defunct"
# Para encontrar el proceso padre relacionado al zombie se utiliza "ps -eo pid,ppid,comm | grep 'defunct'"