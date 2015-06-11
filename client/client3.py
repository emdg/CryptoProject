import time
import random
import urllib
import json
import math
public_url = "http://localhost:8080/publickey"

response = urllib.urlopen(public_url)
data = json.loads(response.read())

N = int(data['n'])

print N



def generateZSet():
    z = [random.randint(N**(1/3.0) + 1, N**(1/2.0) - 1) for p in range(10000)]
    m_list = []
    for message in z:
        encrypt_url = "http://localhost:8080/encrypt?message={0}".format(message)
        response = urllib.urlopen(encrypt_url)
        data = json.loads(response.read())
        m_list.append(data['signature'])

    return m_list
def generateYSet():
    y = [random.randint(0, N**(1/3.0)-1) for p in range(10000)]
    m_list = []

    for message in y:
        encrypt_url = "http://localhost:8080/encrypt?message={0}".format(message)
        response = urllib.urlopen(encrypt_url)
        data = json.loads(response.read())
        m_list.append(data['signature'])
    return m_list

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



def modExp(M, d, n, r):
    M_bar = (M*r) % n
    C_bar = r % n
    d_guess = d
    d_guess += '1'
    reduction = False
    for ei in d_guess:
        C_bar, reduction = monPro(C_bar, C_bar, r, n)
        if(ei == '1'):
            C_bar, reduction  = monPro(M_bar, C_bar, r, n)

    return reduction

def RSACheckReduction(guess, message, n, r):
    return modExp(message, guess, n, r)

def sendGuess(message):
    decrypt_url = "http://localhost:8080/decrypt?message={0}".format(message)
    start = time.time()
    response = urllib.urlopen(decrypt_url)
    end = time.time()
    return end-start


def getDecryptTime(message):
    l = []
    for i in range(300):
        l.append(sendGuess(message))
    return median(l)
    return reduce(lambda x, y: x + y, l) / len(l)


def median(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    return sum(sorted(lst)[half:half + even]) / float(even)




def getSampleMessages(size):
    return [random.randint(100000, 10000000) for s in range(size)]



class RSAAttack(object):
    def __init__(self):
        self.upper = int(math.sqrt(N))
        self.lower = int("1" + "0" * 15, 2) - 1

    def guess(self):
        pUpper = 0
        pLower = 0
        previousUpVal = 1000
        previousDownVal = 1000
        for i in range(0, 8):
            print self.upper
            print self.lower
            up =  getDecryptTime(self.upper)
            low =  getDecryptTime(self.lower)
            print up
            print low

            if (up - low > 0):
                self.upper = int(math.ceil((self.upper + self.lower) / 2.0))
            else:
                self.lower = int(math.floor((self.upper + self.lower) / 2.0))
            previousUpVal = up

            print "upper: ", self.upper
            print "lower: ", self.lower




def doAttack(n):
    r = generate_r(n)
    bits_to_solve = 16
    secretKey = [1] + [0] * 15
    upper = int("1111111111111111", 2)
    av1 =  getDecryptTime(str(upper))
    lower = int("1000000000000000" , 2)
    av0 =  getDecryptTime(str(lower))
    print "upper: ", av1
    print "lower: ", av0
    print "upper - lower: ", av1 - av0
    # for x in range(1, 16):
    #     print secretKey
    #     av0 =  getDecryptTime(str(int("".join(map(lambda x:str(x), secretKey)), 2)))
    #     secretKey[x] = 1
    #     av1 = getDecryptTime(str(int("".join(map(lambda x:str(x), secretKey)), 2)))
    #     if av1 - av0 > 0:
    #         continue
    #     else:
    #         secretKey[x] = 0
    # print secretKey


# for i in xrange(N/4, N/2):
#     print bin(i)

#doAttack(N)

#a = RSAAttack()
#a.guess()
print getDecryptTime(41453)
#print getDecryptTime(42314)
