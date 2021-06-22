import bitcoin
# from bitcoin import sha256, decode_privkey, privkey_to_pubkey, pubkey_to_address, random_key

b_found = False
for i in range(10000):
    # 개인키 생성
    while(1):
        private_key = bitcoin.random_key()
        d_private_key = bitcoin.decode_privkey(private_key, 'hex')
        if d_private_key < 115792089237316195423570985008687907852837564279074904382605163141518161494337:
            break
    
    # 개인키로 공개키를 생성
    public_key = bitcoin.privkey_to_pubkey(private_key)

    # 공개키로 지갑주소를 생성
    address = bitcoin.pubkey_to_address(public_key, 0)

    # 지갑 주소 앞부분이 원하는 문자인지 확인
    if address[1:4] == 'ABC':
        b_found = True
        break

if b_found:
    print('\n\n개인키 : ', private_key)
    print('\n개인키 --> 공개키 : ', public_key)
    print('\n공개키 --> 지갑 주소 : ', address)
else:
    print('다시 시도')
