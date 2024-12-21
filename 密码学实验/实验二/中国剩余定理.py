import math

s = int(input("please choose the test data:"))
filename = f"{s}.txt"
with open(filename, 'r', encoding='utf-8') as f:
    a1 = int(f.readline())
    a2 = int(f.readline())
    a3 = int(f.readline())
    m1 = int(f.readline())
    m2 = int(f.readline())
    m3 = int(f.readline())

if math.gcd(m1, m2) == 1 and math.gcd(m1, m3) == 1 and math.gcd(m2, m3) == 1:
    m = m1 * m2 * m3
    M1 = m // m1
    M2 = m // m2
    M3 = m // m3

    try:
        M1_inverse = pow(M1, -1, m1)
        M2_inverse = pow(M2, -1, m2)
        M3_inverse = pow(M3, -1, m3)

        x = (M1 * M1_inverse * a1 + M2 * M2_inverse * a2 + M3 * M3_inverse * a3) % m
        print(f"M1 is:{M1}")
        print(f"M2 is:{M2}")
        print(f"M3 is:{M3}")
        print(f"M1_inverse is:{M1_inverse}")
        print(f"M2_inverse is:{M2_inverse}")
        print(f"M3_inverse is:{M3_inverse}")
        print(f"x is: {x}")
        print(f"m is: {m}")
    except ValueError:
        print("One of the values does not have an inverse modulo the given modulus.")
else:
    print("The Chinese remainder theorem cannot be utilized directly because m1, m2, and m3 are not coprime.")

