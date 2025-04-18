import os
import time


start_time=time.time()

for _ in range(100):
    os.system("python main.py --read --name 'rotos initis'")
    
end_time = time.time()

print("time it took: ", int(1000 * (end_time - start_time) ) )