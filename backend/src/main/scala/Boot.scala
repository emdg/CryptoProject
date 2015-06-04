

import akka.actor.{ActorSystem, Props}
import akka.io.IO
import spray.can.Http
import akka.pattern.ask
import akka.util.Timeout
import scala.concurrent.duration._
import rsa.routing.RestRouting
object Boot extends App {
    implicit val system = ActorSystem("rsa-server")


    implicit val timeout = Timeout(5.seconds)
    val serviceActor = system.actorOf(Props(new RestRouting), name = "rest-routing")

    IO(Http) ? Http.Bind(serviceActor, "localhost", port = 38080)
}
