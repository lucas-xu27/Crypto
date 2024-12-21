import random
import sympy

def generate_strong_prime(bits):
    while True:
        q = sympy.randprime(pow(10,bits-1),pow(10,bits))
        p = 2 * q + 1
        
        if sympy.isprime(p) and len(str(p)) == 150:
            return p, q

def primitive_root(p,q):
    for g in range (2,p-1):
        if pow(g,2,p) != 1 and pow(g,q,p)!= 1:
            break
    return g



s = int(input("please choose the test data:"))
filename = f"secret{s}.txt"
with open(filename, 'r', encoding='utf-8') as f:
    m = int(f.readline())

p, q = generate_strong_prime(150)
g = primitive_root(p,q)
print(f"p = {p},  g = {g}")

a = random.randint(0,p-2)
A = pow(g,a,p)
print(f"g^a = {A}")

#加密
k = random.randint(1,p-1)
c1 = pow(g,k,p)
c2 = m*pow(g,a*k,p)
print(f"k = {k}")
print(f"C = ({c1},{c2})")

#解密
V = pow(c1,a,p)
inverse_V = pow(V,p-2,p)
m_prime = c2*inverse_V % p
print(f'm_prime = {m_prime}')
if (m == m_prime):
    print("decryption success")



