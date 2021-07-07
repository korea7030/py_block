from bitarray import bitarray
import math
import random
import mmh3

# bloom filter의 최적의 파라미터
# n = number of elements
# prob = Desired False positive probability
def opt_parameter(n, prob):
    m = -n * math.log(prob) / (math.log(2) ** 2)
    k = math.ceil(m * math.log(2) / n)
    return k, math.ceil(m)

# element를 Bloom filter에 등록한다
def add(BloomFilter, element, k, m):
    for i in range(k):
        index = mmh3.hash(element, i) % m
        BloomFilter[index] = 1

# element가 Bloom filter에 있는지 확인한다
def contain(BloomFilter, element, k, m):
    for i in range(k):
        index = mmh3.hash(element, i) % m
        if BloomFilter[index] == 0:
            # 한 비트라도 0 (False)이면 "없음"
            return 0
        
    # 모두 1 이면 "있을 가능성이 있음"
    return 1

def bloom_filter(prob=0.1, n_try=10000):
    set_a = random.sample(range(1, 10000), 100)

    k, m = opt_parameter(len(set_a), prob=prob)
    bloom_filter = bitarray(m)
    bloom_filter[:] = 0 # 0으로 초기화

    for element in set_a:
        add(bloom_filter, str(element), k, m)
    
    pred_cnt = 0
    act_cnt = 0

    for i in range(n_try):
        # 1 ~ 10,000 사이의 난수 1개를 만든다
        r = random.randrange(1,10000)
        
        # r이 집합 A에 있는지 확인한다
        result = contain(bloom_filter, str(r), k, m)
        if result == 1:
            # 있을 가능성이 있다는 카운터
            pred_cnt += 1
            
            # 실제 확인한 카운터
            for e in set_a:
                if r == e:
                    act_cnt += 1
                    break

    print("\nDesired FP rate = ", prob)
    print("Number of element (n) = ", len(set_a))
    print("Number of hash functions (k) = ", k)
    print("Number of Bloom filter bit (m) = ", m)
    print("Actual FP rate (p) = ", (pred_cnt - act_cnt) / n_try)

if __name__ == '__main__':
    bloom_filter(prob = 0.1)