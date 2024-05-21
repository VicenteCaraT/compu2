"""
Ejercicio, modificar el código (usando los comandos de bash) para demostrar que
existe paralelismo real (forzar al kernel a que use más de un nucleo y ejecutar en simultaneo) (hacer que el worker haga más de una cosa)
(investigar como ver que los procesos se ejecuten en distintos nucleos)
"""

import multiprocessing

def worker(num):
    """Función que será ejecutada por cada proceso."""
    print(f'Worker: {num}')

if __name__ == '__main__':
    # Lista para mantener los procesos
    processes = []

    # Crear procesos
    for i in range(5):  # Crear 5 procesos
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()

    print("Procesamiento completado.")