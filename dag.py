'''
DAG(Directed Acyclic Graph)についての関数をここでまとめる。
'''
from collections import deque
def topological_sort(graph):
	'''
	トポロジカルソート
	ソートした頂点の番号を返す。
	もし、閉路があった場合は-1を返す。
	'''
	ret = []
	n_vertex = len(graph)
	ind = [0]*n_vertex  # 入次数
	for i in range(n_vertex):
		for e in graph[i]:
			ind[e] += 1
	
	queue = deque()
	for i in range(n_vertex):
		if ind[i] == 0:
			queue.append(i)
	
	while queue:
		now = queue.popleft()
		ret.append(now)
		for e in graph[now]:
			ind[e] -= 1
			if ind[e] == 0:
				queue.append(e)
	if len(ret) != n_vertex:
		return -1
	return ret