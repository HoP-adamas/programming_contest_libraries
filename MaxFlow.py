from collections import deque

class MaxFlow:
    """
    Dinic's algorithm
    O(N^2|E|)
    reference:
    - https://ikatakos.com/pot/programming_algorithm/graph_theory/maximum_flow
    """

    def __init__(self, n=0):
        self._n = n
        self.g = [[] for _ in range(n)]
        self.depth = None
        self.progress = None

    def add_edge(self, _from, to, cap):
        """
        elements:
        0: capacity
        1: destination
        2: reverse edge
        """
        self.g[_from].append([cap, to, len(self.g[to])])
        self.g[to].append([0, _from, len(self.g[_from]) - 1])

    def bfs(self, s):
        depth = [-1] * self._n
        depth[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for cap, to, rev in self.g[v]:
                if cap > 0 and depth[to] < 0:
                    depth[to] = depth[v] + 1
                    q.append(to)
        self.depth = depth

    def dfs(self, v, t, flow):
        if v == t:
            return flow
        edges_v = self.g[v]
        for i in range(self.progress[v], len(edges_v)):
            self.progress[v] = i
            cap, to, rev = edge = edges_v[i]
            if cap == 0 or self.depth[v] >= self.depth[to]:
                continue
            d = self.dfs(to, t, min(flow, cap))
            if d == 0:
                continue
            edge[0] -= d
            self.g[to][rev][0] += d
            return d
        return 0

    def max_flow(self, s, t):
        flow = 0
        while True:
            self.bfs(s)
            if self.depth[t] < 0:
                return flow
            self.progress = [0] * self._n
            current_flow = self.dfs(s, t, float("inf"))
            while current_flow > 0:
                flow += current_flow
                current_flow = self.dfs(s, t, float("inf"))
