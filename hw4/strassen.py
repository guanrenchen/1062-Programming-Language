import multiprocessing as mp
import random
import time
import argparse
from pprint import pprint
import numpy as np
import os

def randm(w, h):
    return [ [random.randint(0,1) for x in range(w)] for y in range(h) ]

def zerom(w, h):
    rh = range(h)
    rw = range(w)
    return [ [0 for x in rw] for y in rh ]

def inverse(m):
    rh = range(len(m))
    rw = range(len(m[0]))
    return [ [ m[y][x] for y in rh ] for x in rw ]

def mulm(m1,m2):
    i2 = inverse(m2)
    return [ [sum(x*y for x,y in zip(a,b)) for b in i2] for a in m1 ]

def subm(m1, m2):
    return [ [a-b for a,b in zip(r1,r2)] for r1,r2 in zip(m1,m2)]

def addm(m1, m2):
    return [ [a+b for a,b in zip(r1,r2)] for r1,r2 in zip(m1,m2)]

def matchm(m1, m2):
    rn = range(len(m1))
    for i in rn:
        for j in rn:
            if m1[i][j] != m2[i][j]:
                return False
    return True

def standard(A, B):
    n = len(A)//2
    
    tmp = A[:n]
    a = [ row[:n] for row in tmp ]
    b = [ row[n:] for row in tmp ]
    tmp = A[n:]
    c = [ row[:n] for row in tmp ]
    d = [ row[n:] for row in tmp ]

    tmp = B[:n]
    e = [ row[:n] for row in tmp ]
    f = [ row[n:] for row in tmp ]
    tmp = B[n:]
    g = [ row[:n] for row in tmp ]
    h = [ row[n:] for row in tmp ]
    
    if n<=N_MIN:
        p0 = pool.apply_async(mulm, args=(a,e))
        p1 = pool.apply_async(mulm, args=(b,g))
        p2 = pool.apply_async(mulm, args=(a,f))
        p3 = pool.apply_async(mulm, args=(b,h))
        p4 = pool.apply_async(mulm, args=(c,e))
        p5 = pool.apply_async(mulm, args=(d,g))
        p6 = pool.apply_async(mulm, args=(c,f))
        p7 = pool.apply_async(mulm, args=(d,h))
        
        C00 = addm(p0.get(), p1.get())
        C01 = addm(p2.get(), p3.get())
        C10 = addm(p4.get(), p5.get())
        C11 = addm(p6.get(), p7.get())
    else:        
        C00 = addm(standard(a,e), standard(b,g))
        C01 = addm(standard(a,f), standard(b,h))
        C10 = addm(standard(c,e), standard(d,g))
        C11 = addm(standard(c,f), standard(d,h))

    return [r1+r2 for r1,r2 in zip(C00,C01)] + [r1+r2 for r1,r2 in zip(C10,C11)]

def strassen(A, B):
    n = len(A)//2
    
    tmp = A[:n]
    a = [ row[:n] for row in tmp ]
    b = [ row[n:] for row in tmp ]
    tmp = A[n:]
    c = [ row[:n] for row in tmp ]
    d = [ row[n:] for row in tmp ]

    tmp = B[:n]
    e = [ row[:n] for row in tmp ]
    f = [ row[n:] for row in tmp ]
    tmp = B[n:]
    g = [ row[:n] for row in tmp ]
    h = [ row[n:] for row in tmp ]
    
    if n<=N_MIN:
        p1 = pool.apply_async(mulm, args=(a,subm(f,h)))
        p2 = pool.apply_async(mulm, args=(addm(a,b),h))
        p3 = pool.apply_async(mulm, args=(addm(c,d),e))
        p4 = pool.apply_async(mulm, args=(d,subm(g,e)))
        p5 = pool.apply_async(mulm, args=(addm(a,d),addm(e,h)))
        p6 = pool.apply_async(mulm, args=(subm(b,d),addm(g,h)))
        p7 = pool.apply_async(mulm, args=(subm(a,c),addm(e,f)))
        
        p1 = p1.get()
        p2 = p2.get()
        C01 = addm(p1,p2)
        p3 = p3.get()
        p4 = p4.get()
        C10 = addm(p3,p4)
        p5 = p5.get()
        p6 = p6.get()
        C00 = addm(subm(addm(p5,p4),p2),p6)
        p7 = p7.get()
        C11 = subm(subm(addm(p1,p5),p3),p7)
    else:
        p1 = strassen(a,subm(f,h))
        p2 = strassen(addm(a,b),h)
        C01 = addm(p1,p2)
        p3 = strassen(addm(c,d),e)
        p4 = strassen(d,subm(g,e))
        C10 = addm(p3,p4)
        p5 = strassen(addm(a,d),addm(e,h))
        p6 = strassen(subm(b,d),addm(g,h))
        C00 = addm(subm(addm(p5,p4),p2),p6)
        p7 = strassen(subm(a,c),addm(e,f))
        C11 = subm(subm(addm(p1,p5),p3),p7)

    return [r1+r2 for r1,r2 in zip(C00,C01)] + [r1+r2 for r1,r2 in zip(C10,C11)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename', help='file with matrices')
    parser.add_argument('-n', action='store', dest='n_min', help='Leaf size')
    args = parser.parse_args()

    filename = args.filename
    N_MIN = int(args.n_min)

    
    os.system("taskset -p 0xff %d" % os.getpid())

    # with open(filename) as f:
    #     w,h = [ int(x) for x in f.readline().split(' ')[:2] ]
    #     m1 = [ [int(x) for x in f.readline().split(' ')[:w]] for i in range(h)] 
    #     m1 = np.array(m1, np.int64)
    #     w,h = [ int(x) for x in f.readline().split(' ')[:2] ]
    #     m2 = [ [int(x) for x in f.readline().split(' ')[:w]] for i in range(h)] 
    #     m2 = np.array(m2, np.int64)

    m1 = np.random.randint(10, size=(N_MIN,N_MIN))
    m2 = np.random.randint(10, size=(N_MIN,N_MIN))

    cpus = mp.cpu_count()
    with mp.Pool(processes=cpus) as pool:
        start = time.time()
        p = []
        for x in np.array_split(m1,cpus):
            p.append(pool.apply_async(np.matmul, args=(x,m2)))
        p = [x.get() for x in p]
        end = time.time()
        print('Elapsed time : {} (sec)'.format(end-start))
    
    # start = time.time()
    # np.matmul(m1,m2)
    # end = time.time()
    # print('Elapsed time : {} (sec)'.format(end-start))

