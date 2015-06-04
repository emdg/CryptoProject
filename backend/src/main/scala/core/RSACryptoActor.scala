package rsa.core
import akka.actor.{ActorRef, Actor}
import rsa.clients.RSAClient
import rsa._
import rsa.Keygenerator
import rsa.clients.RSAClient._

class RSACryptoActor(rsaService: ActorRef) extends Actor {

	def receive = {
		case RSACryptRequest(message) =>
		rsaService ! Encrypt(message)
		context.become(waitingResponses)
		case RSADecryptRequest(message) =>
		rsaService ! Decrypt(message)
		context.become(waitingResponses)

	}



	def waitingResponses: Receive = {
		case Signature(message) =>
		context.parent ! RSASignature(message)
		case Message(message) =>
		context.parent ! RSADecrypted(message)
	}
}