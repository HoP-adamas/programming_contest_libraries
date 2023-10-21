def count_digit(n):
  d = 0
  while n:
    d+=1
    n//=10
  return d
