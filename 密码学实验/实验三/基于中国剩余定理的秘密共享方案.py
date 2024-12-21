import math
import random

def generate_d(k,n):
    while True:
        d = []
        for i in range(n):
            d.append(random.randint(10**170,10**180))

        coprime = all(math.gcd(d[i], d[j]) == 1 for i in range(n) for j in range(i + 1, n))
        if not coprime:
            continue
        d.sort()
        
        N = d[0]*d[1]*d[2]
        M = d[3]*d[4]
        if N > k and k > M:
            for i in range(5):
                print(f"d{i+1} is:{d[i]}")
            print(f"N is:{N}")
            print(f"M is:{M}")
            return d
        
def generate_k(k,d):
    subk = [k % di for di in d]
    return subk

def recover_k(subk,d,t):
    m = 1
    for i in range(t):
        m *= d[i]
    
    M = [m // d[i] for i in range(t)]
    M_inverse = [pow(M[i], -1, d[i]) for i in range(t)]
    
    x = sum(subk[i] * M[i] * M_inverse[i] for i in range(t)) % m
    print(f"k is {x}")
    return x


def main():
    s = int(input("please choose the test data:"))
    filename = f"secret{s}.txt"
    with open(filename, 'r', encoding='utf-8') as f:
        k = int(f.readline())
        
    d = generate_d(k,5)
    subk = generate_k(k,d)
    x = recover_k(subk,d,2)
    if x==k:
        print("Decryption successful")
    else:
        print("Decryption failure")

if __name__ == "__main__":
    main()
