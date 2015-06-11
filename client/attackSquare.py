import random
import RSA
import connection_handler

def getSampleMessages(size):
	return [random.randint(100000, 100000000) for s in range(size)]

def doSquareAttack(n):
	r = RSA.generate_r(n)
	bits_to_solve = 32
	secretKey = '1'
	
	for i in range(1, bits_to_solve):
		sample_list = getSampleMessages(5000)
		
		M1 = [] # M1 is our additional reduction with 1
		M2 = []	    # M2 is our no reduction set with 1

		M3 = [] #M3 is our additional reduction set with 0
		M4 = []	    #M4 is our no reduction set with 0

		for sample in sample_list:
			
			if(RSA.CheckReduction(secretKey[0] + '1', sample, n, r)):
				M1.append(sample)
			else:
				M2.append(sample)
		
			if(RSA.CheckReduction(secretKey[0] + '0', sample, n, r)):
				M3.append(sample)
			else:
				M4.append(sample)
		

		M1_times = []
		M2_times = []
		M3_times = []
		M4_times = []
		for y in M1:
			M1_times.append(connection_handler.getDecryptTime(y))
		
			
		for x in M2:
			M2_times.append(connection_handler.getDecryptTime(x))

		
		for i in M3:
			M3_times.append(connection_handler.getDecryptTime(i))

		
		for j in M4:
			M4_times.append(connection_handler.getDecryptTime(j))

		
		average_M1 = sum(M1_times) / len(M1_times)

		
		average_M2 = sum(M2_times) / len(M2_times)

	
		average_M3 = sum(M3_times) / len(M3_times)

		
		average_M4 = sum(M4_times) / len(M4_times)

		
		if( abs(average_M1 - average_M2) > abs(average_M3 - average_M4)):
			print secretKey + '1'
		else:
			print secretKey + '0'
		
		
		print abs(average_M1 - average_M2)
	        print abs(average_M3 - average_M4)

		print  (abs(average_M1 - average_M2) -  abs(average_M3 - average_M4))
	#	print secretKey

doSquareAttack(connection_handler.getN())
