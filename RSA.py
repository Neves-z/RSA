'''
RSA的过程：
1. 随意选择两个大的质数p和q，p不等于q，计算N=pq。
2. 根据欧拉函数，不大于N且与N互质的整数個数為(p-1)(q-1)。
3. 选择一个整数e与(p-1)(q-1)互质，并且e小于(p-1)(q-1)。
4. 用以下这个公式计算d：d× e ≡ 1 (mod (p-1)(q-1))。
5. 将p和q的记录销毁。

(N,e)是公钥，(N,d)是私钥。
'''
import random
import time


# 欧几里得算法求最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# 用拓展的欧几里得算法求模逆
def modular_inverse(a, m):
    m0 = m
    y = 0
    x = 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0

    return x


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
def choose_e(OrLa, n):
    print('Choosing e...')
    for e in range(2 ** 31, 2, -1):
        if gcd(e, OrLa) == 1 and gcd(e, n) == 1:
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
    e = choose_e(OrLa, N)
    d = modular_inverse(e, OrLa)
    print('私钥p,q,d分别为:')
    print('p: %d' % p)
    print('q: %d' % q)
    print('d: %d\n' % d)

    print('公钥n,e分别为:')
    print('n: %d' % N)
    print('e: %d\n' % e)
    return e, d, N, p, q


# RSA算法的加密运算
def RSA_Encrypt(message, N, e):
    entext = []
    # M = input("请输入待加密的明文：")
    print('Plaintext: ', message)
    if message == "":
        print('No Message')
    else:
        converted = convert_to_int(message)
        for number in converted:
            entext.append(fast_power(number, e, N))
        print('Encrypted text: ', ''.join(map(str, entext)))
    return entext


# RSA算法的解密运算
def RSA_Decrypt(C, N, d):
    detext = []
    time_start = time.time()
    for number in C:
        detext.append(fast_power(number, d, N))
    decrypted = convert_to_ascii(detext)
    print("_______RSA____________")
    print('Decrypted text: ', decrypted)
    time_finish = time.time()
    run_time = time_finish - time_start
    print('Time for classic decryption: ', run_time)
    return decrypted, run_time


# 中国剩余定理
def CRT(p, q, dP, dQ, c):
    qInv = modular_inverse(q, p)
    m1 = pow(c, dP, p)
    m2 = pow(c, dQ, q)
    h = (qInv * (m1 - m2)) % p
    m = m2 + h * q
    return m


# RSA算法采用中国剩余定理改进后的解密运算
def RSA_CRT(C, p, q, d):
    time_start = time.time()
    dp = d % (p - 1)
    dq = d % (q - 1)
    M = ''
    for i in C:
        M = M + chr(CRT(p, q, dp, dq, i))
    print("_______RSA_CRT____________")
    print('Decrypted using TCR: ', M)
    time_finish = time.time()
    run_time = time_finish - time_start
    print('Time for CRT decryption: ', run_time)
    return M, run_time


if __name__ == "__main__":
    e, d, N, p, q = get_key()  # 生成公钥、私钥 长度为1024位：(N,e)是公钥，(N,d)是私钥。
    C = []

    '''加密过程'''
    C = RSA_Encrypt(N, e)  # RSA通过公钥（N, e)进行加密
    '''解密过程'''
    RSA_Decrypt(C, N, d)  # RSA通过私钥（N, d)对上诉密文进行解密
    RSA_CRT(C, p, q, d)
