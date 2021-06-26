from bitcoin.bci import history
from bitcoin.transaction import mktx, sign
from urllib.request import urlopen
from urllib.parse import urlencode

url = "https://testnet.blockchain.info/"

A = 0 # 송금자(A)
B = 1 # 수금자(B)

address = ['mhJH61ScRnWJrhJm6283BbmACr27FjzT4Y', 'mg5urjMQZpALgga9GmwZaiiKKyBftxe7Mt']
private_key = ['7c06fcd8b6d7ef34182dd86882f5f1f1834381c132653b4f6937065167062b10', '8126b6e1b33432198cbf9139174b470285b085fd4a0ccb6cc439f31cdbf3d298']

# 서드파티 API 서버에 UTXO 요청
def get_utxo(n=A):
    if n == A or n == B:
        h = history(address[n])
        return list(filter(lambda txo: 'spend' not in txo, h))
    else:
        print('address error.')

# transaction data packet 생성
# input, output을 생성
def make_tx(utxo, n1=A, n2=B, value=0.01, fee=0.0001):
    # input 생성
    tot_value = 0
    inputs = []
    for i in range(len(utxo)):
        tot_value += utxo[i]['value'] * 1e-8
        inputs.append(utxo[i])

        # 송금할 금액만큼 utxo선택. 최적화는 아니고 앞에서부터 소비
        if tot_value > (value + fee):
            break
        
    # 수수료를 차감한 금액을 계산
    # 수수료(Fee)를 뺀 나머지는 my_addr1 으로 재송금
    # 재송금 하지 않으면 모두 fee로 간주되어 miner가 가져간다
    out_change = tot_value - value - fee
    chg_satoshi = int(out_change * 1e8)

    # transaction 데이터 생성
    outputs = [{'value': int(value * 1e8), 'address': address[n2]}, {'value': chg_satoshi, 'address': address[n1]}]
    tx = mktx(inputs, outputs)
    return tx, len(inputs)

# 송금자의 private key로 서명한다. scriptsig를 생성
def sign_tx(utxo, tx, n_input=1, n_priv=A):
    for i in range(n_input):
        tx = sign(tx, i , private_key[n_priv])
    return tx

# 서드파티 API 서버에 TX전송 요청
def send_tx(tx):
    params = {'tx': tx}
    payload = urlencode(params).encode('UTF-8')
    response = urlopen(url + 'pushtx', payload).read()
    print(response.decode('utf-8'))

if __name__ == '__main__':
    utxo = get_utxo(A)
    print(utxo)