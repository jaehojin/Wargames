from random import randint, shuffle
import sympy as sp
from sympy.abc import x

def is_prime(n: int) -> bool:
    for i in range(2, int(n**0.5)+1):
        if n%i == 0:
            return False
    return True

def is_2_power(n: int) -> bool:
    return n != 0 and (n & (n-1) == 0)

def invert_poly(f: sp.Poly, R: sp.Poly, p: int) -> sp.Poly:
    if is_prime(p):
        inv_poly = sp.invert(f, R, domain=sp.GF(p))
    elif is_2_power(p):
        inv_poly = sp.invert(f, R, domain=sp.GF(2))
        e = p.bit_length()-1
        for _ in range(1, e):
            inv_poly = ((2 * inv_poly - f * inv_poly ** 2) % R).trunc(p)
    return inv_poly.set_domain('ZZ')

def bytes_to_bits(b: bytes) -> list[int]:
    bits = [int(b) for b in ''.join(["{0:08b}".format(x) for x in b])]
    return bits

def bits_to_bytes(bits: list[int]) -> bytes:
    if len(bits) % 8 != 0:
        bits = [0] * (8-len(bits)%8) + bits
    b = b''
    for i in range(0,len(bits),8):
        b += int(''.join([str(x) for x in bits[i:i+8]]),2).to_bytes(length=1, byteorder='big')
    return b

def bytes_to_coeffs(b: bytes) -> list[int]:
    coeffs = []
    for i in range(0, len(b), 2):
        coeffs.append(int.from_bytes(b[i:i+2],'big',signed=True))
    return coeffs

def coeffs_to_bytes(coeffs: list[sp.Integer]) -> bytes:
    b = b''
    for c in coeffs:
        b += int(c).to_bytes(2,'big',signed=True)
    return b

class NTRU:
    def __init__(self, N: int, p: int, q: int, verbose: bool=False):
        if verbose:
            print("[*] Initiating NTRU system... ")
            print(f"[+] System parameter: {N = }, {p = }, {q = }")
        self.N, self.p, self.q = N,p,q
        self.R = sp.poly(x**N-1, x)
        if verbose:
            print("[+] Generating Secret keys ... ")
        self._gen_sk()
        self._gen_pk()
        if verbose:
            print(f"[+] Public Key = {self.h.all_coeffs()}")    

    def _rand_coeffs(self, n: int, balanced: bool = False) -> list[int]:
        if balanced:
            half = [randint(0,1) for _ in range(n//2)]
            res = half+[x*(-1) for x in half]
            if n % 2 == 1:
                res += [0]
            shuffle(res)
            return res
        return [randint(-1, 1) for _ in range(n)]

    def _gen_sk(self):
        try:
            self.f = sp.Poly(self._rand_coeffs(self.N), x)
            self.g = sp.Poly(self._rand_coeffs(self.N), x)
            self.fp = invert_poly(self.f, self.R, self.p)
            self.fq = invert_poly(self.f, self.R, self.q)
        except sp.NotInvertible:
            self._gen_sk()

    def _gen_pk(self):
        self.h = ((self.p * self.fq * self.g) % self.R).trunc(self.q)

    def encrypt(self, plaintext: bytes) -> bytes:
        pt = sp.Poly(bytes_to_bits(plaintext), x)
        r = sp.Poly(self._rand_coeffs(self.N, balanced = True), x)

        ct = ((r*self.h+pt) % self.R).trunc(self.q)

        ciphertext = coeffs_to_bytes(ct.all_coeffs())
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        ct = sp.Poly(bytes_to_coeffs(ciphertext), x)

        a = ((self.f * ct) % self.R).trunc(self.q)
        b = a.trunc(self.p)
        pt = (self.fp*b % self.R).trunc(self.p)

        plaintext = bits_to_bytes(pt.all_coeffs())
        return plaintext

if __name__ == '__main__':
    import os
    cipher = NTRU(N=509, p=3, q=2048)
    for _ in range(0x100):
        pt = os.urandom(10)
        ct = cipher.encrypt(pt)
        dt = cipher.decrypt(ct)
        print(pt.hex(), dt.hex())
        assert pt == dt
