#getops: herramienta de python que sirve para analizar argumentos de la línea de comandos.
import getopt
import sys

def main(argv):
    # Definir las opciones cortas y largas
    opciones_cortas = "h"
    opciones_largas = ["nombre="]
    
    # Intentar analizar los argumentos de la línea de comandos
    try:
        argumentos, valores = getopt.getopt(argv, opciones_cortas, opciones_largas)
    except getopt.GetoptError:
        # Imprimir el modo de uso si se encuentran opciones inválidas
        print('Uso: ejemplo_getopt.py -h --nombre <nombre>')
        sys.exit(2)
        
    for argumento, valor in argumentos:
        if argumento == '-h':
            print('Ayuda: ejemplo_getopt.py -h --nombre <nombre>')
            sys.exit()
        elif argumento in ("--nombre"):
            print(f"Nombre: {valor}")

if __name__ == "__main__":
    main(sys.argv[1:])
    
    

#python3 getops_ej.py -h
#python3 getops_ej.py --nombre vicente
