'''
低解密指数攻击
'''
import random
def rational_to_contfrac(x, y): #有理数转换为连分数
    a = x // y
    if a * y == x:
        return [a]
    else:
        pquotients = rational_to_contfrac(y, x - a * y)
        pquotients.insert(0, a)
        return pquotients


def convergents_from_contfrac(frac):    #渐进分数
    convs = [];
    for i in range(len(frac)):
        convs.append(contfrac_to_rational(frac[0:i]))
    return convs


def contfrac_to_rational(frac): #连分数转为有理数
    if len(frac) == 0:
        return (0, 1)
    elif len(frac) == 1:
        return (frac[0], 1)
    else:
        remainder = frac[1:len(frac)]
        (num, denom) = contfrac_to_rational(remainder)
        return (frac[0] * num + denom, num)

def egcd(a, b): #扩展欧几里得算法
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def modInverse(e, n):   #计算模逆
    return egcd(e, n)[0] % n

def bitlength(x):   #计算位长
    assert x >= 0
    n = 0
    while x > 0:
        n = n + 1
        x = x >> 1
    return n


def isqrt(n):   #计算平方根
    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n):   #判断是否能进行开方
    h = n & 0xF

    if h > 9:
        return -1

    if (h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8):
        t = isqrt(n)
        if t * t == n:
            return t
        else:
            return -1

    return -1


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


def miller_rabin_pass(a, s, d, n):
    a_to_power = pow(a, d, n)
    i = 0

    if a_to_power == 1:
        return True

    while (i < s - 1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
        i += 1

    return a_to_power == n - 1

# MillerRabin，素数性检验
def Miller_Rabin(n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    # 进行K次
    K = 20

    i = 1
    while (i <= K):
        # 1 < a < n-1
        a = random.randrange(2, n - 1)
        if not miller_rabin_pass(a, s, d, n):
            return False
        i += 1

    return True

def gen_prime(nbits):
	while True:
		p = random.getrandbits(nbits)
		#force p to have nbits and be odd
		p |= 2**nbits | 1
		if Miller_Rabin(p):
			return p
			break

def gen_prime_range(start, stop):
	while True:
		p = random.randrange(start,stop-1)
		p |= 1
		if Miller_Rabin(p):
			return p
			break

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


def getPrimePair(bits=512): #判断是否满足条件 p<q<2p

    assert bits % 4 == 0

    p = gen_prime(bits)
    q = gen_prime_range(p + 1, 2 * p)

    return p, q

def generateKeys(nbits=1024):
    assert nbits % 4 == 0

    p, q = getPrimePair(nbits // 2)
    n = p * q
    phi = (p-1)*(q-1)

    # generate a d such that:
    #     (d,n) = 1
    #    36d^4 < n
    good_d = False
    while not good_d:
        d = random.getrandbits(nbits // 4)
        if (gcd(d, phi) == 1 and 36 * pow(d, 4) < n):
            good_d = True

    e = modInverse(d, phi)
    return e, n, d

# RSA算法的加密运算
def RSA_Encrypt(M, N, e):
    entext = []
    #M = input("请输入待加密的明文：")
    if M == "":
        print('No PlainText')
    else:
        converted = convert_to_int(M)
        for number in converted:
            entext.append(fast_power(number, e, N))
        print('密文: ', ''.join(map(str, entext)))
    return entext


# RSA算法的解密运算
def RSA_Decrypt(C, N, d):
    detext = []
    for number in C:
        detext.append(fast_power(number, d, N))
    decrypted = convert_to_ascii(detext)
    print('利用攻击得到的秘钥解密得到明文: ', decrypted)
    return decrypted

def hack_RSA(e, n, C):
    frac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(frac)

    for (k, d) in convergents:
        # check if d is actually the key
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s * s - 4 * n
            if (discr >= 0):
                t = is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("\n攻击后得到私钥, d=", d)
                    RSA_Decrypt(C, n, d)
                    return d

if __name__ == "__main__":
    e, N, d= generateKeys() # 生成公钥、私钥 长度为1024位：(N,e)是公钥，(N,d)是私钥。
    print('e = ', e)
    print('N = ', N)
    print('d = ', d)
    C = []
    C = RSA_Encrypt(N, e)

    hack_RSA(e,N,C)

