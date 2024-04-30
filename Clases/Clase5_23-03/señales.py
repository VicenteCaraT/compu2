import os
import signal

def enviar_sig(pid, sig):
    try:
        os.kill(pid, sig)
        print(f"Señal {signal.Signals(sig).name} enviada al proceso con PID {pid}")
    except ProcessLookupError:
        print("Error: No se encontró el proceso.")
    except PermissionError:
        print("Error: Permiso denegado.")

# Ejemplo de uso
pid = 47583  # Reemplazar con el PID real del proceso (sleep -time &)
sig = signal.SIGTERM  # Señal para terminar el proceso

enviar_sig(pid, sig)