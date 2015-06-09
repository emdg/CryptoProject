

import akka.actor.{ActorSystem, Props}
import akka.io.IO
import spray.can.Http
import akka.pattern.ask
import akka.util.Timeout
import scala.concurrent.duration._
import rsa.routing.RestRouting
import util.Properties

object Boot extends App {
    implicit val system = ActorSystem("rsa-server")


    implicit val timeout = Timeout(5.seconds)
    val serviceActor = system.actorOf(Props(new RestRouting), name = "rest-routing")
	val port = Properties.envOrElse("PORT", "8080").toInt
    IO(Http) ? Http.Bind(serviceActor, "0.0.0.0", port = port)
}
