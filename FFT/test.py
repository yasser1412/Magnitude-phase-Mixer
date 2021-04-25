import subprocess as sp
import time 

print("y3m ana python")

start_time = time.time()

sp.call(["g++","test.cpp"])
sp.call("./a")

print("--- %s seconds ---" % (time.time() - start_time))