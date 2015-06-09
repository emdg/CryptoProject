package rsa.routing
import akka.actor.{Props, Actor}
import spray.routing.{Route, HttpService}
import rsa.clients.RSAClient
import rsa.core.RSACryptoActor
import rsa._


class RestRouting extends HttpService with Actor with PerRequestCreator {
	implicit def actorRefFactory = context
    val rsaService = context.actorOf(Props[RSAClient])

	def receive = runRoute(route)
	val route = {
        path("encrypt"){
            get {
                parameters('message) { message =>
                    handleMessage {
                        RSACryptRequest(message)
                    }
                }
            }
        }~ path("decrypt"){
            get {
                parameters("message") { message =>
                    handleMessage {
                        RSADecryptRequest(BigInt(message))
                    }
                }
            }
        } ~ path("publickey"){
            get {
                handleMessage {
                    GetPublicKey
                }
            }
        }
	}



    def handleMessage(message: RestMessage): Route = {
        ctx =>
        perRequest(ctx, Props(new RSACryptoActor(rsaService)), message)
    }

}
