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
	z = [random.randint(N**(1/3.0) + 1, N**(1/2.0) - 1) for p in range(100000)]

def generateYSet():
	return [random.randint(0, N**(1/3.0)-1) for p in range(100000)]


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



def doAttack():
	ySet = generateYSet()
	zSet = generateZSet()

	zTimes = []
	yTimes = []

	for z in zSet:
		zTimes.append(getDecryptTime(z))
	
	for y in ySet:
		yTimes.append(getDecryptTime(y))

	print sum(zTimes)/len(zTimes)
	print
	print sum(yTimes)/len(yTimes)
doAttack()
