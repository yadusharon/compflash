import sys
import time
import random


for i in range(50):
    f = random.choice([sys.stdout,sys.stderr])
    f.write(str(i)+'\n')
    f.flush()
    time.sleep(0.1)
