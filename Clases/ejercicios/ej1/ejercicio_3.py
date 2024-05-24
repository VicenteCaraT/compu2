#3- Escribir un programa en Python que acepte argumentos de línea de comando para leer un archivo de texto. El programa debe contar el número de palabras y líneas del archivo e imprimirlas en la salida estándar. Además el programa debe aceptar una opción para imprimir la longitud promedio de las palabras del archivo. Esta última opción no debe ser obligatoria. Si hubiese errores deben guardarse el un archivo cuyo nombre será "errors.log" usando la redirección de la salida de error.
import os, argparse


def count_words_and_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            return num_lines, num_words, lines
    except Exception as e:
        with open("error.log", "a") as error_log:
            error_log.write(str(e) + "\n")
        return None, None, None

def calculate_average_file(lines):
    total_word_length = sum(len(word) for line in lines for word in line.split())
    total_words = sum(len(line.split()) for line in lines)
    return total_word_length / total_words if total_words > 0 else 0 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="file_detaill", description="thos program takes a file and counts the amount of words and lines of the file")
    parser.add_argument("-f", "--file", required=True, type=str, help="Path to the text file")
    parser.add_argument("-av", "--average", action="store_true", help="Calculate the average word length")
    args = parser.parse_args()

    num_lines, num_words, lines = count_words_and_lines(args.file)
    if num_lines is not None and num_words is not None:
        print(f"Number of lines: {num_lines}")
        print(f"Number of words: {num_words}")
        if args.average:
            average_words_file = calculate_average_file(lines)
            print(f"Average word length: {average_words_file:.2f}")
    else:
        print("An error occurred while processing the file. Please check errors.log for details.")