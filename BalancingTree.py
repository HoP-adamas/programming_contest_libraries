class BalancingTree:
    """
    回転を使わない平衡2分木
    https://qiita.com/Kiri8128/items/6256f8559f0026485d90
    """

    def __init__(self, n):
        self.N = n
        self.root = self.node(1<<n, 1<<n)
    
    def append(self, v):
        v += 1
        nd =self.root
        while True:
            if v == nd.value:
                # 既に存在しているとき。何か処理をする場合はここに書く。
                return 0
            mi, ma = min(v, nd.value), max(v, nd.value)
            if mi < nd.pivot:
                nd.value = ma
                if nd.left:
                    nd = nd.left
                    v = mi
                else:
                    p = nd.pivot
                    nd.left = self.node(mi, p - (p&-p)//2)
                    break
            else:
                nd.value = mi
                if nd.right:
                    nd = nd.right
                    v = ma
                else:
                    p = nd.pivot
                    nd.right = self.node(ma, p + (p&-p)//2)
                    break
    def leftmost(self, nd):
        if nd.left:
            return self.reftmost(nd.left)
        return nd
    def rightmost(self, nd):
        if nd.right:
            return self.rightmost(nd.right)
        return nd
    
    def lower_bound(self, v):
        # vより真に小さいやつの中での最大値（なければ-1）
        v += 1
        nd = self.root
        prev = 0
        if nd.value < v:
            prev = nd.value

        while True:
            if v <= nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return prev - 1
            else:
                prev = nd.value
                if nd.right:
                    nd = nd.right
                else:
                    return prev - 1
    
    def upper_bound(self, v):
        # vより真に大きいやつの中での最小値（なければRoot）
        v += 1
        nd = self.root
        prev = 0
        if nd.value > v:
            prev = nd.value
        while True:
            if v < nd.value:
                prev = nd.value
                if nd.left:
                    nd = nd.left
                else:
                    return prev - 1
            else:
                if nd.right:
                    nd = nd.right
                else:
                    return prev - 1
    @property
    def max(self):
        return self.lower_bound((1<<self.N)-1)
    @property
    def min(self):
        return self.upper_bound(-1)

    def delete(self, v, nd = None, prev = None):
        # 値がvのノードがあれば削除（なければ何もしない）
        v += 1
        if not nd:
            nd = self.root
        if not prev:
            prev = nd

        while v != nd.value:
            prev = nd
            if v <= nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return
            else:
                if nd.right:
                    nd = nd.right
                else:
                    return
        
        if (not nd.left) and (not nd.right):
            if not prev.left:
                prev.right = None
            elif not prev.right:
                prev.left = None
            else:
                if nd.pivot == prev.left.pivot:
                    prev.left = None
                else:
                    prev.right = None

        elif nd.right:
            nd.value = self.leftmost(nd.right).value
            self.delete(nd.value - 1, nd.right, nd)
        else:
            nd.value = self.rightmost(nd.left).value
            self.delete(nd.value - 1, nd.left, nd)

    def __contains__(self, v: int) -> bool:
        return self.upper_bound(v - 1) == v


        






    class node:
        def __init__(self, v, p):
            self.value = v
            self.pivot = p
            self.left = None
            self.right = None