from multiprocessing import Process, Value
import ctypes

counter = Value(ctypes.c_int, 0)

num_increments = 100000

def increment_counter(counter):
    for _ in range(num_increments):
        counter.value += 1

def decrement_counter(counter):
    for _ in range(num_increments):
        counter.value -= 1

process1 = Process(target=increment_counter, args=(counter,))
process2 = Process(target=decrement_counter, args=(counter,))

process1.start()
process2.start()

process1.join()
process2.join()

process1(counter.value)
