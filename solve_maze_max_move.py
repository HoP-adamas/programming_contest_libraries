# ABC 151 D 問題
"""
高橋君は、縦 Hマス、横Wマスの 
H × Wマスからなる迷路を持っています。
上から i行目、左から j列目のマス (i,j)は、
S_ijが # のとき壁であり、. のとき道です。
道のマスからは、上下左右に隣接する道のマスに移動することができます。
迷路の外に移動すること、壁のマスへ移動すること、斜めに移動することはできません。
高橋君は、道のマスからスタートとゴールを自由に決め、迷路を青木君に渡します。
青木君は、移動回数が最小になるようにしてスタートからゴールまで移動します。
高橋君がスタートとゴールの位置を適切に定めたとき、青木君の移動回数は最大で何回になるでしょうか？
"""

from collections import deque
h,w=map(int,input().split())
maze = []
D = [(-1,0), (1,0), (0,-1), (0,1)]

for _ in range(h):
  maze.append(list(input()))
max_move = 0

for sy in range(h):
  for sx in range(w):
    if maze[sy][sx] == '#':
      continue
    
    dp = [[-1]*w for i in range(h)]
    dp[sy][sx] = 0
    queue = deque()
    queue.append((sy,sx))
    
    while queue:
      y,x = queue.popleft()
      for dx,dy in D:
        Y = y+dy
        X = x+dx
        if 0<=Y<h and 0<=X<w and maze[Y][X] == '.' and dp[Y][X] == -1:
          dp[Y][X] = dp[y][x] + 1
          queue.append((Y,X))
    tmp_max = 0
    for row in dp:
      tmp_max = max(tmp_max,max(row))
    max_move = max(max_move, tmp_max)
print(max_move)
