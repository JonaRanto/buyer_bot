import subprocess

subprocesos = 2

for i in range(subprocesos):
    subprocess.Popen(['python', 'p.py', 'hola'], creationflags=subprocess.CREATE_NEW_CONSOLE)
