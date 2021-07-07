import binascii
import hashlib
import time
from datetime import datetime

# big-endian <-> little-endian 변환
# x는 hex-string
def reverse(x):
    return ''.join(reversed([x[i:i+2] for i in range(0, len(x), 2)]))

def double_sha256(header):
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()

def make_header(version, prev_hash, merkle, timestamp, n_bits):
    s = reverse(version) + reverse(prev_hash) + reverse(merkle) + reverse(timestamp) + reverse(n_bits)
    return s

# 압축형 타깃을 일반형으로 변환
def uncompact(bits):
    # bit의 왼쪽 1bytes(exponents)를 추출
    exponents = bits >> 24

    # bits의 오른쪽 3bytes(coefficient)를 추출
    coefficient = bits & 0x007fffff

    # target value 계산
    target = coefficient << 8 * (exponents - 3)
    return target

# 일반형 타깃을 압축형으로 변환
def compact(target):
    # target의 길이
    n_len = target.bit_length()

    # compact format 변환
    n_len = ((n_len + 7) & ~0x7)
    exponents = (int(n_len/8) & 0xff)
    coefficient = (target >> (n_len - 24)) & 0xfffff

    if coefficient & 0x800000:
        coefficient >>= 8
        exponents += 1
    return (exponents << 24) | coefficient

# header 정보
prev_hs = '00000000000000000028a9837a638d6ab0b0aa51cd97c87cefd7ca0b5ca55201'
merkle = '5299b7778e8409227af85b00ca4f006717a5d7e90470012779441deea32b67ce'
target = 0x1745fb53
version = '20000000'              # 4 bytes
prev_hash = prev_hs                 # 32 bytes
merkle_root = merkle               # 32 bytes
timestamp = '5ae7502d'            # 4 bytes
n_bits = f"{target:#0{10}x}"[2:]   # 4 bytes

# nonce를 제외한 header 조립
hdr = make_header(version, prev_hash, merkle_root, timestamp, n_bits)

# nonce 값을 0 부터 1씩 증가시키면서 header의 hash 계산
# hash값이 n_bits보다 작은 nonce값을 찾는 것이 목적
target_value = uncompact(target)

# nonce(=3647874098) 값을 알고있으므로, 이 주변으로 시험
for nonce in range(3647874000, 0xffffffff):
    # nonce 값을 포함한 header를 생성
    n_s = f"{nonce:#0{10}x}"[2:]
    header = hdr + reverse(n_s)

    # header의 hash값을 계산
    h = hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()
    print(nonce, reverse(h.hex()))

    # hash값이 n_bits보다 작은지 확인
    rh = int(reverse(h.hex()), 16)
    if rh < target_value:
        # nonce 찾으면 break
        break
    nonce += 1

print("\n   Version =", version)
print("  prevHash =", prev_hash)
print("merkleRoot =", merkle_root)
print("time stamp = %s [%s]" % (timestamp, datetime.utcfromtimestamp(int(timestamp,16)).strftime('%Y-%m-%d %H:%M:%S')))
print("     nBits =", n_bits)
print('     nonce = %d <-- Found' % nonce)
print('Header =', header)
print('\nHash =', reverse(h.hex()))

# 100만번 돌려보고 hash power 측정
start_time = time.time()
for nonce in range(0, 1000000):
    # nonce값을 포함한 header 생성
    n_s = f"{nonce:#0{10}x}"[2:]
    header = hdr + reverse(n_s)

    # header의 hash값을 계산
    h = hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()

    # hash값이 n_bits보다 작은지 확인
    rh = int(reverse(h.hex()), 16)
    if rh < target_value:
        pass

end_time = time.time()
elapsed = end_time - start_time
print('\n\nHash power 측정 :')
print('Elapsed time (100 만회) = %.2f (sec)' % elapsed)
print('Hash power (Python & CPU & i7 processor) = %.2f (hash/sec)' % (nonce / elapsed))