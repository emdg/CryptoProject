import time
import urllib
import json


def getN():
	public_url = "http://localhost:8080/publickey"

	response = urllib.urlopen(public_url)
	data = json.loads(response.read())

	N = int(data['n'])

	return N

def sendGuess(message):
    decrypt_url = "http://localhost:8080/decrypt?message={0}".format(message)
    start = time.clock()
    response = urllib.urlopen(decrypt_url)
    end = time.clock()
    return end-start


def getDecryptTime(message):
    times = []
    for i in range(1):
        times.append(sendGuess(bin(message)[2:]))
    times.sort()
    return sum(times)/len(times)

