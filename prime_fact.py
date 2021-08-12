import math
from collections import defaultdict
'''
前処理ありの素因数分解
init; O(NloglogN)
O(logN)
'''
def prime_fact_spf(n):
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
    factor = prime_fact_spf(n)
    ret = 1
    for key, item in factor.items():
        ret *= item + 1
    return ret


def prime_fact(n):
    '''
    O(n**(1/2))
    '''
    ret = defaultdict(int)
    i = 2
    while i**2 <= n:
        if n % i != 0:
            i+=1
            continue
        tmp = 0
        while n % i == 0:
            tmp += 1
            n //= i
        ret[i] = tmp
        i += 1
    if n != 1:
        ret[n] = 1
    return ret
