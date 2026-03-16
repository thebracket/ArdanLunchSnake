#/usr/bin/python3
import time
from scratchpad import par_fibo

print("Multi thread")
results = []
t0 = time.time()
results = par_fibo(40)
t1 = time.time()
print(results)
print("Time: ", t1-t0)
