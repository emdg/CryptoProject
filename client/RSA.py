import time
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def generate_r(n):
    x = 0
    while(2**x < n):
        x += 1
    return 2 ** x

def monPro(a, b, r, n):

    r_inv = modinv(r, n)
    n_prime = (r * r_inv - 1)/n

    t = a * b
    m = (t*n_prime) % r
    u = (t + m*n)/r
    if (u >= n):
        return (u-n, True)
    return (u, False)

def monProSleepy(a, b, r, n):

    r_inv = modinv(r, n)
    n_prime = (r * r_inv - 1)/n

    t = a * b
    m = (t*n_prime) % r
    u = (t + m*n)/r
    if (u >= n):
	time.sleep(0.0002)
        return (u-n, True)
    return (u, False)



def modExp(M, d, n, r):
    M_bar = (M*r) % n
    C_bar = r % n
    d_guess = d
    reduction = False
    for ei in d_guess:
        C_bar, reduction = monPro(C_bar, C_bar, r, n)
        if(ei == '1'):
            C_bar, reduction  = monPro(M_bar, C_bar, r, n)
	C_bar, tmp = monPro(C_bar, 1, r, n)
    return C_bar, reduction


def modExpSleepy(M, d, n, r):
    M_bar = (M*r) % n
    C_bar = r % n
    d_guess = d
    reduction = False
    for ei in d_guess:
        C_bar, reduction = monProSleepy(C_bar, C_bar, r, n)
        if(ei == '1'):
            C_bar, reduction  = monProSleepy(M_bar, C_bar, r, n)
	C_bar, tmp = monProSleepy(C_bar, 1, r, n)
    return C_bar, reduction

def CheckReduction(guess, message, n, r):
    r,e= modExp(message, guess, n, r)
    return e

def DoRSA(guess, message, n, r):
	r, e = modExpSleepy(message, guess, n, r)
	return r


