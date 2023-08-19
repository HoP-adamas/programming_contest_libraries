import heapq
from collections import defaultdict

class Multiset():

	'''
	順序付き多重集合のクラス
	要素の挿入がO(logN)
	要素の削除がO(logN)
	要素の存在確認がO(1)
	集合の最小値取得がO(1)

	'''
	def __init__(self, A = []):
		self.heap = []
		self.dict = defaultdict(int)

		self.size = 0
		for a in A:
			self.add(a)

	def add(self,x):
		heapq.heappush(self.heap, x)
		self.dict[x] += 1
		self.size += 1

	def erase(self, x):
		if self.dict[x] > 0:
			self.dict[x] -= 1
			self.size -= 1

			while len(self.heap) != 0:
				if self.dict[self.heap[0]] == 0:
					heapq.heappop(self.heap)
				else:
					break
		else:
			print(x, 'is not in Multiset')
			exit()

	def count(self, x):
		return self.dict[x]

	def find(self, x):
		return self.dict[x] > 0

	def minimum(self):
		return self.heap[0]