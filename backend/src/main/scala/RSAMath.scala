package rsa;
object RSAMath {
	def find_r(n:BigInt, radix: BigInt = 2):BigInt = {
		def find_r_internal(n:BigInt, radix:BigInt, k:Int):BigInt = {
			if (radix.pow(k)> n)
				radix.pow(k)			
			else
				find_r_internal(n, radix, k+1)
		}

		find_r_internal(n, radix, 0)
	}
	
	def monPro(a:BigInt, b:BigInt, n:BigInt):BigInt = {
		val r = find_r(n)
		val r_inv = r.modInverse(n)
		val n_prime = (r * r_inv - 1) / n

		val t = a * b
		val m = (t * n_prime) % r
		val u = (t + m * n) / r
		if (u >= n){
			u - n
		}
		else{
			u
		}
	}





	def monProSleepy(a:BigInt, b:BigInt, n:BigInt):BigInt = {
		val r = find_r(n)
		val r_inv = r.modInverse(n)
		val n_prime = (r * r_inv - 1) / n

		val t = a * b
		val m = (t * n_prime) % r
		val u = (t + m * n) / r
		if (u >= n){
			Thread sleep 2
			u - n
		}
		else{
			u
		}
	}


	def monExp(M:BigInt, e:BigInt, n:BigInt):BigInt = {
		val r = find_r(n)
		val r_inv = r.modInverse(n)
		val n_prime = (r*r_inv - 1) / n
		val M_bar = (M * r) % n
		var x_bar = r % n
		for (i <- e.bitLength to 0 by - 1){
			x_bar = monPro(x_bar, x_bar, n)
			if (e.testBit(i)){
				x_bar = monPro(M_bar, x_bar, n)
			}
		}
		monPro(x_bar, 1, n)
	}


	def monExpSleepy(M:BigInt, e:BigInt, n:BigInt):BigInt = {
		val r = find_r(n)
		val r_inv = r.modInverse(n)
		val n_prime = (r*r_inv - 1) / n
		val M_bar = (M * r) % n
		var x_bar = r % n
		for (i <- e.bitLength to 0 by - 1){
			x_bar = monProSleepy(x_bar, x_bar, n)
			if (e.testBit(i)){
				x_bar = monProSleepy(M_bar, x_bar, n)
			}
		}
		monProSleepy(x_bar, 1, n)
	}
}