# 타원 곡선암호의 순환군 찾기
import math
import numpy as np
import matplotlib.pyplot as plt

def add_operation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p
    
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    
    if p == q:
        # Doubling
        # slope (s) = (3 * x1 ^ 2 + a) / (2 * y1) mod m
        # 분모의 역원부터 계산한다 (by Fermat's Little Theorem)
        r = 2 * y1
        rInv = pow(r, m-2, m)   # Fermat's Little Theorem
        s = (rInv * (3 * (x1 ** 2) + a)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m-2, m)   # Fermat's Little Theorem
        s = (rInv * (y2 - y1)) % m
    x3 = (s ** 2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3

# y^2 = x^3 + 2 * x + 2 mod 127
a = 2; b = 2; m = 127; P = (5,1); Q = P

all_points = [P]
while (1):
    if (Q[0] == P[0]) & (abs(Q[1] - m) == P[1]):
        break
    else:
        R = add_operation(a, b, P, Q, m)
        all_points.append(R)
        Q = R

x, y = np.array(all_points).T
plt.figure(figsize=(8, 6))
plt.scatter(x, y, marker='o', color='green', alpha=0.5, s=150)
plt.show()
print(all_points)