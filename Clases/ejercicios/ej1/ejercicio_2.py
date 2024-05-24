#2- Escribir un programa en Python que acepte dos argumentos de línea de comando: una cadena de texto, un número entero. El programa debe imprimir una repetición de la cadena de texto tantas veces como el número entero.
import os, argparse

def program_repeat(s, n):
    return s * n

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="prog2", description="This program takes a string and a number, and prints the string repeated the given number of times")
    parser.add_argument("s", type=str, help="a string to be repeated")
    parser.add_argument("n", type=int, help="a positive integer indicating the number of repetitions")
    args = parser.parse_args()
    
    if args.n <= 0 or len(args.s) <= 0:
        print("Please enter an string and a positive number")
    else:
        repetition = program_repeat(args.s, args.n)
        print(repetition)
        