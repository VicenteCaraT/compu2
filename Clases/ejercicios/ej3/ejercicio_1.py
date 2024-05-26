# 1- Escribir un programa en Python que comunique dos procesos. El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, contar la cantidad de palabras que contiene y mostrar ese número.
import os, argparse

def pipe_program(file_path):
    r_parent, w_child = os.pipe()
    r_child, w_parent = os.pipe()
    pid = os.fork()
    try:
        if pid > 0:
            os.close(r_parent)
            os.close(w_parent)
            with open(file_path, 'r') as file:
                for line in file:
                    os.write(w_child, line.encode())
                    
                    #Leer respuesta del hijo
                    word_count = os.read(r_child, 1024).decode().strip()
                    print(f"Conteo de palabras recibido por el hijo: {word_count}")
            os.close(w_child)
            os.wait()
        else:
            os.close(w_child)
            os.close(r_child)
            
            while True:
                line = os.read(r_parent, 1024).decode()
                if not line:
                    break
                word_count = len(line.split())
                os.write(w_parent, str(word_count).encode())
            os.close(r_parent)
            os.close(w_parent)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="pipe_comunication")
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()
    
    if args.file:
        pipe_program(args.file)
    else:
        print("No file option specified.")