# single_threaded.py
import time
from threading import Thread

COUNT = 50000000

def countdown(n):
    while n>0:
        n -= 1

def SingleThread():
    start = time.time()
    countdown(COUNT)
    end = time.time()
    print(end - start, 's to execute code in single threaded mode')

def MultiThread():
    t1 = Thread(target=countdown, args=(COUNT//2,))
    t2 = Thread(target=countdown, args=(COUNT//2,))
    start = time.time()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time.time()
    print(end - start, 's to execute code in multi threaded mode')


def main():
    SingleThread()
    MultiThread()


if __name__ == "__main__":
    main()


