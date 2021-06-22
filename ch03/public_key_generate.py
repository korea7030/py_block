import os
import math
import random
import time
import hashlib

# Additive Operation
def add_operation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p

    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]

    if p == q:
        # Doubling
        r = 2 * y1
        rInv = pow(r, m-2, m)
        s = (rInv * (3 * (x1 ** 2) + a))
    else:
        r = x2 - x1
        rInv = pow(r, m-2, m)
        s = (rInv * (y2 - y1)) % m
    x3 = (s ** 2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3

# CSPRNG 방식, os.urandom()와 random()을 적당히 섞어 hash256으로
def random_key():
    r = str(os.urandom(32)) + str(random.randrange(2**256)) + str(int(time.time() * 1000000))
    r = bytes(r, 'utf-8')
    h = hashlib.sha256(r).digest()
    key = ''.join('{:02x}'.format(y) for y in h)
    return key

a = 0
b = 7
m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 개인키 생성
while(1):
    d = int(random_key() , 16)
    if d > 0 & d < n:
        break

# Double-and-Add 알고리즘으로 공개키를 생성
bits = bin(d)
bits = bits[2:len(bits)]

# initialize, bits[0] = 1 (always)
K = G

# 두 번째 비트부터 Double-and-Add 알고리즘을 적용
bits = bits[1:len(bits)]
for bit in bits:
    # Double
    K = add_operation(a, b, K, K, m)

    if bit == '1':
        K = add_operation(a,b, K, G, m)

private_key = d
public_key = K
print('\n private key : ', hex(private_key))
print('\n public key : (%s, \n         %s)' % (hex(public_key[0]), hex(public_key[1])))