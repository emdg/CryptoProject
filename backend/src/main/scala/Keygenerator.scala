package rsa
import math._
import scala.annotation.tailrec
import scala.util.Random.nextInt
import rsa.keygen.RsaKeyGenerator

case class PublicKey(e: BigInt, n: BigInt){
	import rsa.RSAMath._
	def encode(m: BigInt):BigInt = {
		monExp(m, e, n)
	}
}
case class PrivateKey(d: BigInt, n: BigInt){
	import rsa.RSAMath._
	def decode(m: BigInt):BigInt = {
		monExp(m, d, n)
	}
}

object Keygenerator{

	def apply(length: Int) = {

		val kgen = new RsaKeyGenerator(length)
		val publicKey = PublicKey(kgen.e, kgen.n)
		val privateKey = PrivateKey(kgen.d, kgen.n)
		(publicKey, privateKey)
	}

}