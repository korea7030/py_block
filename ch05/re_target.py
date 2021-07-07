from datetime import datetime

# 압축형 타깃을 일반형으로 변환
def uncompact(bits):
    # bit의 왼쪽 1bytes(exponents)를 추출
    exponents = bits >> 24

    # bits의 오른쪽 3bytes(coefficient)를 추출
    coefficient = bits & 0x007fffff

    # target value 계산
    target = coefficient << 8 * (exponents - 3)
    return target

# 일반형 타깃을 압축형으로 변환
def compact(target):
    # target의 길이
    n_len = target.bit_length()

    # compact format 변환
    n_len = ((n_len + 7) & ~0x7)
    exponents = (int(n_len/8) & 0xff)
    coefficient = (target >> (n_len - 24)) & 0xfffff

    if coefficient & 0x800000:
        coefficient >>= 8
        exponents += 1
    return (exponents << 24) | coefficient

n_pow_target_timespan = 14 * 24 * 60 * 60 # 2weeks(초)
pow_limit = '00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

# 블록 520128의 target value를 결정 (re_target)
# 이전 520127블록과 2016 이전 블록을 참조해 계산
if 520128 % 2016 == 0:
    # 블록 520127의 target value와 timestamp를 읽음
    old_target = 0x1749500d
    old_target = uncompact(old_target)
    current_timestamp = 0x5ae305b6

    # 2016 이전 블록 (520127 - 2016 + 1 = 518112)의 timestamp 
    prev_timestamp = 0x5ad16764

    # 2016블록이 생성된 시간 측정(초 단위)
    n_actual_timespan = current_timestamp - prev_timestamp

    # 크게 변동하는 것을 방지하기 위해,
    # 0.5 weeks보다 작으면 0.5 weeks로, 8 weeks보다 크면 8weeks로 조정
    if n_actual_timespan < n_pow_target_timespan / 4:
        n_actual_timespan = n_pow_target_timespan / 4
    if n_actual_timespan > n_pow_target_timespan * 4:
        n_actual_timespan = n_pow_target_timespan * 4

    # retarget value를 계산
    new_target = old_target * (n_actual_timespan / n_pow_target_timespan)

    # 난이도 상한선 조정
    if new_target > int(pow_limit, 16):
        new_target = int(pow_limit, 16)

    new_target = round(new_target)
    new_target = compact(new_target)

    # 결과출력
    print("\n블록 518112 생성 시각 =", datetime.utcfromtimestamp(prev_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    print("블록 520127 생성 시각 =", datetime.utcfromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    print("2016 블록 생성에 걸린 시간 = %.2f (분)" % (n_actual_timespan / 60))
    print("1 블록 생성에 걸린 평균 시간 = %.2f (분)" % (n_actual_timespan / 60 / 2016))
    print("현재 Target bits =", hex(compact(old_target)))
    print("블록 520128에 적용할 새로운 Target bits =", hex(new_target))
else:
    # 아직 target을 바꿀때가 아님. 520127의 target을 유지
    new_target = 0x1749500d