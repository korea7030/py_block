# 비트코인에서 사용하는 타원곡선암호의 표준 문서인 secp256k1 도메인 파라미터 활용(ECDSA)
import math
import random
from Crypto.Hash import SHA256

# secp256k1의 Domain parameters
# y^2 = x^3 + 7 mod m
a = 0
b = 7
m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def add_operation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p
    
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    
    if p == q:
        # Doubling
        # slope (s) = (3 * x1 ^ 2 + a) / (2 * y1) mod m
        # 분모의 역원부터 계산한다 (by Fermat's Little Theorem)
        # pow() 함수가 내부적으로 Square-and-Multiply 알고리즘을 수행한다.
        r = 2 * y1
        rInv = pow(r, m-2, m)   # Fermat's Little Theorem
        s = (rInv * (3 * (x1 ** 2) + a)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m-2, m)
        s = (rInv * (y2 - y1)) % m
    x3 = (s ** 2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3

# 개인키 생성
def generate_private_key():
    while(1):
        d = random.getrandbits(256)
        if d > 0 & d < n:
            break
    return d

# 공개키 생성
def generate_public_key(d, g):
    bits = bin(d)
    bits = bits[2:len(bits)]

    K = g

    bits = bits[1:len(bits)]
    for bit in bits:
        K = add_operation(a, b, K, K, m)
        if bit == '1':
            K = add_operation(a, b, K, g, m)
    return K

message = '이 문서를 서명합니다.'
message = message.encode()

# 서명자의 개인키와 공개키 생성
d = generate_private_key()
Q = generate_public_key(d, G)

# ephemeral 키 생성
k = generate_private_key()
x, y = generate_public_key(k, G)
r = x % n

# Signing
h = SHA256.new()
h.update(message)
hx = h.hexdigest()
hx = int(hx, 16)

invK = pow(k, n-2, n)
s = ((hx + d * r) * invK) % n

# 전자서명을 보낸다
print('Message = ', message.decode() )
print('\n전자서명 생성 : ')
print('h(x) = ', hex(hx))
print('  r = ', hex(r))
print('  s = ', hex(s))
# =========================

# Verification
w = pow(s, n-2, n)
u1 = (w * hx) % n
u2 = (w * r) % n
v1 = generate_public_key(u1, G)
v2 = generate_public_key(u2, Q)
x, y = add_operation(a, b, v1, v2, m)

print('\n전자서명 확인 : ')
print('h(x) = ', hex(hx))
print('  r = ', hex(x))
print('  s = ', hex(r))

if r == x % n:
    print('\nValid Signature')
else:
    print('\nInvalid Signature')