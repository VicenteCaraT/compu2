import os

r, w = os.pipe()

r = os.fdopen(r)
w = os.fdopen(w, 'w')

msg = input('Ingrese un mensaje: ')

w.write(msg)
w.close()

print('Mensaje Leído: ', r.readline())
r.close()