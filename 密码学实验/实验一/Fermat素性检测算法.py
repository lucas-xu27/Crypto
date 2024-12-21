import random
import math

contents = []
f=open("1.txt", 'r',encoding='utf-8')
contents.append(int(f.read()))
f=open("2.txt", 'r',encoding='utf-8')
contents.append(int(f.read()))
f=open("3.txt", 'r',encoding='utf-8')
contents.append(int(f.read()))
f=open("4.txt", 'r',encoding='utf-8')
contents.append(int(f.read()))

s = int(input("please choose the test data:"))
m = contents[s-1]
k = int(input("please choose the safety parameter:"))

for i in range(k):
    a = random.randint(2,m-2)
    g = math.gcd(a,m)
    if g != 1:
        break
    r = pow(a, m - 1, m)
    if r != 1:
        break

if i == k-1:
    p = 1 - pow(0.5,k)
    print("The probability that m is prime is",p)
else:
    print("m is a composite number")
