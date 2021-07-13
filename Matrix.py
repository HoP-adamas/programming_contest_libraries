
from Vector import Vector

class Matrix:
    def __init__(self, A):
        self.nrow = len(A)
        self.ncol = len(A[0])
        self._matrix = A

    def __getitem__(self, item):
        if type(item) == tuple:
            return self._matrix[item[0]][item[1]]
        else:
            return self._matrix[item]
    def __setitem__(self, item, val):
        i, j = item
        self._matrix[i][j] = val

    def __add__(self, B):
        C = [[0] * self.ncol for _ in range(self.nrow)]
        for i in range(self.nrow):
            for j in range(self.ncol):
                C[i][j] = self._matrix[i][j] + B._matrix[i][j]
        return Matrix(C)

    def __sub__(self, B):
        C = [[0] * self.ncol for _ in range(self.nrow)]
        for i in range(self.nrow):
            for j in range(self.ncol):
                C[i][j] = self._matrix[i][j] - B._matrix[i][j]
        return Matrix(C)

    def __mul__(self, other):
        h, w, A = self.nrow, self.ncol, self._matrix
        if type(other) == int:
            C = [[other * A[i][j] for j in range(w)] for i in range(h)]
            return Matrix(C)
        elif type(other) == Vector:
            v = other
            assert len(v) == w, "The columm size of matrix and that of vector are different"
            ret = [0] * w
            for i in range(h):
                for j in range(w):
                    ret[i] = ret[i] + A[i][j] * v[j]
            return Vector(ret)
            
        else:
            assert self.ncol == other.nrow, "sizes of matrices are different"
            C = [[0]*other.ncol for _ in range(self.nrow)]
            for i in range(h):
                for j in range(other.ncol):
                    tmp = 0
                    for k in range(w):
                        tmp += A[i][k] * other._matrix[k][j]
                    C[i][j] = tmp
            return Matrix(C)

    def __floordiv__(self,c):
        h, w, A=self.nrow,self.ncol,self._matrix
        res=A.copy()
        for i in range(h):
            for j in range(w):
                res[i][j]=res[i][j]//c
        return Matrix(res)

    def __mod__(self, c):
        h, w, A=self.nrow,self.ncol,self._matrix
        res=A.copy()
        for i in range(h):
            for j in range(w):
                res[i][j]=res[i][j]%c
        return Matrix(res)

    def __pow__(self, m):
        h, w, A = self.nrow, self.ncol, self._matrix
        assert h == w, "This matrix does not a square matrix"
        if m == 0:
            mask = 1<<32 - 1
            return Matrix([[int(i==j)*mask for i in range(h)] for j in range(h)])
        else:
            m -= 1
            res = self
            while m:
                if m % 2 == 1:
                    res = res * self
                self = self * self
                m >>= 1
        return res
