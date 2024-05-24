#1- Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar relizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.
import os, argparse, random, math

def fork_program():
    number = random.randint(0, 100)
    pid = os.fork()
    if pid == 0:
        negative_sqrt = -math.sqrt(number)
        print(f"Chilf: Negative square root of {number}: {negative_sqrt:.2f}")
    else:
        positive_sqrt = math.sqrt(number)
        print(f"Parent: Positive square root of {number}: {positive_sqrt:.2f}")
        os.wait()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="fork_example", description="Program to demonstrate fork and argument parsing")
    parser.add_argument("-f", "--fork", action="store_true", help="Perform fork and calculate square roots")
    args = parser.parse_args()
    
    if args.fork:
        fork_program()
    else:
        print("No fork option specified.")