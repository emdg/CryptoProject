import time
import random
import urllib

N = 7893364505739056694752315123831541284296639995794928392341494104718749447912465392151523342505244983911640199474005668676906821577143673549665195711897437

def generateZSet():
	return [random.randint(N**(1/3.0) + 1, N**(1/2.0) - 1) for p in range(200)]

def generateYSet():
	return [random.randint(0, N**(1/3.0 - 1)) for p in range(200)]


def sendGuess(message):
	start = time.clock()
	decrypt_url = "https://polar-coast-7047.herokuapp.com/decrypt?message={0}".format(message)
	response = urllib.urlopen(decrypt_url)
	end = time.clock()
	return end-start


def getDecryptTime(message):
	print 'getDecryptTime'
	times = [] 
	for i in range(1):
		times.append(sendGuess(message))
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
