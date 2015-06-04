package rsa
import math._
import scala.annotation.tailrec
import scala.util.Random.nextInt
import rsa.keygen.RsaKeyGenerator

case class PublicKey(e: BigInt, n: BigInt){
	def encode(m: BigInt):BigInt = {
		m.modPow(e, n)
	}
}
case class PrivateKey(d: BigInt, n: BigInt){
	def decode(m: BigInt):BigInt = {
		m.modPow(d, n)
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