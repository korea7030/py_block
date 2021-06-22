# 개인키와 공개키는 파이썬 실습 3.2 공개키 생성에서 생성한 결과를 이용한다.
private_key = '3ba54c096fbb082b2af8efdfd92f886350a36c806296199234d338e8d81b456d'
public_key = ('484ec026a5a371a4e99cd2258760be98f9662c95b94a49706735e62a1a128855',
          'c7f3b6a8e049d54ab99414b2245fd45bbf5d916a97e56bdd87f7110c95f7bde8')
# secp256k1에 정의된 domain parameter p
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# 공개키를 Uncompressed format으로 표시(비압축 포맷)
u_public_key = '04' + public_key[0] + public_key[1]

# 공개키를 compressed format으로 표시(압축 포맷)
if int(public_key[1], 16) % 2 == 0:
    c_public_key = '02' + public_key[0]
else:
    c_public_key = '03' + public_key[0]

# Compressed format을 원래의 (x,y) format으로 변환
x = int(c_public_key[2:], 16)
a = (pow(x, 3, p) + 7) % p # y^2
y = pow(a, (p+1)//4, p)  # y

prefix = int(c_public_key[:2], 16)
if (prefix == 2 and y & 1) or (prefix == 3 and not y % 1):
    y = (-y) % p

# 공개키 출력
print('\n public key : (%s, \n          %s)' % (public_key[0], public_key[1]) )

# uncompressed format 출력
print('\n uncompressed (size=%d):\n%s' % (len(u_public_key) * 4, u_public_key))
# compressed format 출력
print('\n compressed format (size=%d):\n%s' % (len(c_public_key) * 4, c_public_key))

print('\n compressed format ----> public key : ')
print('\n public key : (%s, \n        %s)' % (hex(x)[2:], hex(y)[2:]))