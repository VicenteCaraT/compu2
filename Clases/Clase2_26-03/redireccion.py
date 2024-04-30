import sys, os, time


print('PID: %d' %os.getpid())


fh = open('test.txt', 'w')
time.sleep(30)


input('Antes de redireccionar')
sys.stderr = fh
time.sleep(30)
print('Esta línea va a test.txt', file=sys.stderr)

sys.Popen('ccc')

input('Despues de redireccionar')


sys.stderr = sys.__stderr__

fh.close()