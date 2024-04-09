import time, sys, os

print("="*50)

print(f"\n-> child.py: new process with PID = {os.getpid()}")

print("\nI am the NEW process. I REPLACED parent.py child thread when \"execv()\" was called.")

print("Sleeping for 3 seconds...\n\n" + "="*50 + "\n")

time.sleep(3)
sys.exit(30)