package rsa.keygen;
import java.math.BigInteger;
import java.util.Random;
public class RsaKeyGenerator {
   public BigInteger n;
   public BigInteger e;
   public BigInteger d;
   public RsaKeyGenerator(int size){
      Random rnd = new Random();
      BigInteger p = BigInteger.probablePrime(size/2,rnd);
      BigInteger q = p.nextProbablePrime();
      BigInteger n = p.multiply(q);
      BigInteger m = (p.subtract(BigInteger.ONE)).multiply(
         q.subtract(BigInteger.ONE));
      BigInteger e = RsaKeyGenerator.getCoprime(m);
      BigInteger d = e.modInverse(m);

      this.n = n;
      this.e = e;
      this.d = d;
   }

      
   public static BigInteger getCoprime(BigInteger m) {
      Random rnd = new Random();
      int length = m.bitLength()-1;
      BigInteger e = BigInteger.probablePrime(length,rnd);
      while (! (m.gcd(e)).equals(BigInteger.ONE) ) {
      	 e = BigInteger.probablePrime(length,rnd);
      }
      return e;
   }

}