import random
import RSA
import connection_handler


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
            if RSA.CheckReduction(secretKey + '1', sample, n, r):
                reduction_list.append(sample)
            else:
                no_reduction_list.append(sample)

        no_reduction_times = []
        reduction_times = []

        for y in no_reduction_list:
            no_reduction_times.append(connection_handler.getDecryptTime(y))
        for x in reduction_list:
            reduction_times.append(connection_handler.getDecryptTime(x))

        average_with_reduction = sum(reduction_times) / len(reduction_times)
        average_without_reduction = sum(no_reduction_times)/len(no_reduction_times)
        if (average_with_reduction > average_without_reduction):
            secretKey += '1'
        else:
            secretKey += '0'
        print average_with_reduction - average_without_reduction
        print secretKey

doAttack(connection_handler.getN())
