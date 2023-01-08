import logging
from itertools import takewhile
from math import gcd

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

def sequence(x, y):
    assert x >= y
    x_o, y_o = x, y
    
    a, b, c, d = 1, 0, 0, 1
    while y:
        q, r = divmod(x, y)
        a, b, c, d = c, d, a - q * c, b - q * d
        print(q)
        x, y = y, r
        
    assert x == a*x_o + b*y_o
    assert y == c*x_o + d*y_o
    
    return x, (a, b, c, d)

def trial(x, y):
    if y > x: x, y = y, x

    print(x, y)
    X, Y = str(x), str(y)
    if len(X) <= 2:
        return gcd(a, b)
    
    d = len(Y) // 2
    p, q = int(X[:-d]), int(Y[:-d])
    print('TRUCATE:', p, q)
    
    _, (a, b, c, d) = sequence(p, q)
    print(a, b, c, d)
    
    m, n = a*x + b*y, c*x + d*y
    assert gcd(m, n) == gcd(x, y)
    
    return trial(m, n)
    
    

print(trial(19305988327, 10249781048))


