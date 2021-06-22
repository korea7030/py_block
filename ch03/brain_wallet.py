from bitcoin import sha256, decode_privkey, privkey_to_pubkey, pubkey_to_address

# 특정 문자열로 256bit 개인키 생성
pass_phrase = 'Brain Wallet 시험용 개인키입니다. 잊어버리지 마세요.'
private_key = sha256(pass_phrase)
d_private_key = decode_privkey(private_key, 'hex')

if d_private_key < 115792089237316195423570985008687907852837564279074904382605163141518161494337:
    # 개인키로 공개키를 생성
    public_key = privkey_to_pubkey(private_key)

    # 공개키로 지갑 주소를 생성
    address = pubkey_to_address(public_key, 0)

    # 결과확인
    print('\n\n\Passphrase : ', pass_phrase)
    print('\n개인키 : ', private_key)
    print('개인키 ---> 공개키 : ', public_key)
    print('\n공개키 ---> 지갑 주소 : ', address)
else:
    print('요청하신 passphrase로 개인키를 만들었으나, 유효하지 않습니다.')