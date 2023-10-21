class BellmanFord:
	'''
	ベルマンフォード法のクラス
	(from, to, cost)の形式で辺をインスタンスに追加していく。

	'''
	def __init__(self,n):
		self.edges = []
		self.has_negative_loop = None # shortest_pathを実行すると判定できる

	def add_edge(self, f, t, cost):
		self.edges.append((f,t,cost))

	def shortest_path(self, start):
		INF = 10**18
		n = len(self.vertex)
		dis = [INF]*n 
		dis[start] = 0
		cnt = 0
		for v in range(n):
			updated = False
			for e in self.edges:
				if dis[e[0]] != INF and dis[e[0]] + e[2] < dis[e[1]]:
					dis[e[1]] = dis[e[0]] + e[2]
					updated = True
				
				if not updated:
					break
			cnt += 1

		if cnt == n:
			self.has_negative_loop = True
		else:
			self.has_negative_loop = False

		return dis

	# ==============================================================================================
import heapq

class Dijkstra:
    '''
    ダイクストラ法のクラス
    グラフは連結リストとして管理する。各辺は(to, cost)というタプルにしておく。
    初期化のときに連結リストを渡す。

    shortest_pathは最短経路とstartからの最短距離を配列として返す。
	'''
    def __init__(self, graph, with_cost=True):
        self.graph = graph
        self.vertex_num = len(graph)
        self.prev = None
        self.with_cost = with_cost

    def shortest_path(self, start): 
        INF = 10**18
        dis = [INF]*self.vertex_num
        self.prev = [-1]*self.vertex_num

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))
        while priority_queue:
            v_dis, v = heapq.heappop(priority_queue)

            if dis[v] < v_dis:
                continue
            for e in self.graph[v]:
                if self.with_cost:
                    if dis[e[0]] > v_dis + e[1]:
                        dis[e[0]] = v_dis + e[1]
                        self.prev[e[0]] = v
                        heapq.heappush(priority_queue, (dis[e[0]], e[0]))
                else:
                    if dis[e] > v_dis + 1:
                        dis[e] = v_dis + 1
                        self.prev[e] = v
                        heapq.heappush(priority_queue, (dis[e], e))
    
        return dis

    def get_shotest_path(self, to):
        if self.prev == None:
            raise Exception('The shortest path does not be calculated. Please call the method "shortest_path(start_vertex_index)"')
        path = []
        cur = to
        while cur != -1:
            path.append(cur)
            cur = self.prev[cur]
        path = path[::-1]

        return path

	# ================================================================================================================================

def warshall_floyd(dp):
	v_num = len(dp)
	for k in range(v_num):
		for i in range(v_num):
			for j in range(v_num):
				dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])


