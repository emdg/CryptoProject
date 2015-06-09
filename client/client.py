import urllib, json, math, time



message = "hello"
encrypt_url = "https://polar-coast-7047.herokuapp.com/encrypt?message={0}".format(message)
response = urllib.urlopen(encrypt_url);
data = json.loads(response.read())

print data['signature']

decrypt_url = " https://polar-coast-7047.herokuapp.com/decrypt?message={0}".format(data['signature'])

response = urllib.urlopen(decrypt_url)
data = json.loads(response.read())

print data['message']
n = 7354628033541988736750302987383110880226650897465367854771937493624543493934806747233081996309885239339238683661216791054337975332653787872939937701072757
e = 6528529828075575923152619377285048409711625043295897801139262997871415501509700229436121007530388984678945730890721390805825241477071752307557046080272561
e = bin(e)[2:]



print len(e)

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
	decrypt_url = " https://polar-coast-7047.herokuapp.com/decrypt?message={0}".format(g)

	response = urllib.urlopen(decrypt_url)
	data = json.loads(response.read())
	end = time.clock()
	return (end - start)

def getDecryptTime(uh):
	times = []
	for i in range(7):
		times.append(sendGuess(uh))
	times.sort()
	return times[3]

def makeAttack(g, e, n):
	differences = []
	for i in range(1, 256):
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
	for x in range(36):
		num.append('1')

	for k in differences:
		if k > 100*average:
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
	print "which gives private key: ", modInv(e, (q-1)*((n/q) - 1)) 

g = []
g.append('1')
for x in range(1,256):
	g.append('0')
makeAttack(g, e, n)
