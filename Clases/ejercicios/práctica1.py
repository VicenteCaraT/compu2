import os, argparse, time

# hacer funcion que lea las lineas del file y las apendee en una lista, 
# despues crear la comunicacion por medio de pipes e ir iterando a lo largo 
# de la lista creando hijos y que esos hijos den vuelta cada linea que les llegue 
# por medio del pipe, luego de darlas vuelta, le dara el string al padre.
#Este programa de be esperar a que todos los hijos terminen

def read_line(file):
    linea = b""
    while True:
        char = os.read(file, 1)
        if char == b"" or char == b"\n":
            break
        linea += char
    return linea
#la funcion de contar las lineas se puede hacer aca, y que le de una string preparada y sin \n a program()

def program(file):
    # Crear dos pipes: uno para que el padre envíe datos al hijo y otro para que el hijo envíe datos al padre
    r, w = os.pipe()
    r2, w2 = os.pipe()
    with open(file, "rb") as f:
        lines = f.readlines()
        clean_lines = [line.rstrip(b"\n") for line in lines]
        
        for child in range(len(clean_lines)):
            pid = os.fork()
            if pid == 0:
                os.close(w)
                os.close(r2)
                
                line = read_line(r)
                os.close(r)
                
                reversed_line = line[::-1]  # Invertir la línea
                os.write(w2, reversed_line + b"\n")  # Escribir la línea invertida en el segundo pipe
                os.close(w2)
                os._exit(0)
            else: 
                os.close(r)
                os.close(w2) 
                os.write(w, clean_lines[child] + b"\n")  # Escribir la línea original en el primer pipe
                os.close(w) 
                
                # Leer la línea invertida del segundo pipe e imprimirla
                inverted_line = read_line(r2)
                print(inverted_line.decode("utf-8"))

                # Crear un nuevo pipe para el próximo hijo
                r, w = os.pipe()
                r2, w2 = os.pipe()

        # Esperar a que todos los procesos hijos terminen
        for _ in range(len(clean_lines)):
            os.wait()

        os.close(r2)
        os.close(w2)
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="revez", description="Este programa invierte las filas de un texto pasado por argumento")
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()
    
    try:
        program(args.file)
    except FileExistsError:
        print(f"El archivo {args.file} no existe.")
    except PermissionError:
        print(f"No posees los permisos para acceder al archivo {args.file}.")
    except IsADirectoryError:
        print(f"{args.file} es un directorio, no un archivo.")
