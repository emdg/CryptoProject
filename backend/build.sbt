name := "RSA Server"

version := "0.1"

lazy val root = (project in file(".")).enablePlugins(JavaAppPackaging)

resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots/"

scalacOptions := Seq("-unchecked", "-deprecation", "-encoding", "utf8")

libraryDependencies ++= {
  val akkaV = "2.3.11"
  val sprayV = "1.3.1"
  Seq(
    "io.spray"            %%  "spray-can"     % sprayV,
    "io.spray"            %%  "spray-routing" % sprayV,
    "org.json4s" %% "json4s-native" % "3.2.11",
	"org.typelevel" %% "scodec-bits" % "1.1.0-SNAPSHOT",
    "io.spray"            %%  "spray-testkit" % sprayV  % "test",
    "com.typesafe.akka"   %%  "akka-actor"    % akkaV
    )
}
