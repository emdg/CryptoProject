package rsa
trait RestMessage

case class Error(message: String)

case class Validation(message: String)


case class RSACryptRequest(message: String) extends RestMessage
case class RSASignature(signature: BigInt) extends RestMessage
case class RSADecryptRequest(crypted: BigInt) extends RestMessage
case class RSADecrypted(message:String) extends RestMessage