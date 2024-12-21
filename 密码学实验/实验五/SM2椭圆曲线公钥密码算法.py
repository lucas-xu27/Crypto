import hashlib
import os

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x, y):
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.p == 0

    def point_add(self, P, Q):
        if P is None: 
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 == -y2 % self.p:
            return None

        if P == Q:
            s = (3 * x1 ** 2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (s ** 2 - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_mult(self, k, P):
        R = None
        while k > 0:
            if k % 2 == 1:
                R = self.point_add(R, P)
            P = self.point_add(P, P)
            k //= 2
        return R

curve = EllipticCurve(a=0, b=7, p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def kdf(data: bytes, klen: int) -> bytes:
    ct = 1
    k = b''
    for i in range((klen + 31) // 32):
        k += hashlib.sha256(data + ct.to_bytes(4, 'big')).digest()
        ct += 1
    return k[:klen]

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt(message: bytes, pubkey, curve):
    k = int.from_bytes(os.urandom(32), 'big') % n
    C1 = curve.scalar_mult(k, G)
    print(f"k: {hex(k)}\n")
    
    h = k
    S = curve.scalar_mult(h, pubkey)
    if S is None:
        raise ValueError("Point S is at infinity. Aborting encryption.")

    shared_point = curve.scalar_mult(k, pubkey)
    print(f"shared_point: {shared_point}\n")
    x2, y2 = shared_point
    x2y2 = x2.to_bytes(32, 'big') + y2.to_bytes(32, 'big')

    t = kdf(x2y2, len(message))
    if all(b == 0 for b in t):
        raise ValueError("Derived key is all zeroes. Aborting.")
    print(f"t: {t.hex()}\n")

    C2 = xor_bytes(message, t)
    C3 = hashlib.sha256(x2.to_bytes(32, 'big') + message + y2.to_bytes(32, 'big')).digest()

    return C1, C2, C3

def decrypt(C1, C2, C3, privkey, curve):
    shared_point = curve.scalar_mult(privkey, C1)
    print(f"shared_point: {shared_point}\n")
    x2, y2 = shared_point
    x2y2 = x2.to_bytes(32, 'big') + y2.to_bytes(32, 'big')

    t = kdf(x2y2, len(C2))
    print(f"t: {t.hex()}\n")
    if all(b == 0 for b in t):
        raise ValueError("Derived key is all zeroes. Aborting.")

    message = xor_bytes(C2, t)

    u = hashlib.sha256(x2.to_bytes(32, 'big') + message + y2.to_bytes(32, 'big')).digest()
    print(f"u: {u.hex()}\n")

    if u != C3:
        raise ValueError("Hash mismatch. Decryption failed.")

    return message


def main():
    s = int(input("please choose the test data:"))
    filename = f"{s}.txt"
    with open(filename, 'r', encoding='utf-8') as f:
        plaintext = f.readline().strip()
    plaintext = plaintext.encode('utf-8')
    # plaintext = b"It is your own fault, I never wished you any sort of harm; but you wanted me to tame you."

    privkey = int.from_bytes(os.urandom(32), 'big') % n
    pubkey = curve.scalar_mult(privkey, G)

    print(f"p: {hex(curve.p)}\n")
    print(f"a: {hex(curve.a)}\n")
    print(f"b: {hex(curve.b)}\n")
    print(f"G: {G}\n")
    print(f"n: {n}\n")

    print(f"Plaintext: {plaintext}\n")
    
    print(f"Public Key: {pubkey}\n")
    print(f"Private Key: {privkey}\n")

    print("----------Encryption----------")
    C1, C2, C3 = encrypt(plaintext, pubkey, curve)
    print(f"C1: {C1}\n")
    print(f"C2: {C2.hex()}\n")
    print(f"C3: {C3.hex()}\n")
 
    print("----------Decryption----------")
    decrypted_message = decrypt(C1, C2, C3, privkey, curve)
    print(f"Decrypted Plaintext: {decrypted_message}\n")

    if plaintext == decrypted_message:
        print("Decryption successful and matches the original plaintext.")
    else:
        print("Decryption failed or mismatch.")

if __name__ == "__main__":
    main()