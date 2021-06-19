from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# private key, public key 쌍을 생성
# private key는 소유자 보관, public key는 공개
key_pair = RSA.generate(2048)
private_key = key_pair.exportKey()
public_key = key_pair.publickey()

# key_pair의 p,q,e,d 를 확인
key_obj = RSA.import_key(private_key)
print('p = ', key_obj.p)
print('q = ', key_obj.q)
print('e = ', key_obj.e)
print('d = ', key_obj.d)

# 암호화할 원문
plain_text = 'This is plain text. It will be encrypted using RSA'
print('원문 : ', plain_text)

# 공개키로 원문을 암호화
cipher_text = public_key.encrypt(plain_text.encode(), 10)
print('암호문 : ', cipher_text[0].hex())

# private key를 소유한 수신자는 자신의 private key로 암호문을 해독
key = RSA.importKey(private_key)
plain_text2 = key.decrypt(cipher_text)
plain_text2 = plain_text2.decode()
print('해독문 : ', plain_text2)