def scc(g, rg):
	n = len(g)
	
	visit = [0]*n
	group = [None]*n
	order = []
	
	def dfs(s):
		visit[s] = 1
		for t in g[s]:
			if not visit[t]:
				dfs(t)
		order.append(s)

	def rdfs(s, col):
		group[s] = col
		visit[s] = 1
		for t in rg[s]:
			if not visit[t]:
				rdfs(t, col)
	
	for i in range(n):
		if not visit[i]:
			dfs(i)
	del visit
	visit = [0]*n
	label = 0
	for s in reversed(order):
		if not visit[s]:
			rdfs(s, label)
		label += 1
	
	return label, group

def construct(g, label, group):
	n = len(g)
	g0 = [set() for _ in range(label)]
	gp = [[] for _ in range(label)]
	for v in range(n):
		lbs = group[v]
		for w in g[v]:
			lbt = group[w]
			if lbs == lbt:
				continue
			g0[lbs].add(lbt)
		gp[lbs].append(v)
	return g0, gp