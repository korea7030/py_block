# target -> normal change 난이도 측정
def target_value(bits):
    # bit의 왼쪽 1 byte(exponents) 추출
    exponents = bits >> 24

    # bits의 오른쪽 3byte(coefficient) 추출
    coefficient = bits & 0x007fffff

    # target value를 계산
    target = coefficient << 8 * (exponents - 3)

    # difficulty 계산
    genesis_targetvalue = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
    difficulty = genesis_targetvalue / target

    return target, difficulty

# block 559834의 target bits의 target value와 difficulty 계산
target_bits = 0x172fd633
target, difficulty = target_value(target_bits)

print('\n\n target bits = ', hex(target_bits))
print('target value = ', hex(target))
print('  difficulty = ', difficulty)

# block 559834의 block hash는 아래와 같고, 이 값은 target보다 작다.(valid)
block_hash = 0x0000000000000000001aa4184c12376e3da18b742c1739a205fe2ea2405cd8e7
print('\n Block Hash = ', hex(block_hash))

if block_hash <= target:
    print('block hash is less than target value. => Valid')
else:
    print('block hash is invalid.')