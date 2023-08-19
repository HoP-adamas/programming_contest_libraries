class Vector:

	def __init__(self, v):
		self.dim = len(v)
		self._vector = v

	def __getitem__(self, item):
		return self._vector[item]

	def __setitem__(self, item, val):
		self._vector[item] = val

	def __neg__(self):
		n, vec = self.dim, self._vector
		res = []
		for x in vec:
			res.append(-x)
		return Vector(res)

	def __add__(self, other):
		n, vec = self.dim, self._vector
		res = vec.copy()
		for i in range(n):
			res[i] += other._vector[i]
		return Vector(res)

	def __sub__(self, other):
		n, vec = self.dim, self._vector
		res = vec.copy()
		for i in range(n):
			res[i] -= other._vector[i]
		return Vector(res)

	def __floordiv__(self, c):
		n, vec = self.dim, self._vector
		res = vec.copy()
		for i in range(n):
			res[i] = res[i] // c
		return Vector(res)

	def __mod__(self, c):
		n, vec = self.dim, self._vector
		res = vec.copy()
		for i in range(n):
			res[i] = res[i] % c
		return Vector(res)

	def __eq__(self,other):
		if type(other) == Vector:
			return self._vector == other._vector
		return False
 
	def __ne__(self,other):
		if type(other) == Vector:
			return self._vector != other._vector
		return True
 
	def __len__(self):
		return self.dim