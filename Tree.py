class Tree():
    def __init__(self, n, decrement=1):
        self.n = n
        self.edges = [[] for _ in range(n)]
        self._edge_label = [[] for _ in range(n)]
        self.root = None
        self.size = [1]*n       # number of nodes in subtree
        self.decrement = decrement
 
    def add_edge(self, u, v, i):
        u, v = u-self.decrement, v-self.decrement
        self.edges[u].append(v)
        self.edges[v].append(u)
        self._edge_label[u].append((v,i))
        self._edge_label[v].append((u,i))
 
    def add_edges(self, edges):
        for i, p in enumerate(edges):
            u, v = p
            u, v = u-self.decrement, v-self.decrement
            self.edges[u].append(v)
            self.edges[v].append(u)
            self._edge_label[u].append((v, i))
            self._edge_label[v].append((u, i))
 
    def set_root(self, root):
        root -= self.decrement
        self.depth = [-1]*self.n
        self.root = root
        self.par = [-1]*self.n
        self.depth[root] = 0
        self.edge_label = [-1]*self.n
        self.order = [root]
        self.chi = [[] for _ in range(self.n)]
        next_set = [root]
        while next_set:
            p = next_set.pop()
            for q, i in self._edge_label[p]:
                if self.depth[q] != -1: continue
                self.par[q] = p
                self.chi[p].append(q)
                self.depth[q] = self.depth[p]+1
                self.edge_label[q]=i
                self.order.append(q)
                next_set.append(q)
        for p in self.order[::-1]:
            for q in self.edges[p]:
                if self.par[p] == q: continue
                self.size[p] += self.size[q]
 
    def diameter(self, path=False):
        # assert self.root is not None
        u = self.depth.index(max(self.depth))
        dist = [-1]*self.n
        dist[u] = 0
        prev = [-1]*self.n
        next_set = [u]
        while next_set:
            p = next_set.pop()
            for q in self.edges[p]:
                if dist[q] != -1: continue
                dist[q] = dist[p]+1
                prev[q] = p
                next_set.append(q)
        d = max(dist)
        if path:
            v = w = dist.index(d)
            path = [v+1]
            while w != u:
                w = prev[w]
                path.append(w+self.decrement)
            return d, v+self.decrement, u+self.decrement, path
        else: return d
 
    def rerooting(self, op, merge, id):
        # assert self.root is not None
        dp1 = [id] * self.n
        dp2 = [id] * self.n
        for p in self.order[::-1]:
            t = id
            for q in self.edges[p]:
                if self.par[p] == q: continue
                dp2[q] = t
                t = merge(t, op(dp1[q], p, q))
            t = id
            for q in self.edges[p][::-1]:
                if self.par[p] == q: continue
                dp2[q] = merge(t, dp2[q])
                t = merge(t, op(dp1[q], p, q))
            dp1[p] = t
        for q in self.order[1:]:
            pq = self.par[q]
            dp2[q] = op(merge(dp2[q], dp2[pq]), q, pq)
            dp1[q] = merge(dp1[q], dp2[q])
        return dp1
 
    def heavy_light_decomposition(self):
        """
        return flat array of lists of heavy edges (1-indexed if decrement=True)
        """
        # assert self.root is not None
        self.vid = [-1]*self.n
        self.hld = [-1]*self.n
        self.head = [-1]*self.n
        self.head[self.root] = self.root
        self.heavy_node = [-1]*self.n
        next_set = [self.root]
        for i in range(self.n):
            """ for tree graph, dfs ends in N times """
            p = next_set.pop()
            self.vid[p] = i
            self.hld[i] = p+self.decrement
            maxs = 0
            for q in self.edges[p]:
                """ encode direction of Heavy edge into heavy_node """
                if self.par[p] == q: continue
                if maxs < self.size[q]:
                    maxs = self.size[q]
                    self.heavy_node[p] = q
            for q in self.edges[p]:
                """ determine "head" of heavy edge """
                if self.par[p] == q or self.heavy_node[p] == q: continue
                self.head[q] = q
                next_set.append(q)
            if self.heavy_node[p] != -1:
                self.head[self.heavy_node[p]] = self.head[p]
                next_set.append(self.heavy_node[p])
        return self.hld
 
    def lca(self, u, v):
        # assert self.head is not None
        u, v = u-self.decrement, v-self.decrement
        while True:
            if self.vid[u] > self.vid[v]: u, v = v, u
            if self.head[u] != self.head[v]:
                v = self.par[self.head[v]]
            else:
                return u + self.decrement
 
    def path(self, u, v):
        """ return the path array of the shortest path on u-v """
        p = self.lca(u, v)
        u, v, p = u-self.decrement, v-self.decrement, p-self.decrement
        R = []
        while u != p:
            yield u+self.decrement
            u = self.par[u]
        yield p+self.decrement
        while v != p:
            R.append(v)
            v = self.par[v]
        for v in reversed(R):
            yield v+self.decrement
 
    def distance(self, u, v):
        # assert self.head is not None
        p = self.lca(u, v)
        u, v, p = u-self.decrement, v-self.decrement, p-self.decrement
        return self.depth[u] + self.depth[v] - 2*self.depth[p]
 
    def find(self, u, v, x):
        return self.distance(u,x)+self.distance(x,v)==self.distance(u,v)
 
    def path_to_list(self, u, v, edge_query=False):
        """
        transform a half-open interval into segments on the self.hld, which is the heavy edge list
 
        edge_query: map from edge (par,chi) to point (chi)
                (note: The root is never updated)
        """
        # assert self.head is not None
        u, v = u-self.decrement, v-self.decrement
        while True:
            if self.vid[u] > self.vid[v]: u, v = v, u
            if self.head[u] != self.head[v]:
                yield self.vid[self.head[v]], self.vid[v] + 1
                v = self.par[self.head[v]]
            else:
                yield self.vid[u] + edge_query, self.vid[v] + 1
                return
 
    def ver_to_idx(self, u):
        """ return index on self.hld corresponding to vertex u """
        return self.vid[u-self.decrement]
 
    def idx_to_ver(self, i):
        """ from index i on self.hld to vertex-index """
        return self.hld[i]
 
    def idx_to_edge(self, i):
        """ from index i on self.hld to edge-index """
        return self.edge_label[self.hld[i]-self.decrement]
 
    def subtree_query(self, u):
        u -= self.decrement
        return self.vid[u], self.vid[u] + self.size[u]
 
    def top_down(self,dp):
        def merge(dp_chi,dp_par):
            return dp_chi^dp_par
        for chi in self.order[1:]:
            par=self.par[chi]
            dp[chi]=merge(dp[chi], dp[par])
        return dp
 
    def top_down_edge_query(self,dp):
        def merge(dp_chi,dp_par):
            return dp_chi^dp_par
        for p in self.order[1+len(self.edges[self.root]):]:
            chi,par=self.edge_label[p],self.edge_label[self.par[p]]
            dp[chi]=merge(dp[chi], dp[par])
        return dp
 
    def bottom_up(self,dp):
        def merge(dp_chi,dp_par):
            return dp_chi+dp_par
        for par in self.order[::-1]:
            for chi in self.edges[par]:
                if self.par[par] == chi: continue
                dp[par]=merge(dp[chi],dp[par])
        return dp
 
    def draw(self):
        import matplotlib.pyplot as plt
        import networkx as nx
 
        G = nx.Graph()
        for x in range(self.n):
            for y in self.edges[x]:
                G.add_edge(x + self.decrement, y + self.decrement)
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos)
        plt.axis("off")
        plt.show()