def gcd_ext(a,b):
    """
    ax + by = gcd(a,b) を満たすxが最小の(x,y)
    一般解は (x+k*b//gcd(a,b),y-k*a//gcd(a,b)) と表される
    """
    x0, y0, x, y = 0, 1, 1, 0
    while b!=0:
        q=a//b
        a,b=b,a%b
        x0, y0, x, y = x-q*x0, y-q*y0, x0, y0
    else: return (x,y)
 
def mod_solve(a,b,MOD):
    """
    ax=b (mod MOD)
    """
    x,y=gcd_ext(a,MOD)
    g=a*x+MOD*y
    a_inv=x%MOD
    if b%g: return -1
    a,b,MOD=a//g,b//g,MOD//g
    return b*a_inv%MOD