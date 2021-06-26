import binascii
import bitcoin as btc

#P2WPKH nested in P2SH
script_sig = '0014a4b4ca48de0b3fffc15404a1acdc8dbaae226955'

script_hash = '2928f43af18d2d60e8a843540d8086b305341339'

print ('\n\n사례 : txid = c586389e5e4b3acb9d6c8be1c19ae8ab2795397633176f5a6442a261bbdefc3a')
print("\nCombined Script (without Witness) :")
print("\n<%s> OP_HASH160 <%s> OP_EQUAL" % (script_sig, script_hash))

# validity check : OP_HASH160
check = btc.bin_hash160(binascii.unhexlify(script_sig))

if check.hex() == script_hash:
    print('\n==> valid script')
else:
    print('\n==> invalid script')