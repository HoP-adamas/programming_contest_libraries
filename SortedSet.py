"""
reference
https://github.com/tatyam-prime/SortedSet
"""
from bisect import bisect_left, bisect_right, insort
import math

class SortedSet:
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None):
        if a is None:
            a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [a[size*i//bucket_size : size*(i+1)//bucket_size] for i in range(bucket_size)]

    def __init__(self, a=[]):
        a = list(a)
        if not all(a[i] < a[i+1] for i in range(len(a)-1)):
            a = sorted(set(a))
        self._build(a)

    def __iter__(self):
        for i in self.a:
            for j in i:
                yield j
    
    def __reversed__(self):
        for i in reversed(self.a):
            for j in reversed(i):
                yield j

    def __len__(self):
        return self.size

    def __repr__(self):
        return "SortedSet" + str(self.a)

    def __str__(self):
        s = str(list(self))
        return "{" + s[1:len(s)-1] + "}"

    def _find_bucket(self, x):
        # Find the bucket which should contain x. self must not be empty.
        for a in self.a:
            if x <= a[-1]:
                return a
        return a

    def __contains__(self, x):
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x

    def add(self, x):
        # Add an element and return True if added. O(√N)
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return False
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
            return True

    def discard(self, x):
        # Remove an element and return True if removed. O(√N)
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x:
            return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0:
            self._build()
        return True

    def lt(self, x):
        # Find the largest element < x, or None if it doesn't exist.
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x):
        # Find the largest element <= x, or None if it doesn't exist.
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x):
        # Find the smallest element > x, or None if it doesn't exist.
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x):
        # Find the smallest element >= x, or None if it doesn't exist.
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, x):
        if x < 0:
            x += self.size
        if x < 0:
            raise IndexError
        for a in self.a:
            if x < len(a):
                return a[x]
            x -= len(a)
        raise IndexError

    def index(self, x):
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x):
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans


class SortedMultiSet:
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None):
        if a is None:
            a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [a[size*i//bucket_size : size*(i+1)//bucket_size] for i in range(bucket_size)]

    def __init__(self, a=[]):
        a = list(a)
        if not all(a[i] < a[i+1] for i in range(len(a)-1)):
            a = sorted(a)
        self._build(a)

    def __iter__(self):
        for i in self.a:
            for j in i:
                yield j
    
    def __reversed__(self):
        for i in reversed(self.a):
            for j in reversed(i):
                yield j

    def __len__(self):
        return self.size

    def __repr__(self):
        return "SortedMultiSet" + str(self.a)

    def __str__(self):
        s = str(list(self))
        return "{" + s[1:len(s)-1] + "}"

    def _find_bucket(self, x):
        # Find the bucket which should contain x. self must not be empty.
        for a in self.a:
            if x <= a[-1]:
                return a
        return a

    def __contains__(self, x):
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x

    def count(self, x):
        # Count the number of x
        return self.index_right(x) - self.index(x)

    def add(self, x):
        # Add an element and return True if added. O(√N)
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a = self._find_bucket(x)
        insort(a, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
            return True

    def discard(self, x):
        # Remove an element and return True if removed. O(√N)
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x:
            return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0:
            self._build()
        return True

    def lt(self, x):
        # Find the largest element < x, or None if it doesn't exist.
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x):
        # Find the largest element <= x, or None if it doesn't exist.
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x):
        # Find the smallest element > x, or None if it doesn't exist.
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x):
        # Find the smallest element >= x, or None if it doesn't exist.
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, x):
        if x < 0:
            x += self.size
        if x < 0:
            raise IndexError
        for a in self.a:
            if x < len(a):
                return a[x]
            x -= len(a)
        raise IndexError

    def index(self, x):
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x):
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans