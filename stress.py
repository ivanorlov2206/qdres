import quickdraw
import os
import time
import random
import threading
import sys

qd = quickdraw.QuickDraw("from_github.h5")
files = os.listdir("stress_images")
threads = int(sys.argv[1])
cnt = int(sys.argv[2]);

def test(n):
    for i in range(cnt):
        print(n)
        res = qd.classif("stress_images/" + files[random.randint(0, len(files) - 1)])

#t0 = time.time()

for i in range(threads):
    t = threading.Thread(target=test, args=(i,))
    t.start()

#print("Time:", time.time() - t0, 's')
