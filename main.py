import time
import threading

import Modules.SerialParser as serial
import Modules.ThreadWithReturn as threading

THREAD_POOL = []
DINNNERRRRRR = ["Baecon", "Vasta", "Zpagetthiee", "Pizzah", "Buerguer"]

def sampleFunction(arg):
    print(f"Thread {arg} started...")
    time.sleep(1)
    return arg


if __name__ == "__main__":

    for food in DINNNERRRRRR:
        new_thread = threading.ThreadWithReturn( target=sampleFunction, args=(food,) )
        THREAD_POOL.append(new_thread)

    for thread in THREAD_POOL:
        thread.start()

    print("\nWaiting for threads to finish")

    for thread in THREAD_POOL:
        ret_val = thread.join()
        print(f"Thread #{ret_val} finished...")

    print("All thread job finished")
