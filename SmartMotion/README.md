Projektkurs Informatik
Herr Tohang und Herr Kaiser
Eine Projektdokumentation zu "Smart Motion" von Malte und Jonas 2023

Inhaltsaufbau
	1. Hintergrund
	2. Problemstellung
	3. Materialliste
	4. Aufteilung
	5. Danksagung

Hintergrund

Wir sind Malte und Jonas, Schüler der Liebfrauenschule Mülhausen und belegen den Projektkurs Informatik an unserer Schule, in dem wir uns dazu entschieden haben, an der World Robotics Olympiade teilzunehmen (World Robot Olympiad - Internationaler Roboterwettbewerb für Mädchen und Jungen). Da diese unterschiedliche Wettbewerbskategorien beinhaltet und Malte später einmal in der Automobilbranche arbeiten möchte, ist die Kategorie "Future Engineers" für uns die optimale Kategorie um schon einmal für den spätere Beruf einen groben Einblick zu erhalten. Im Wettbewerb geht es darum ein eigenes Roboterauto zu kreieren, welches in einer vorgegebenen Umgebung schnellstmöglich Hindernisse umfahren soll (WRO Future Engineers Kategorie - Baue ein autonom fahrendes Roboterauto (worldrobotolympiad.de)). 

Problemstellung

Die Aufgabe besteht darin, einen Roboter autonom in einem 3*3 Meter großen weißen Feld fahren zu lassen. Auf dieser weißen Fläche sind vor den Ecken jeweils orange und blaue Linien eingezeichnet, die für uns eine Möglichkeit bieten, dem Roboter durch einen Farbsensor zu signalisieren, ob er jetzt links oder rechts abbiegen muss. In der Mitte des Feldes ist zudem auch eine Begrenzung, die wie die äußere Begrenzung ebenso dunkel gefärbt und gleich hoch (etwa 10 cm) ist. Sie darf nicht berührt werden. Es gibt zwei Wettbewerbsrunden. In der ersten soll der Roboter das Feld einmal innerhalb von 3 Minuten abfahren. In der zweiten Runde stehen in dem Feld zudem rote und grüne Hindernisse. Die roten Hindernisse sollen rechts herum umfahren werden und die Grünen links herum. Das Ziel ist, dass das Roboterauto möglichst wenig falsch macht und uns damit möglichst viele Punkte einbringt. Das ganze Regelwerk findet sich auf der Webseite der WRO (siehe Links oben).

Materialliste

Folgende elektronische Bauteile sind bzw. werden noch im "Smart Motion"-Roboterauto verbaut: 

	- Raspberry Pi 4b (Steuerung)
	- Jumper-Kabel (selbsterklärend)
	- USB Kamera (zur Erkennung der roten und grünen Blöcke)
	- Ultraschallsensor (um die Distanz zu den Blöcken zu testen)
	- Schrittmotor (zum Antrieb des Roboters)
	- Dual H Bridge (zur Kontrolle des Motors und der dementsprechenden Spannung)
	- Servomotor (zum Antrieb des Autos)


Folgende elektronische Bauteile sind bzw. werden noch im "Smart Motion"-Roboterauto verbaut:
	- 3D gedruckte Karosserie: das Modell ist von Thingiverse und für den Bauraum eines Prusa Mini+ herunter skaliert (Thing files for 2013 Charger Race Car by petropixel - Thingiverse)
	- Grundplatte (um alles zu befestigen)
	- Klemmbausteine zum Bau eines Differentials
	- Räder (Klemmbauteile)

Aufteilung

Damit eine Projektarbeit funktioniert, muss diese natürlich aufgeteilt werden. Wir haben uns dazu entschieden, dass Malte sich insbesondere auf die Programmierung und die damit verbundene Sensorik konzentriert. Jonas übernimmt schwerpunktmäßig den 3D Druck der Karosserie sowie das Github-Repository und die Verkabelung einzelner Sensormodule. Allerdings sollte hier erwähnt werden, dass das keine starre Zuordnung ist und die Übergänge im Rahmen der Teamarbeit natürlich fließend sind. 

Probleme

Zwischendurch entstanden immer wieder erneut Probleme, die vorallem die Lieferzeiten einiger Hardware betrafen. Bugs in der Software konnten jederzeit behoben werden, auch wenn dies etwas Zeit erforderte. Womit keiner von uns beiden rechnen konnte war, dass uns genau am 01.06, zwei Tage vor dem Wettberwerb, ein entscheidener Teil unserer Hardware durch einen Kurzschluss durchgebrannt ist (Farbsensor TCS3200). Da es nicht mehr möglich ist, dieses Teil in Kürze erneut zu kaufen, mussten wir kurzerhand unsere Strategie umdenken und leider den Kompromisseingehen, die Kamera statt für die Objekterkennung auf die Farberkennung des Bodens zu verwenden.

Fortschritt

