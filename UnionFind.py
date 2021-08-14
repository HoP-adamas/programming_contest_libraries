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