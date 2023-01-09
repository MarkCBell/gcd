
# Based on https://www.ams.org/journals/mcom/2008-77-261/S0025-5718-07-02017-0/S0025-5718-07-02017-0.pdf
# by Niels Martin Moller
# See Figure 5.

from math import gcd as gcd_base
from random import randrange

# 2x2 matrix things:
def apply_inv(M, A, B):
    ''' Return M^{-1} * [[A], [B]] '''
    u, up, v, vp = M
    w, x, y, z = M
    return vp * A + -up * B, -v * A + u * B

def mmult(M, Mp):
    ''' Return M * Mp '''
    w, x, y, z = M
    wp, xp, yp, zp = Mp
    return w*wp + x*yp, w*xp + x*zp, y*wp + z*yp, y*xp + z*zp

# Norms:
def pound(*args):
    return max(arg.bit_length() for arg in args)

def pound_(*args):
    return min(arg.bit_length() for arg in args)

# Helpers:
def sdiv(a, b, s=-1):
    a, b = max(a, b), min(a, b)  # a >= b
    if not b: return 0
    q, r = divmod(a, b)
    return q if pound(r) > s else q-1

def sdiv_step(A, B, S=-1):
    q = sdiv(A, B, S)
    return (1, q, 0, 1) if A > B else (1, 0, q, 1)

# Main:
def hgcd_d(A, B):
    ''' Return invertible M such that:
     - a & b have at least #(A, B) / 2 bits, and
     - a & b agree, except for up to possibly the last #(A, B) / 2 bits
    where [[a], [b]] = M * [[A], [B]],
    '''
    N = pound(A, B)
    S = N // 2 + 1
    Q = 3 * N // 4
    M = 1, 0, 0, 1  # Running total of all matrices we have applied.

    if pound_(A, B) <= S:
        return M  # Nothing to do.

    if pound_(A, B) > Q + 2:
        p1 = S - 1
        Mp = hgcd_d(A >> p1, B >> p1)
        A, B = apply_inv(Mp, A, B)
        M = mmult(M, Mp)

    while pound(A, B) > Q + 1 and pound(A - B) > S:
        Ms = sdiv_step(A, B, S)
        A, B = apply_inv(Ms, A, B)
        M = mmult(M, Ms)

    if pound_(A, B) > S + 2:
        N2 = pound(A, B)
        p2 = N - N2 + 3
        Mp = hgcd_d(A >> p2, B >> p2)
        A, B = apply_inv(Mp, A, B)
        M = mmult(M, Mp)

    while pound(A - B) > S:
        Ms = sdiv_step(A, B, S)
        A, B = apply_inv(Ms, A, B)
        M = mmult(M, Ms)

    assert M[0] * M[3] - M[1] * M[2] == 1
    assert pound_(A, B) > S
    assert pound(A - B) <= S
    return M


def gcd(A, B):
    # Each round pound(A, B) at least halves.
    # Hence only log_2(N) rounds are needed, each of which can be done in O(N log(N)) time.
    while pound_(A, B) > 10:  # We could drop back to classical (quadratic) GCD at any bound, including 0.
        A, B = apply_inv(hgcd_d(A, B), A, B)
        # Now A & B agree on at least the first half of their bits.
        A, B = apply_inv(sdiv_step(A, B), A, B)
        A, B = apply_inv(sdiv_step(A, B), A, B)

    return gcd_base(A, B)

if __name__ == '__main__':
    print(gcd(961697210359817202263303702018958750638744980169267464730824038734, 533145347706103984085623632875168339022233202940652359139605938490))
    print(gcd(881977367293790019891741237765792326366976618401959844946532357313, 1394094305888389051794636634143434282855635329783306699540532756256))
    print(gcd(0b101010110111010101000101010001010101001010100010100, 0b101010110111010101000101010001010101001010100010101))
    print(gcd(11335, 11579))
    print(gcd(1199, 1178))
    print(gcd(4797, 4715))
    print(gcd(1355091, 1473130))
    print(gcd(19305988327, 10249781048))
    print(gcd(1167069018940349606113996073591670634813765546847559999557817500338, 1039248469860445756831313176017102025282160112920673302131874661185))
    while True:
        a, b = randrange(1 << 1000), randrange(1 << 1000)
        print(a, b)
        print(gcd(a, b))