Am Anfang des Halbjahres standen wir vor der Frage, ob wir ein autonom fahrendes Auto bauen wollen oder doch an einem anderen Wettbewerb teilnehmen. Da wir beide aber Fans von Kraftfahrzeugen sind, haben wir uns für dieses Projekt entschieden. 
Zuerst stand die Frage im Raum, auf welches System man setzt: Lego oder ein alternatives.
Wir sind zu dem Schluss gekommen, dass Lego zwar gute Möglichkeiten bietet, eine Karosserie für ein Auto zu bauen, die EV3 MINDSTORMS jedoch einen zu geringen Funktionsumfang bieten, vorallem durch die eigenen Stecker.
Letztendlich haben wir uns dafür entschieden, dass wir die Karosserie aus Lego bauen, für die Hardware zum Fahren jedoch auf ein anderes System setzen. 
Inspiriert von unsrer Recherche hatten wir die Idee, eine Kamera als Objekterkennung zu benutzen, für Abstand einen Ultraschallsensor und für die Erkennung der Striche auf dem Spielfels einen Farbsensor.
So konnten wir unsere Möglichkeiten nur auf einem Raspberry PI umsetzen, da ein Arduino bspw. nicht die Möglichkeit bietet, eine Python Bibliothek zu benutzen.
Nachdem wir die Teile zusammengesucht hatten und bestellt hatten, hieß es ersteinmal warten. Diese Zeit nutzen wir jedoch, um schon die Anfänge für unser Projekt zu setzen. 
Während Jonas mit dem Bau der Karosserie anfing, kümmerte ich mich um die Software. Nach Überlegungen, wie das Script aufgebaut sein könnte und was es leisten muss, stand folgendes fest:

Das Script muss:
- Die Farben auf dem Boden erkennen
- Die Distanz von Objekten messen 
- über die Kamera die Roten und blauen Klötze erkennen 
- den Motor ansteuern 
- den Servo zum Lenken ansteuern 

Angefangen wurde mit der Objekterkennung, da die anderen Teile (unter anderem auch der RPI) noch nicht angekommen waren. zum Erkennen der Farben wurde die Bibliothek "OpenCV" verwendet, und das Script wurde in Python geschrieben.
Durch viel ausprobieren und der Hilfe von Seiten wie bspw. Stackoverflow stand nach einer Woche das Script, welches erfolgreich die Farben rot und Grün hervorheben konnte. 
Als nach einiger Zeit dann die Teile ankamen, stellte sich ein Problem heraus: OpenCV auf dem RPI zu installieren ist nicht so einfach wie man es sich denkt.
Es dauerte tatsächlich über 2 Wochen, bis die Bibliothek auf dem RPI installiert war, und man das Script endlich lief.
Jonas hatte zu diesem Zeitpunkt das Chassis schon gut ausgebaut, unter anderem war auch schon das Differential verbaut.
Über die Zeit hinweg bauten wir immer weiter, das Script wurde größer, unser Auto konnte immer mehr, und schließlich waren wir fertig.
Zwischendurch, als wir das Auto testen wollte, entstanden jedoch immer noch Fehler. Objekte wurden nicht erkannt, die Stanzmessung spielte regelmäßig verrückt, der Farbsensor erkannte alle Farben ausser denen, die er sollte. All dies konnte über die Zeit behoben werden, bis zum Donnerstag vor dem Wettbewerb.
Eigentlich sollte das Auto eine seiner Testrunden absolvieren, jedoch fing es auf einmal an zu rauchen weshalb die Stromversorgung sofort unterbrochen wurde.
In Angst, es könne sich um den Motor handeln, wurde jede einzelne Komponente getestet, und wie sich herausstellte, war es der Farbsensor, welcher durchgebrannt ist (siehe Bild). Dies warf uns in unserem Zeitplan Wochen zurück, und auf die Schnelle lies sich kein neuer Farbsensor bestellen. Wir entschieden uns, dass die Kamera absofort nun die Farben auf dem Boden kontrollieren muss, um dann jeweils die Lenkbewegungen auszuführen. So wird es uns als nicht möglich sein, an der ZWeiten Runde des Wettbwerbs teilzunehmen, da jede weitere Kamera das maximale Gesamtgewicht überschreiten würde (Gemessen: 1490g).
Nichts desto trotz versuchen wir trotzdem, unser bestes zu geben, auch, wenn das was es könnte sicherlich mehr wäre.

Danksagung

Zum Abschluss bedanken wir uns herzlich bei Herrn Kaiser und Herrn Tohang für die Möglichkeit am Projektkurs teilnehmen zu können und dafür bis 16 Uhr in der Schule verbleiben zu dürfen. Ein weiterer Dank geht an dieser Stelle an die WRO, die ein solches Projekt für Schüler anbietet.
Weiteres Lob geht an Herrn Zanders, welcher sich bereit erklärte uns Schüler während seiner Stunde an unserem Projekt weiterarbeiten zu lassen.
