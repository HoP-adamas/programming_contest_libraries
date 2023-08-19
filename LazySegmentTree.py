class LazySegmentTree():

	def __init__(self, n, f, g, merge, ef, eh):
		self.n = n
		self.f = f  # 二項演算
		self.g = lambda xh, x: g(xh, x) if xh != eh else x
		self.merge = merge
		self.ef = ef
		self.eh = eh
		l = (self.n - 1).bit_length()
		self.size = 1 << l  # 2^Nの形に変えてる。ただし、n = 2^Nの形じゃなくても同じコードで正しく動作する。参考）https://maspypy.com/segment-tree-%e3%81%ae%e3%81%8a%e5%8b%89%e5%bc%b71
		self.tree = [self.ef] * (self.size << 1)
		self.lazy = [self.ef] * (self.size << 1)
		self.plt_cnt = 0

	def build(self, array):
		for i in range(self.n):
			self.tree[self.size + i] = array[i]
		for i in range(self.size - 1, 0, -1):
			self.tree[i] = self.f(self.tree[i << 1], self.tree[(i << 1)| 1])

	def replace(self, i, x):
		"""
		一点更新
		tree[i]をxで更新
		"""
		i += self.size
		self.propagate_lazy(i)
		self.tree[i] = x
		self.lazy[i] = self.eh
		self.propagate_tree(i)

	def get(self, i):
		i += self.size
		self.propagate_lazy(i)
		return self.g(self.lazy[i], self.tree[i])

	def update_range(self, l, r, x):
		"""
		[l, r)(o-indexed) の　要素aに対してop(x, a)を作用させる
		"""
		l += self.size
		r += self.size
		l0 = l // (l & -l)
		r0 = r // (r & -r)
		self.propagate_lazy(l0)
		self.propagate_lazy(r0 - 1)
		while l < r:
			if r & 1:
				r -= 1
				self.lazy[r] = self.merge(x, self.lazy[r])
			if l & 1:
				self.lazy[l] = self.merge(x, self.lazy[l])
				l += 1
			l >>= 1
			r >>= 1
		self.propagate_lazy(l0)
		self.propagate_tree(r0 - 1)

	def update_range_right_half(self, l, x):

		if l == 0:
			self.update_all(x)
			return
		l += self.size
		l0 = l // (l & -l)
		self.propagate_lazy(l0)
		while l > 1:
			if l % 1:
				self.lazy[l] = self.merge(x, self.lazy[l])
				l += 1
			l >>= 1
		self.propagate_tree(l0)

	def update_range_left_half(self, r, x):
		if r == self.n:
			self.update_all(x)
			return
		r += self.size
		r0 = r // (r & -r)
		self.propagate_lazy(r0 - 1)
		while r > 1:
			if r & 1:
				r -= 1
				self.lazy[r] = self.merge(x, self.lazy[r])
			r >>= 1
		self.propagate_tree(r0 - 1)

	def update_all(self, x):
		self.lazy[1] = self.merge(x, self.lazy[1])

	def get_range(self, l, r):
		"""
		区間[l, r)から値を取得
		"""
		l += self.size
		r += self.size
		self.propagate_lazy(l // (l & -l))
		self.propagate_lazy(r // (r & -r) - 1)
		res_l = res_r = self.ef
		while l < r:
			if l & 1:
				res_l = self.f(res_l, self.g(self.lazy[l], self.tree[l]))
				l += 1
			if r & 1:
				r -= 1
				res_r = self.f(self.g(self.lazy[r], self.tree[r]), res_r)
			l >>= 1
			r >>= 1
		return self.f(res_l, res_r)

	def get_range_left_half(self, r):
		if r == self.n:
			return self.get_all()
		r += self.size
		self.propagate_lazy(r // (r& -r) - 1)
		res_l = res_r = self.ef
		while  r > 1:
			if r & 1:
				r -= 1
				res_r = self.f(self.g(self.lazy[r], self.tree[r]), res_r)
			r >>= 1
		return self.f(res_l, res_r)

	def get_rage_right_half(self, l):
		if l == 0:
			return self.get_all()
		l += self.size
		self.propagate_lazy(l // (l & -l))
		res_l = res_r = self.ef
		while l > 1:
			res_r = self.f(res_l, self.g(self.lazy[l], self.tree[l]))
			l >>= 1
		return self.f(res_l, res_r)

	def get_all(self):
		return self.g(self.lazy[1], self.tree[1])

	def max_right(self,l,func):
		"""
		return r such that
			・r = l or f(op(a[l], a[l + 1], ..., a[r - 1])) = true
			・r = n or f(op(a[l], a[l + 1], ..., a[r])) = false
		"""
		if l >= self.n: return self.n
		l += self.size
		s = self.ef
		while 1:
			while l % 2 == 0:
				l >>= 1
			if not func(self.f(s, self.g(self.lazy[l], self.tree[l]))):
				while l < self.size:
					l<<=1
					if func(self.f(s, self.g(self.lazy[l], self.tree[l]))):
						s = self.f(s, self.g(self.lazy[l], self.tree[l]))
						l += 1
				return l - self.size
			s = self.f(s, self.g(self.lazy[l], self.tree[l]))
			l += 1
			if l & -l == l: break
		return self.n
 
	def min_left(self,r,func):
		"""
		return l such that
			・l = r or f(op(a[l], a[l + 1], ..., a[r - 1])) = true
			・l = 0 or f(op(a[l - 1], a[l], ..., a[r - 1])) = false
		"""
		if r <= 0: return 0
		r += self.size
		s = self.ef
		while 1:
			r -= 1
			while r > 1 and r % 2:
				r >>= 1
			if not func(self.f(self.g(self.lazy[r], self.tree[r]), s)):
				while r < self.size:
					r = (r << 1) | 1
					if func(self.f(self.g(self.lazy[r], self.tree[r]), s)):
						s = self.f(self.g(self.lazy[r], self.tree[r]), s)
						r -= 1
				return r + 1 - self.size
			s = self.f(self.g(self.lazy[r], self.tree[r]), s)
			if r & -r == r: break
		return 0
 
	def propagate_lazy(self, i):
		for k in range(i.bit_length() - 1, 0, -1):
			x = i >> k
			laz = self.lazy[x]
			if laz == self.eh:
				continue
			self.lazy[(x << 1) | 1] = self.merge(laz, self.lazy[(x << 1) | 1])
			self.lazy[x << 1] = self.merge(laz, self.lazy[x << 1])
			self.tree[x] = self.g(laz, self.tree[x])
			self.lazy[x] = self.eh

	def propagate_tree(self, i):
		for _ in range(1, i.bit_length()):
			i >>= 1
			self.tree[i] = self.f(self.g(self.lazy[i << 1], self.tree[i << 1]), self.g(self.lazy[(i << 1) | 1], self.tree[(i << 1) | 1]))

	def __getitem__(self, i):
		if i < 0:
			i = self.n + i
		return self.get(i)

	def __setitem__(self, i, value):
		if i < 0:
			i = self.n + i
		self.replace(i, value)

	def __iter__(self):
		for x in range(1, self.size):
			if self.lazy[x] == self.eh:
				continue
			self.lazy[(x << 1) | 1] = self.merge(self.lazy[x], self.lazy[(x << 1) | 1])
			self.lazy[x << 1] = self.merge(self.lazy[x], self.lazy[x << 1])
			self.tree[x] = self.g(self.lazy[x], self.tree[x])
			self.lazy[x] = self.eh
		for xh, x in zip(self.lazy[self.size : self.size + self.n], self.tree[self.size : self.size + self.n]):
			yield self.g(xh, x)

	def __str__(self):
		return str(list(self))


####### example ########################################################


####### 更新:加算 取得:min ########################################################
# # get chain rule
# def f(x,y):
#	 return x if x < y else y
# ef = 10**18
 
# # merge of update
# def merge(a,b):
#	 return a + b
# eh = 0
 
# # update chain rule
# def g(a,x):
#	 return a + x
 
# st = LazySegmentTree(N, f, g, merge, ef, eh)
################################################################################

####### 更新:代入 取得:min ########################################################
# # get chain rule
# def f(x,y):
#	 return x if x < y else y
# ef = 10**18
 
# # merge of update
# def merge(a,b):
#	 return a if a != eh else b
# eh = -float("inf")
 
# # update chain rule
# def g(a,x):
#	 return a
 
# st = LazySegmentTree(N, f, g, merge, ef, eh)
################################################################################

####### 更新:min 取得:min ########################################################
# # get chain rule
# def f(x,y):
#	 return x if x < y else y
# ef = 10**18
 
# # merge of update
# def merge(a,b):
#	 return a if a < b else b
# eh = 10**18
 
# # update chain rule
# def g(a,x):
#	 return a if a < x else x
 
# st = LazySegmentTree(N, f, g, merge, ef, eh)
################################################################################

###### 更新:代入 取得:加算 ########################################################
# off=10**7
# # get chain rule
# def f(x,y):
#	 x0, x1 = divmod(x,off)
#	 y0, y1 = divmod(y,off)
#	 z0 = x0+y0
#	 z1 = x1+y1
#	 return z0*off + z1
# ef = 0
 
# # merge of update
# def merge(a,b):
#	 return a if a!=eh else b
# eh = -1
 
# # update chain rule
# def g(a,x):
#	 x0, x1 = divmod(x,off)
#	 return a*x1*off + x1
 
# st = LazySegmentTree(N, f, g, merge, ef, eh)
# st.build([1]*N)
 
# # (how to get)
# # res, _ = divmod(st.get_range(l, r), off)
################################################################################

