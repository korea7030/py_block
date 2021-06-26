import binascii
import bitcoin as btc
# import bitcoin.segwit_addr as bech32
import bitcoinutils.segwit_addr as bech32

# 개인키 생성
while (1):
    privKey = btc.random_key()                      # 256 bit Random number를 생성한다
    dPrivKey = btc.decode_privkey(privKey, 'hex')   # 16진수 문자열을 10진수 숫자로 변환한다
    if dPrivKey < btc.N:                            # secp256k1 의 N 보다 작으면 OK
        break

private_key='860ef116221744a5299c99a0ed726c15a2148a21a341fe522399c84a59771cfe01'
# 개인키로 공개키를 생성한다. Compressed format.
public_key = btc.privkey_to_pubkey(private_key)
c_public_key = btc.compress(private_key)

# 공개키로 160-bit public key hash를 생성한다
wit_prog = btc.bin_hash160(binascii.unhexlify(c_public_key))

# BIP-173 주소를 생성한다. (Base32 address format for native v0-16 witness outputs)
# P2WPKH
mainnet_addr = bech32.encode('bc', 0, wit_prog)
testnet_addr = bech32.encode('tb', 0, wit_prog)

# 결과
print("\n\n공개키 :", c_public_key)
print("Bech32 주소 (Mainnet P2WPKH) :", mainnet_addr)
print("Bech32 주소 (Testnet P2WPKH) :", testnet_addr)

print("\n\nBIP-173 문서의 Example 확인")
print("==========================")
cPubKey = '0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'

# 공개키로 160-bit public key hash를 생성한다
witprog = btc.bin_hash160(binascii.unhexlify(c_public_key))

# BIP-173 주소를 생성한다. (Base32 address format for native v0-16 witness outputs)
mainnet_addr = bech32.encode('bc', 0, witprog)
testnet_addr = bech32.encode('tb', 0, witprog)
print("\n공개키 :", cPubKey)
print("Bech32 주소 (Mainnet P2WPKH) :", mainnet_addr)
print("Bech32 주소 (Testnet P2WPKH) :", testnet_addr)