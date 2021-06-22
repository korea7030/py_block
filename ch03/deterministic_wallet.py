import bitcoin as btc

seed = '초기 seed 값입니다.'

# n 개의 개인키를 만든다
n = 5
error = 0
for i in range(1, (n+1)):
    seed += str(i)
    private_key = btc.sha256(seed)
    d_private_key = btc.decode_privkey(private_key, 'hex')
    if d_private_key < btc.N:
        print('개인키 (%d) : %s' %(i, private_key))
    else: 
        error += 1

if error > 0:
    print('못만듦')