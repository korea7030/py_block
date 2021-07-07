import binascii
import hashlib
from datetime import datetime

# big-endian <-> little-endian 변환
# x는 hex-string
def reverse(x):
    return ''.join(reversed([x[i:i+2] for i in range(0, len(x), 2)]))

def double_sha256(header):
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()

def make_header(version, prev_hash, merkle, timestamp, n_bits, nonce):
    h = str(hex(nonce))[2:]
    s = reverse(version) + reverse(prev_hash) + reverse(merkle) + reverse(timestamp) + reverse(n_bits) + reverse(h)
    return s

header = '00000020cfbf17b954f7baae49bff3a19fba1bef2032ff73384c1f0000000000000000007d4ced56ee79b139ab53ff4fd5be2ac022aaaff9ed5ca168a55547725acb935d233c485c33d62f17ff7b256a'


# Header hash를 계산하고 blockchain.info의 결과와 비교해 본다
h = double_sha256(binascii.unhexlify(header))
print("Header Hash = ", reverse(h.hex()))

# header를 decode한다.
version = reverse(header[0:0 + 4 * 2])        # 4 bytes
prev_hash = reverse(header[8: 8 + 32 * 2])     # 32 bytes
merkle_root = reverse(header[72: 72 + 32 * 2]) # 32 bytes
timestamp = reverse(header[136: 136 + 4 * 2]) # 4 bytes
n_bits = reverse(header[144: 144 + 4 * 2])     # 4 bytes
nonce = reverse(header[152: 152 + 4 * 2])     # 4 bytes

print('\nheader=', header)
print('\n\n version', version)
print('  prevhash=', prev_hash)
print('  currhash=', reverse(h.hex()))
print('merkleRoot=', merkle_root)
print("time stamp = %s [%s]" % (timestamp, datetime.utcfromtimestamp(int(timestamp,16)).strftime('%Y-%m-%d %H:%M:%S')))
print('  n_bits:', n_bits)
print('  nonce : ', int(nonce, 16))

# 다시 header로 조립
hdr = make_header(version, prev_hash, merkle_root, timestamp, n_bits, int(nonce, 16))
print('\n\n header : ', hdr)
