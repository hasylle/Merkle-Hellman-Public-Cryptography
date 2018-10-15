def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def xgcd(a, b):
    """
    Extended Euclidean Algorithm
    ax + by = gcd(a,b)
    :param a:
    :param b:
    :return:
    """
    x0 = 1 #old x
    x1 = 0 #new x
    y0 = 0 #old y
    y1 = 1 #new y
    while b:
        if b > 0:
            q = a // b
        else:
            q = 0
        a, b = b, a % b
        x0, x1 = x1, x0 - q*x1
        y0, y1 = y1, y0 - q*y1
    return a, x0, y0

def modinv(a, n):
    """
    Modular inverse using Extended Euclidean Algorithm
    x = 1/a (mod n)
    (x * a)(mod n) == 1
    :param a:
    :param n:
    :return: the modular inverse if success, False otherwise
    """
    if n == 0:
        return False
    g, x, y = xgcd(a, n)
    if g == 1:
        return x % n
    else:
        return False


if __name__ == '__main__':
    print(gcd(32, 20))
    #Test
    g = xgcd(300, 1024)
    print(g)
    i = modinv(53, 120)
    print(i)