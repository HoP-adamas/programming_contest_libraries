# Union-Find tree

class UnionFind:
    def __init__(self, n):
        # 負  : 根であることを示す。絶対値は木の要素数
        # 非負: 根でないことを示す。値は親を示す
        self.table = [-1] * n
 
    def _root(self, x):
        stack = []
        tbl = self.table
        while tbl[x] >= 0:
            stack.append(x)
            x = tbl[x]
        for y in stack:
            tbl[y] = x
        return x
 
    def find(self, x, y):
        return self._root(x) == self._root(y)
 
    def union(self, x, y):
        r1 = self._root(x)
        r2 = self._root(y)
        if r1 == r2:
            return
        if self.table[r1] > self.table[r2]:
            r1, r2  = r2, r1
        self.table[r1] += self.table[r2]
        self.table[r2] = r1
      
    def size(self, x):
      return -self.table[self._root(x)]

def get_uft_size(uft):
  '''
  Union-Find tree の各木のノード数を取得する。
  返り値はdictでkeyは各木のルート、valueはそのルートの木のノード数
  '''
  counter = {}
  for i in range(len(uft.table)):
    if uft.table[i] < 0:
      try:
        counter[i] += 1
      except:
        counter[i] = 1

    else:
      try:
        counter[uft._root(i)] += 1
      except:
        counter[uft._root(i)] = 1

  return counter


class PotentialUnionFindTree:
	"""
	references
	- https://qiita.com/drken/items/cce6fc5c579051e64fab
	- https://atcoder.jp/contests/typical90/submissions/23535952
	"""
	def __init__(self, n, unit=0, inf=10**18):
		self.n = n
		self.parent = [-1]*n	# 正の値の時は親ノードを表す。負の時はrootであり、その絶対値はこのrootに属するノードの数（木のサイズ）を表す。
		self.pot = [unit]*n
		self.inf = inf

	def root(self, x):
		x0 = x
		s = 0
		while self.parent[x] >= 0:
			s += self.pot[x]
			x = self.parent[x]
		px = x
		x = x0
		while px != x:
			self.pot[x], s = s, s - self.pot[x]
			self.parent[x], x = px, self.parent[x]
		return px

	def dist(self, s, t):
		rs = self.root(s)
		rt = self.root(t)
		if rs == rt:
			return self.pot[t] - self.pot[s]
		return self.inf

	def union(self, a, b, d):
		ra, rb = self.root(a), self.root(b)
		if ra != rb:
			if self.parent[rb] >= self.parent[ra]:
				self.parent[ra] += self.parent[rb]
				self.pot[rb] = self.pot[a] + d - self.pot[b]
				self.parent[rb] = ra
			else:
				self.parent[rb] += self.parent[ra]
				self.pot[ra] = self.pot[b] - d - self.pot[a]
				self.parent[ra] = rb

	def size(self, a):
		return -self.parent[self.root(a)]

	def find(self, a, b):
		return self.root(a) == self.root(b)

	def groups(self):
		G = [[] for _ in range(self.n)]
		for i in range(self.n):
			G[self.root(i)].append(i)
		return [g for g in G if g]
