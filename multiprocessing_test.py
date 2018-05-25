import time
from multiprocessing import Process, Value, Lock

class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

    def func(self, counter):
        for i in range(50):
            time.sleep(0.01)
            counter.increment()

if __name__ == '__main__':
    counter = Counter(0)
    procs = [Process(target=counter.func, args=(counter,)) for i in range(10)]
    
    time0 = time.time()
    for p in procs: p.start()
    for p in procs: p.join()
    time1 = time.time()
    
    print(time1 - time0)
    print(counter.value())
    
    counter = Counter(0)
    
    time0 = time.time()
    for i in range(500):
        time.sleep(0.01)
        counter.increment()
    time1 = time.time()
    
    print(time1 - time0)
    print(counter.value())
