import time
import random
import urllib
import json
import RSA


public_url = "http://localhost:8080/publickey"

response = urllib.urlopen(public_url)
data = json.loads(response.read())

N = int(data['n'])

print N


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

def getSampleMessages(size):
    return [random.randint(100000, 10000000) for s in range(size)]


def doAttack(n):
    r = RSA.generate_r(n)
    bits_to_solve = 128
    secretKey = '1'

    for i in range(1, bits_to_solve):
        sample_list = getSampleMessages(1000)
        reduction_list = []
        no_reduction_list = []
        for sample in sample_list:
            if RSA.CheckReduction(secretKey, sample, n, r):
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
        if (average_with_reduction > average_without_reduction):
            secretKey += '1'
        else:
            secretKey += '0'
        print average_with_reduction - average_without_reduction
        print secretKey

doAttack(N)
