import os, sys, time

cmd = "/bin/python3"

pid = os.fork()
if pid == 0:
    print(f"-> parent.py: CHILD with PID = {os.getpid()}\n")
    os.execv(cmd, (cmd, "child.py")) # /bin/python3 child.py
    sys.exit(99) #no se ejecuta ya que el exec cambia el curso de procesamiento por child.py
elif pid > 0:
    print(f"-> parent.py: PARENT with PID = {os.getpid()}")
    wval = print(os.wait())
    print(f"-> parent.py:\"child.py has finished with exit code {wval[1]>>8}\"")
else:
    print("Forking error")