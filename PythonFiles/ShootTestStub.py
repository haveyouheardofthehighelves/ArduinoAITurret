import threading
import time

def shoot():
    while True:
        print("Shooting...")
        time.sleep(2)

thread = threading.Thread(target=shoot)
thread.daemon = True
thread.start()

try:
    for i in range(10):
        print("Main thread running...")
        time.sleep(1)
finally:
    print("Main thread finished.")
