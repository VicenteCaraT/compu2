# 1- Escribir un programa en Python que acepte un número de argumento entero positivo n y genere una lista de los n primeros números impares. El programa debe imprimir la lista resultante en la salida estandar.

import os, argparse

def program_odd(n):
    return [2 * i + 1 for i in range(n)]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="prog1", description="This program given a positive number will generate a list of the first n odd numbers")
    parser.add_argument("n", type=int, help="a positive integer")
    args = parser.parse_args()

    if args.n <= 0:
        print("Please provide a positive inteder")
    else:
        odd_numbers = program_odd(args.n)
        print(odd_numbers)