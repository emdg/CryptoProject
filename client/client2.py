import time
import random
import urllib
import json

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
	start = time.clock()
	decrypt_url = "http://localhost:8080/decrypt?message={0}".format(message)
	response = urllib.urlopen(decrypt_url)
	end = time.clock()
	return end-start


def getDecryptTime(message):
	times = [] 
	for i in range(1):
		times.append(sendGuess(bin(message)[2:]))
	times.sort()
	return sum(times)/len(times)

def getSampleMessages(size):
	return [random.randint(100000, 10000000) for s in range(size)]


def doAttack(n):
	r = generate_r(n)
	bits_to_solve = 128
	secretKey = '1'

	for i in range(1, bits_to_solve):
		sample_list = getSampleMessages(10000)
		reduction_list = []
		no_reduction_list = []
		for sample in sample_list:
			if RSACheckReduction(secretKey, sample, n, r):
				reduction_list.append(sample)
			else:
				no_reduction_list.append(sample)
					
		no_reduction_times = []	
		reduction_times = []
		
		for y in no_reduction_list:
			no_reduction_times.append(getDecryptTime(y))
		for x in reduction_list:
			reduction_times.append(getDecryptTime(x))

		average_with_reduction = sum(reduction_times) / len(reduction_times)
		average_without_reduction = sum(no_reduction_times)/len(no_reduction_times)

		print average_with_reduction

		print average_without_reduction
doAttack(N)
