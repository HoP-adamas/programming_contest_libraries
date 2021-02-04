def cmb(n, r, mod):
	'''
	modありで組み合わせの総数を計算する。
	ただし、modが素数以外の時は使用できない。
	'''
	g1 = [1, 1] # 元テーブル
	g2 = [1, 1] #逆元テーブル
	inverse = [0, 1] #逆元テーブル計算用テーブル
	for i in range( 2, n + 1 ):
		g1.append( ( g1[-1] * i ) % mod )
		inverse.append( ( -inverse[mod % i] * (mod//i) ) % mod )
		g2.append( (g2[-1] * inverse[-1]) % mod )
    
	if ( r<0 or r>n ):
		return 0
	r = min(r, n-r)
	return g1[n] * g2[r] * g2[n-r] % mod

from functools import reduce
def cmb2(n, r, MOD=10**9+7):
    if not 0 <= r <= n: return 0
    r = min(r, n - r)
    numerator = reduce(lambda x, y: x * y % MOD, range(n, n - r, -1), 1)
    denominator = reduce(lambda x, y: x * y % MOD, range(1, r + 1), 1)
    return numerator * pow(denominator, MOD - 2, MOD) % MOD

class Combination:
	def __init__(self, n_max, mod = 10**9+7):
		self.mod = mod
		f = 1
		self.fac = fac = [f]
		for i in range(1, n_max+1):
			f = f * i %mod
			fac.append(f)
		f = pow(f, mod-2, mod)

		self.facinv = facinv = [f]
		for i in range(n_max, 0, -1):
			f = f * i % mod
			facinv.append(f)
		facinv.reverse()

	def __call__(self, n, r):
		if not 0 <= r <= n:
			return 0
		return self.fac[n] * self.facinv[r] % self.mod * self.facinv[n-r] % self.mod

