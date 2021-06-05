import math
'''
前処理ありの素因数分解
O(logN)
'''
def prime_fact(n):
    spf = [0]*(n+1)
    # calc spf
    for i in range(n+1):
        spf[i] = i
    for i in range(2,int(math.sqrt(n))+1):
        if spf[i] == i:
            for j  in range(i**2, n+1, i):
                if spf[j] == j:
                    spf[j] = i

    # do prime factrization
    factor = {}
    while (n != 1):
        try:
            factor[spf[n]] += 1
        except:
            factor[spf[n]] = 1
        n //= spf[n]
    
    return factor

def divisor(n):
    ret = []
    for i in range(1,int(math.sqrt(n))+1):
        if n % i == 0:
            ret.append(i)
            if i * i != n:
                ret.append(n // i)

    ret.sort()
    return ret

def divisor_num(n):
    factor = prime_fact(n)
    ret = 1
    for key, item in factor.items():
        ret *= item + 1
    return ret

