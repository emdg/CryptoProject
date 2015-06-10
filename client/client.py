import urllib, json, math, time

public_url = "http://localhost:8080/publickey"

response = urllib.urlopen(public_url)
data = json.loads(response.read())

n = int(data['n'])
e = bin(int(data['e']))[2:]

print n

print e



def generateGuess(e):
	g = []
	for i in range(0, len(e)):
		if i < 36:
			g.append( e[i])
		else:
			g.append('0')
	return g

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)

def modinv(a, m):
	g,x,y = egcd(a,m)
	
	if g != 1:
		raise Exception("modular inverse does not exist")
	else:
		return x % m
def sendGuess(g):
	start = time.clock()
	decrypt_url = " http://localhost:8080/decrypt?message={0}".format(g)

	response = urllib.urlopen(decrypt_url)
	data = json.loads(response.read())
	end = time.clock()
	return (end - start)

def getDecryptTime(uh):
	times = []
	for i in range(50):
		times.append(sendGuess(uh))
	times.sort()
	return times[3]

def makeAttack(g, e, n):
	differences = []
	for i in range(1, 32):
		print "n in makeAttack ", n
		T = T1 = 0
		g1 = g
		g1[i] = '1'
		h1 = round(math.sqrt(int("".join(g1), 2)))
		
		h = round(math.sqrt(int("".join(g), 2)))
		times = []
		for j in range(0, 1):
			R = 2**(len(e)) % n
			ug = long((modinv(R, n) * int("".join(g), 2 )) % n)
			T += getDecryptTime(bin(ug)[2:])
		
		for j in range(0, 1):
			R = 2**(len(e)) % n
			ug1 = long((modinv(R, n) * int("".join(g1), 2) ) % n)
			T1 += getDecryptTime(bin(ug1)[2:])
		
		differences.append(abs(T-T1))
	total = 0
	for x in differences:
		total += x
	average = total/len(differences)

	num = []

	for k in differences:
		if k > 1.004*average:
			num.append('0')
		else:
			num.append('1')
	print "number deduced in binary: ", "".join(num)
	print
	q = long(int("".join(num), 2))
	print "q number in decimal", q
	print
	print "n divided by q: ", n/q
	print 
	private_key = modinv(long(int("".join(e), 2)), (q-1)*((n/q) - 1))
	print "which gives private key: ", private_key
	print "with length: ", len(str(private_key)) 

g = []
g.append('1')
for x in range(1,32):
	g.append('0')
makeAttack(g, e, n)
