import time
import Queue
import sys
import threading
import subprocess

import os


from subprocess import call






def read_output(pipe, funcs):
    for line in iter(pipe.readline, ''):
        for func in funcs:
            func(line)
            # time.sleep(1)
    pipe.close()

def write_output(get):
    for line in iter(get, None):
        #sys.stdout.write(line)
        #print "test"
        print line
def thr():
    rand = "python random_print.py"
    rand2 = "avrdude -c usbtiny -p t44 -U flash:r:-:h"
    process = subprocess.Popen(rand2,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell =True,bufsize=1)
    q = Queue.Queue()
    out, err = [], []

    tout = threading.Thread(
        target=read_output, args=(process.stdout, [q.put, out.append]))

    terr = threading.Thread(
        target=read_output, args=(process.stderr, [q.put, err.append]))

    twrite = threading.Thread(target=write_output, args=(q.get,))

    for t in (tout, terr, twrite):
        t.daemon = True
        t.start()
    process.wait()
    for t in (tout, terr):
        t.join()
    q.put(None)
    #print(out)
    #print(err)

thr()


"""win= Text(root, height =20, width = 50).pack()
butn= Button(root, text="Click", command = thr).pack()
#win.insert(0,"hello")
root.mainloop()

"""
