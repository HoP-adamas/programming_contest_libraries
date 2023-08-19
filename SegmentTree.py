class SegmentTree:
	def __init__(self,n, ele=10**10):
		'''
		n: the number of element
		ele: unit element
		'''

		self.ide_ele = ele
		self.n = n
		self.num = 1 << (n-1).bit_length()
		self.seg=[self.ide_ele]*2*self.num


	#####segfunc######

	def segfunc(self,x,y):
		'''
		define a binary operation on the segment tree
		'''
		return min(x, y)

	def init(self,init_val):
		#set_val
		for i in range(self.n):
			self.seg[i+self.num]=init_val[i]	
		#built
		for i in range(self.num-1, 0,-1) :
			self.seg[i]=self.segfunc(self.seg[2*i],self.seg[2*i+1]) 
		
	def update(self,k,x):
		k += self.num
		self.seg[k] = x
		while k > 1:
			k >>= 1
			self.seg[k] = self.segfunc(self.seg[k*2],self.seg[k*2+1])
		
	def query(self,p,q):
		if q<=p:
			return self.ide_ele
		p += self.num
		q += self.num
		res=self.ide_ele
		while q > p:
			if p&1:
				res = self.segfunc(res,self.seg[p])
				p += 1
			if q&1:
				q -= 1
				res = self.segfunc(res,self.seg[q])
			p >>= 1
			q >>= 1

		return res