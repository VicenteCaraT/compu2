import os


def main():
    print("Ejecutando 'sh' para iniciar una shell")

    # Reemplaza el proceso actual 'sh' inicializando una shell
    # -c: indica que el argumento siguiente es un comando que debe ejecutar
    # ps fax | grep python3: comando a ejecutar, muestra procesos en forma de arbol y filtra por lo procesos de python3
    os.execlp('sh', 'sh', '-c', 'ps fax | grep python3')
    # Nota: Este código no se ejecutará más allá de este punto en el proceso actual
    # Esta línea no se ejecutará ya que exec() cambia el curso de procesamiento
    print("Esta línea no se mostrará.") 

if __name__ == "__main__":
    main()