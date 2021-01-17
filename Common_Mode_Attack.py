'''
共模攻击的过程：
    如果在RSA的使用中使用了相同的模n对相同的明文m进行了加密，那么就可以在不分解n的情况下还原出明文m的值
    若两个加密指数互质，即gcd(e1,e2)=1, 那么存在s1与s2，使得
        e1*s1+e2*s2=1
    此式子可以用扩展欧几里得算法求得s1与s2，又因为
        c1 = m^e1 % n
        c2 = m^e2 % n
    所以
        (c1^s1 * c2^s2) % n = ((m^e1 % n)^s1 * (m^e2 % n)^s2) % n
    根据模运算性质，可以化简为
        (c1^s1 * c2^s2) % n = ((m^e1)^s1 * (m^e2)^s2) % n
        (c1^s1 * c2^s2) % n = (m^(e1^s1 + e2^s2)) % n
    又因为
        e1*s1 + e2*s2 = 1
    所以
        (c1^s1*c2^s2) % n = (m^(1)) % n
        (c1^s1*c2^s2) % n = m % n
'''
import random
from gmpy2 import invert    #模逆函数
from gmpy2 import gcdext    #扩展欧几里得算法

# 欧几里得算法求最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

# 快速进行幂运算
def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power&1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power>>1
    return result


# MillerRabin
def Miller_Rabin(n, iter_num):
    # 2是素数
    if n == 2:
        return True

    if n&1 == 0 or n<2:
        return False
    # n-1 = (2^s)m
    m,s = n - 1,0
    while m&1==0:
        m = m>>1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = fast_power(random.randint(2,n-1), m, n)
        if b==1 or b== n-1:
            continue
        for __ in range(s-1):
            b = fast_power(b, 2, n)
            if b == n-1:
                break
        else:
            return False
    return True


# 生成大的素数,将Miller进行k次，将合数当成素数处理的错误概率最多不会超过4^(-k)
def get_prime():
    Min = 10**152;Max = 10**154;p = 0
    while(1):
        p = random.randrange(Min, Max, 1)
        # 这里进行素数验证
        if Miller_Rabin(p, 20) == False:
                continue
        else:
                return p


# 选择符合要求的e
def choose_e1(OrLa, n):
    print('Choosing e1...')
    for e in range(2 ** 31, 2, -1):
        if gcd(e, OrLa) == 1 and gcd(e, n) == 1 :
            return e

def choose_e2(OrLa, n, e1):
    print('Choosing e2...')
    for e in range(2**31, 2, -1):
        if gcd(e, OrLa) == 1 and gcd(e, n) == 1 and gcd(e,e1) == 1 :
            return e


def convert_to_int(text):
    converted = []
    for i in text:
        converted.append(ord(i))
    return converted


def convert_to_ascii(text):
    converted = ''
    for i in text:
        converted = converted + chr(i)
    return converted


# 生成密钥
def get_key():
    # 随意选择两个大的质数p和q，p不等于q，计算N=pq
    p = get_prime()
    q = get_prime()
    N = p * q
    # 欧拉函数
    OrLa = (p - 1) * (q - 1)
    e1 = choose_e1(OrLa, N)
    e2 = choose_e2(OrLa, N, e1)
    return e1, e2, N

def Common_Mode_Attack(M):
    e1, e2, N, = get_key()  #生成公钥

    # M = input("请输入待加密明文：")
    M = convert_to_int(M)   #将输入ascii码转换为数字
    C1 = []
    C2 = []
    for number in M:
        C1.append(fast_power(number, e1, N))
        C2.append(fast_power(number, e2, N))
    #分别用e1和e2对同一段明文加密
    print('N:', N)
    print('C1:', ''.join(map(str, C1)))
    print('C2:', ''.join(map(str, C2)))
    print('e1:', e1)
    print('e2:', e2)
    print('开始计算使得e1*s1+e2*s2=1成立的s1与s2')
    s = gcdext(e1, e2)
    s1 = s[1]
    s2 = s[2]
    #扩展欧几里得算法，找出使e1*s1+e2*s2=1成立的s1和s2
    print('\n经过计算后')
    print('s1=', s1)
    print('s2=', s2)
    M1 = []
    if s1 < 0:
        t = s1
        s1 = -s1
        C11 = []
        for i in range(len(C1)):
            C11.append(invert(C1[i], N))    #invert()为求模逆的函数
            M1.append(pow(C11[i], s1, N) * pow(C2[i], s2, N) % N)
            print('由于s1<0，求得C1模N逆为', ''.join(map(str, C11)))
    elif s2 < 0:
        s2 = -s2
        C22 = []
        for i in range(len(C2)):
            C22.append(invert(C2[i], N))
            M1.append(pow(C1[i],s1,N) * pow(C22[i], s2, N) % N)
            print('由于s2<0，求得C2模N逆为', ''.join(map(str, C22)))
    #根据s1和s2的正负，判断是否对c1或c2进行模逆操作
    M2 = convert_to_ascii(M1)   #将得到的数字转变为ascii码
    print('攻击后得到原文：', M2)
    return e1, e2, t, s2, M2, N

if __name__ == "__main__":
    Common_Mode_Attack(0)