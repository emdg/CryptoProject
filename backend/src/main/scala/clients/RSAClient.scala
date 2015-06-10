package rsa.clients
import scala.annotation.tailrec
import akka.actor.Actor
import rsa.clients.RSAClient._
import scodec.bits._
import math._
import rsa.{Keygenerator, PublicKey, PrivateKey}


class RSAClient extends Actor {
	val (publicKey: PublicKey, privateKey:PrivateKey) = Keygenerator(32)

	def receive = {
		case Encrypt(message) =>
			val uncoded: BigInt = BigInt(message.getBytes)
			val encoded: BigInt = publicKey.encode(uncoded)
			sender ! Signature(encoded)
		case Decrypt(message) =>
			val uncoded: BigInt = privateKey.decode(message)
			sender ! Message(new String(uncoded.toByteArray.map(_.toChar)))
        case RequestPublicKey =>
            sender ! publicKey
        case _ =>
        	println("errosh")
	}
}

object RSAClient {
	case class Encrypt(message: String)
	case class Decrypt(message: BigInt)
	case class Signature(message: BigInt)
	case class Message(message: String)
    case object RequestPublicKey
    case class PublicKeyOut(e: BigInt, n: BigInt)
}



