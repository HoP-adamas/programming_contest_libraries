from UnionFind import UnionFind

edges = []

for i in range(num_edge):
	f,t,c = map(int,input().split())
	edges.append((f,t,c))

def kruskal(edges, num_vertex):
	uft = UnionFind(num_vertex)
	cost_sum = 0	# 最小全域木のコストの総和

	edges = sorted(edges, key = lambda x: x[2])
	for e in edges:
		if not uft.find(e[0], e[1]):
			uft.union(e[0], e[1])
			cost_sum += e[2]
	return cost_sum