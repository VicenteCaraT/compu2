import os, time



print('SOY EL PADRE (PID: %d)' % os.getpid(), 'SOY EL PADRE DEL PADRE (PID: %d)' %os.getppid())
time.sleep(5) #añadido para ver el proceso 
os.execlp('python3', 'python3', './hijo.py')
