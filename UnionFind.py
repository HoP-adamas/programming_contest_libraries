# Union-Find tree

class UnionFind:
    def __init__(self, n):
        # 負  : 根であることを示す。絶対値はランクを示す
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
        # ランクの取得
        d1 = self.table[r1]
        d2 = self.table[r2]
        if d1 <= d2:
            self.table[r2] = r1
            if d1 == d2:
                self.table[r1] -= 1
        else:
            self.table[r1] = r2

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