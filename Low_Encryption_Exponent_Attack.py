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
    Min = 10**2;Max = 10**3;p = 0
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
    return ''.join(map(str, entext))

# 基于低指数攻击的中国剩余定理
def LEA_CRT(n1,n2,n3,c1,c2,c3):
    #print(c1,c2,c3)
    N=n1*n2*n3
    m1=n2*n3
    m2=n1*n3
    m3=n1*n2
    e1 = modular_inverse(m1 ,n1)
    e2 = modular_inverse(m2, n2)
    e3 = modular_inverse(m3, n3)
    re = e1*c1*m1+e2*c2*m2+e3*c3*m3
    return re%N

#开立方，精确到个位
def cube_root(n):
    if(n<0):
        temp=-n
    else: temp=n
    precision=0.1
    low=0
    high= temp/2
    last_high=0
    while(abs(high-last_high)>1 or abs(high*high*high-temp)>precision):
        last_high=high
        if(high*high*high>temp):
            high=high-(high-low)/2
        elif(high*high*high<temp):
            x=high+(high-low)/2
            low=high
            high=x
        else:
            break
        #print(high)
    re=high
    if (n<0):
        re=-high
    return (int(round(re)))

#低指数攻击
def Low_Exponent_Attack(message):
    count=0
    n=[0,0,0]
    #挑三个符合要求的大整数n0,n1,n2
    while(1):
        if count==3:
            break
        p = get_prime()
        q = get_prime()
        N = p * q
        # 欧拉函数
        OrLa = (p - 1) * (q - 1)
        if OrLa%3==0:
            continue
        else:
            n[count]=N
            print('选取大整数n:',n[count])
            count=count+1
    #低指数攻击实验直接令e=3
    e=3
    #令铭文是m计算用3个不同n和相同公钥e=3得出的密文c1,c2,c3
    #message = input("请输入待加密的明文：")
    message= convert_to_int(message)  # 将输入ascii码转换为数字
    print("message=",message)
    C1 = []
    for number in message:
        C1.append(fast_power(number, e, n[0]))
    print('C1:', ''.join(map(str, C1)))
    C2=[]
    for number in message:
        C2.append(fast_power(number, e, n[1]))
    print('C2:', ''.join(map(str, C2)))
    C3=[]
    for number in message:
        C3.append(fast_power(number, e, n[2]))
    print('C3:', ''.join(map(str, C3)))
    #中国剩余定理求得m的立方
    M_3 = []
    for index in range(len(message)):
        M_3.append(LEA_CRT(n[0], n[1], n[2], C1[index], C2[index], C3[index]))
    print("M_3=",M_3)
    #m_3开立方得出m_1与最初得m进行对比即可验证低指数攻击
    M_1=[]
    for number in M_3:
        M_1.append(cube_root(number))
    print("M_1=", M_1)
    #m_1=m_3**(1/e)
    M_1 = convert_to_ascii(M_1)  # 将得到的数字转变为ascii码
    print('攻击后得到原文：', M_1)
    return n[0], n[1], n[2], C1, C2, C3, M_1

if __name__ == "__main__":
    Low_Exponent_Attack()

