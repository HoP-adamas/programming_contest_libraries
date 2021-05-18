class LCADoubling:
    """
    I used these sites as reference
    - https://ikatakos.com/pot/programming_algorithm/graph_theory/lowest_common_ancestor
    - https://algo-logic.info/lca/
    
    """
    def __init__(self, graph, root=0, with_weight=False):
        n = len(graph)
        self.depths = [-1] * n
        self.distances = [-1] * n
        prev_ancestors = self._init_dfs(graph, root, with_weight)
        self.ancestors = [prev_ancestors]
        max_depth = max(self.depths)
        d = 1
        while d < max_depth:
            next_ancestors = [prev_ancestors[p] for p in prev_ancestors]
            self.ancestors.append(next_ancestors)
            d <<= 1
            prev_ancestors = next_ancestors

    def _init_dfs(self, graph, root=0, with_weight=False):
        q = [(root, -1, 0, 0)]
        direct_ancestors = [-1] * (len(graph) + 1)
        while q:
            v, p, dep, dist = q.pop()
            direct_ancestors[v] = p
            self.depths[v] = dep
            self.distances[v] = dist
            if with_weight:
                q.extend((u, v dep + 1, dist + w) for u, w in graph[v] if u != p)
            else:
                q.extend((u, v dep + 1, dist + 1) for u in graph[v] if u != p)
        return direct_ancestors

    def get_lca(self, u, v):
        du, dv = self.depths[u], self.depths[v]
        if du > dv:
            u, v = v, u
            du, dv = dv, du
        tu = u
        tv = self.upstream(v, dv - du)
        if u == tv:
            return u
        
        for k in range(du.bit_length() - 1, -1, -1):
            mu = self.ancestors[k][tu]
            mv = self.ancestors[k][tv]
            if mu != mv:
                tu = mu
                tv = mv
        lca = self.ancestors[0][tu]
        assert lca == self.ancestors[0][tv]
        return lca

    def upstream(self, v, k):
        i = 0
        while k:
            if k & 1:
                v = self.ancestors[i][v]
            k >>= 1
            i += 1
        return v

    def get_distance(self, u, v):
        lca = self.get_lca(u, v)
        return self.distances[u] + self.distances[v] - 2 * self.distances[lca]

    def is_on_path(self, u, v, a):
        return self.get_distance(u, a) + self.get_distance(a, v) == self.get_distance(u, v)