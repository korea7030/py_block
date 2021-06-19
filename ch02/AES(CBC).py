from Crypto.Cipher import AES
from Crypto import Random
import numpy as np


secret_key_128 = b'0123456701234567'
secret_key_192 = b'012345670123456701234567'
secret_key_256 = b'01234567012345670123456701234567'

# 128bit key
secret_key = secret_key_128
plain_text = 'This is Plain text. It will be encrypted using AES with CBC mode'
print('\n\n')
print('원문 : ')
print(plain_text)

# CBC 모드에서는 plain text가 128bit의 배수가 돼야 하므로 padding이 필요
n = len(plain_text)
if n % 16 != 0:
    n = n + 16 - (n % 16)
    plain_text = plain_text.join(n, '\0')

# initialization vector, iv도 수신자에게 보내야 함
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv) # 수신자에게 보낼 복사본

# 송신자는 secret_key와 iv로 plain text를 암호문으로 변환
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv)
aes = AES.new(secret_key, AES.MODE_CBC, iv)
cipher_text = aes.encrypt(plain_text.encode('utf-8'))
print('\n\n\n')
print('암호문 : ')
print(cipher_text.hex())

# 암호문. secret_key, iv를 수신자에게 보내면 수신자는 암호문을 해독할 수 있다
aes = AES.new(secret_key, AES.MODE_CBC, iv)
plain_text2 = aes.decrypt(cipher_text)
plain_text2 = plain_text2.decode()
print('\n\n\n')
print('해독문 : ')
print(plain_text2)
