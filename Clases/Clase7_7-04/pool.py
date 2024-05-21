import os
from multiprocessing import Pool

def f(x):
    return (x*x ,os.getpid())

with Pool(processes=4) as pool: #process: cant de nucleos que ejecutan la tarea
    x = range(10)
    print(list(x))
    print(pool.map(f, range(10)))