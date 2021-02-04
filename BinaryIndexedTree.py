class BIT:
    def __init__(self, n):
        self.num_element = n+1 # 数列の要素数+1 = 配列の要素数
        self.bit = [0]*(n+1) # 1-indexed

    def add(self, i, x):
        idx = i
        while idx < self.num_element:
            self.bit[idx] += x
            idx += idx & (-idx)
    
    def sum(self,i):
        res = 0
        idx = i
        while idx > 0:
            res += self.bit[idx]
            idx += idx & (-idx)
        return res

class BIT2D:
    def __init__(self, h, w):
        self.height = h + 1
        self.width = w + 1
        self.bit = [[0]*self.width for _ in range(self.height)]

    def add(self, h, w, x):
        idx_h = h
        idx_w = w
        while idx_h < self.height:
            while idx_w < self.width:
                self.bit[idx_h][idx_w] += x
                idx_w += idx_w & (-idx_w)
            idx_h += idx_h & (-idx_h)
    
    def sum(self, h, w):
        res = 0
        idx_h = h
        idx_w = w
        while idx_h < self.height:
            while idx_w < self.width:
                res += self.bit[idx_h][idx_w]
                idx_w += idx_w & (-idx_w)
            idx_h += idx_h & (-idx_h)
        
        return res

    def query(self, h1, w1, h2, w2):
        return self.sum(h2 - 1, w2 - 1) - self.sum(h2 - 1, w1 - 1) - self.sum(h1 - 1, w2 - 1) + self.sum(h1 - 1, w1 - 1) 