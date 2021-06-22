import os
import random
import time
import hashlib

# secp256k1의 Domain parameter
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# CSPRNG 방식, os.urandom()와 random()을 적당히 섞어서 hash256으로 256비트의 난수를 생성
def random_key():
    r = str(os.urandom(32)) + str(random.randrange(2**256)) + str(int(time.time() * 1000000))
    r = bytes(r, 'utf-8')
    h = hashlib.sha256(r).digest()
    key = ''.join('{:02x}'.format(y) for y in h)
    return key

while(1):
    private = random_key()
    if int(private, 16) < N:
        break

print('Private Key (Hex) : ', private)
print('Private Key (DEC) : ', int(private, 16))