# ABC 153 E

h,n=map(int,input().split())
INF = 10**9
A = []
B = []
for _ in range(n):
	a,b = map(int,input().split())
	A.append(a)
	B.append(b)

# dp[i+1][j] i番目までの魔法を使ってＨＰをj減らすときのＭＰ消費の最小値
dp = [[0]*(10**4+1) for i in range(10**3+1)]
for j in range(h+1):
	dp[0][j] = INF
for i in range(n+1):
	dp[i][0] = 0

'''
dp[i][0] = 0
dp[i+1][j] = min{dp[i][j - k*A[i]] + k*B[i]|0<=k}
		   = min(dp[i][j], dp[i+1][j-A[i]] + B[i])
'''

for i in range(1,n+1):
	for j in range(h+1):
		dp[i][j] = min(dp[i-1][j], dp[i][j-A[i-1]] + B[i-1])
print(dp[n][h])
