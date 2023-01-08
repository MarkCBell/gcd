
import logging
from itertools import takewhile
from math import gcd

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

def sequence(a, b):
    assert a >= b
    
    seq = []
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        yield q

def rebuild(seq):
    a, b, c, d = 1, 0, 0, 1
    # [[1, 0], [0, 1]]
    for q in seq:
        # [[0, 1], [1, -q]]
        a, b, c, d = c, d, a - q * c, b - q * d
    
    return a, b, c, d

def apply_mat(M, a, b):
    print('Applying:', M)
    w, x, y, z = M
    return w*a + x*b, y*a + z*b

def trial(a, b):
    while True:
        if b > a: a, b = b, a
        print(a, b)
        s_full = list(sequence(a, b))
        logging.debug('FULL: %s', s_full)
        A, B = str(a), str(b)
        
        if len(A) <= 2:
            return gcd(a, b)
        
        d = len(B) // 2
        p, q = int(A[:-d]), int(B[:-d])
        
        print('TRUCATE:', p, q)
        s_upper = sequence(p+1, q)
        s_lower = sequence(p, q+1)
        
        s_common = [i for i, j in takewhile(lambda x: x[0]== x[1], zip(s_lower, s_upper))]
        print(s_common)
        
        if s_common:
            a, b = apply_mat(rebuild(s_common), a, b)
        else:
            print('>>>> HAVE TO USE FULL:', s_full)
            a, b = apply_mat(rebuild(s_full[:1]), a, b)
    

print(trial(19305988327, 10249781048))


