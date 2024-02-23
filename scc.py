# reference
# https://github.com/atcoder/ac-library/blob/master/atcoder/internal_scc.hpp
# https://github.com/atcoder/ac-library/blob/master/atcoder/internal_csr.hpp

import sys

sys.setrecursionlimit(500005)


class CSR:

    def __init__(self, n, edges):
        self.start = [0] * (n + 1)
        self.elist = [0] * len(edges)
        for e in edges:
            self.start[e[0] + 1] += 1

        for i in range(1, n + 1):
            self.start[i] += self.start[i - 1]

        counter = self.start[::]
        for e in edges:
            self.elist[counter[e[0]]] = e[1]
            counter[e[0]] += 1


class SccGraph:

    def __init__(self, n=0):
        self._n = n
        self._edges = []

    def __len__(self):
        return self._n

    def add_edge(self, s, t):
        assert 0 <= s < self._n and 0 <= t < self._n
        self._edges.append([s, t])

    def _scc_ids(self):

        g = CSR(self._n, self._edges)
        now_ord = 0
        group_num = 0
        visited = []
        low = [0] * self._n
        order = [-1] * self._n
        ids = [0] * self._n

        def _dfs(self_dfs, v):
            nonlocal now_ord, group_num
            low[v] = now_ord
            order[v] = now_ord
            now_ord += 1
            visited.append(v)
            for i in range(g.start[v], g.start[v + 1]):
                t = g.elist[i]
                if order[t] == -1:
                    self_dfs(self_dfs, t)
                    low[v] = min(low[v], low[t])
                else:
                    low[v] = min(low[v], order[t])

            if low[v] == order[v]:
                while True:
                    u = visited.pop()
                    order[u] = self._n
                    ids[u] = group_num
                    if u == v:
                        break
                group_num += 1

        for i in range(self._n):
            if order[i] == -1:
                _dfs(_dfs, i)

        for i, x in enumerate(ids):
            ids[i] = group_num - 1 - x

        return group_num, ids

    def scc(self):

        group_num, ids = self._scc_ids()
        counts = [0] * group_num
        for x in ids:
            counts[x] += 1

        groups = [[] for _ in range(group_num)]
        for i in range(self._n):
            groups[ids[i]].append(i)

        return groups
