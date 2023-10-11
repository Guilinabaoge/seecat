import subprocess
from multiprocessing import Process

"""
    There are two threads running in this container. 
    Thread 1: Monitoring cat water bowl constantly using pi camera.
    Thread 2: Web server for user to access the pi camera image. 
    Each thread need exclusive access to the camera device. Therefore I need to implement a mutex lock to ensure thread safe. 
"""

def gunicorn_process(): 
    try:
        subprocess.run("gunicorn",check=True) 
    except subprocess.CalledProcessError as e:
        print(f"Error running Gunicorn: {e}")


def monitor_process():
    try:
        subprocess.run(["python3","monitor.py"],check=True) 
    except subprocess.CalledProcessError as e:
        print(f"Error running monitor: {e}")
        

p1 = Process(target=gunicorn_process)
p2 = Process(target=monitor_process)

p1.start()
p2.start()




