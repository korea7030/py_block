import hashlib
import binascii

private_key = '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'

# Base58 Encoding
s = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# version prefix 추가 - 0x80 ~ Private Key WIF
# 공개키를 compressed form으로 사용할 때는 뒤에 '01'을 추가로 붙인다
prefix_payload = '80' + private_key

# checksum을 구한다. version + payload에 double-SHA256을 수행하고 앞 부분의 4바이트를 prefixPayload뒤에 추가한다
version_payload = binascii.unhexlify(prefix_payload)
h = hashlib.sha256(hashlib.sha256(version_payload).digest()).digest()
h = ''.join('{:02x}'.format(y) for y in h)
version_payload_checksum = prefix_payload + h[0:8]

# Base58Check encoding을 수행
e_key = int(version_payload_checksum, 16)
base58 = ''
while(1):
    m, r = divmod(e_key, 58)
    base58 += s[r]
    if m == 0:
        break
    e_key = m

wif = base58[::-1]
print('\n 개인키 : (Hex) : ', private_key.lower())
print('개인키 WIF : ', wif)