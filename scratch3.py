import logging
from itertools import takewhile
from math import gcd as gcd_base

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

def sdiv(a, b, s):
    q, r = divmod(a, b)
    return (q, r) if r.bit_length() > s else (q-1, r+b)

def sdiv_step(A, B, M, S):
    w, x, y, z = M
    if A > B:
        q, A = sdiv(A, B, S)
        w, x, y, z = w, q*w + x, y, q*y + z
    else:
        q, B = sdiv(B, A, S)
        w, x, y, z = w + q*x, x, y + q*z, z
    
    return A, B, (w, x, y, z)

def pound(*args):
    return max(arg.bit_length() for arg in args)

def pound_(*args):
    return min(arg.bit_length() for arg in args)

def split(A, p):
    upper, lower = A >> p, A & ((1 << p) - 1)
    assert A == (upper << p) + lower
    return upper, lower

def mmult(M, Mp):
    w, x, y, z = M
    wp, xp, yp, zp = Mp
    return w*wp + x*yp, w*xp + x*zp, y*wp + z*yp, y*xp + z*zp

def helper(A, B, p):
    a, Ap = split(A, p)  # TO DO.
    b, Bp = split(B, p)
    alpha, beta, M = hgcd_d(a, b)
    u, up, v, vp = M
    # A, B = M_inv * (A, B)
    An = (alpha << p) + vp * Ap + -up * Bp
    Bn = (beta << p) + -v * Ap + u * Bp
    assert An == vp * A + -up * B
    assert Bn == -v * A + u * B
    return An, Bn, M

def hgcd_d(A, B):
    A0, B0 = A, B
    print(bin(A), bin(B))
    N = pound(A, B)
    S = N // 2 + 1
    Q = 3 * N // 4
    if pound_(A, B) > Q + 2:
        p1 = S - 1  # N // 2
        A, B, M = helper(A, B, p1)
    else:
        M = 1, 0, 0, 1
    
    while pound(A, B) > Q + 1 and pound(A - B) > S:
        A, B, M = sdiv_step(A, B, M, S)
    
    if pound_(A, B) > S + 2:
        N2 = pound(A, B)
        p2 = 2*S - N2 + 1
        A, B, Mp = helper(A, B, p2)
        M = mmult(M, Mp)
    
    while pound(A - B) > S:
        A, B, M = sdiv_step(A, B, M, S)
    
    # print(A, B, M, A0, B0)
    assert A == M[3] * A0 + -M[1] * B0
    assert B == -M[2] * A0 + M[0] * B0
    return A, B, M


GCD_THRESHOLD = 30

def gcd(A, B):
    while pound(A, B) > GCD_THRESHOLD:
        A, B, _ = hgcd_d(A, B)
    
    return gcd_base(A, B)


print(gcd(19305988327, 10249781048))


