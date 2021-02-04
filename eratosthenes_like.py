# ABC 160 D
'''
与えられた数列の中でエラトステネスの篩と同様の操作を行う。
'''

n = int(input())
A = list(map(int,input().split()))
A.sort()
is_prime = [0]*(A[-1]+1)

for num in A:
  if is_prime[num] == 0:
    for j in range(num,A[-1]+1,num):
      is_prime[j] += 1
  else:
    is_prime[num] += 1
ans = 0
for num in A:
  if is_prime[num] == 1:
    ans += 1
print(ans)