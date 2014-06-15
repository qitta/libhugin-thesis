###############
Zusammenfassung
###############

Verwendete Algorithmik
======================

Die Evaluation der Bibliothek und der Metadaten konnte die bisher getroffenen
Annahmen bestätigen. Das Downloadverhalten skaliert über mehrere Thread gut. Die
Algorithmik für den Zeichenkettenvergleich wurde angepasst um auch Filmtitel mit
nachziehenden Artikeln zu finden. Hier skaliert der Algorithmus basierend auf
der Damerau--Levenshtein--Distanz weiterhin sehr gut. Die zusätzliche
Gewichtung vom Jahr erwies sich mit der kleinen Testdatenmenge als wirkungsvoll.

Der verwendete Ansatz beim ,,Lookup"--Mode funktioniert ebenso wkirkungsvoll.
Dieser Ansatz wurde zum normalisieren der Filmtitel für die
Metadaten--Stichprobe verwendet.

Weitere Ansätze wie die Implementierung der Unschärfesuche, können nur schwer
beurteilt werden. Hier gibt es je Titel Toleranzen, im Grunde kommt es hier auf
die Genauigkeit der Suchmaschine an. Kleine Stichproben in der Projektarbeit
zeigten einen hohen Wirkungsgrad.

Die Normalisierung des Genre funktioniert Momentan nur mit den API--Providern
über statische Tabellen. Hier wären noch andere Ansätze beziehungsweise Ideen
wünschenswert.

Die verwendeten Algorithmen bei den Plugins greifen aktuell zum Teil auf externe
Tools zurück, wie beispielsweise das *FileTypeAnalyze* Plugin. Hier wären in
naher Zukunft Ansätze die sich mehr in die Bibliothek integrieren wünschenswert.


Untersuchungen der Metadaten
============================

Die Annahmen über die Metadaten wurden mit einer Stichprobe von 2500 Filmen fast
vollständig bestätigt. Das Genrespektrum sowie Gewichtung bei den Onlinequellen
ist hier sehr unterschiedlich. Desweitere variiert der Detailgrad des Genres pro
Film je nach Datenquellen mehr oder weniger stark. Durchschnittlich kommt hier
zu Abweichungen von mehr als einem Genre.

Die Annahme und persönliche Erfahrung des Autors, dass es Hier Differenzen beim
Erscheinungsjahr gibt, wurden bestätigt.

Die Annahme, dass die Metadaten sehr lückenhaft gepflegt sind, was die
Grundproblematik der Metadatenbeschaffung unterstreicht, wurde anhand der
Stichprobe von ca. 2500 Testmetadaten pro Film bestätigt.

Die Annahme, dass das die Bewertungmoral je nach Plattform sich stark
unterscheidet, konnte nicht bestätigt werden. Hier wurde ein Test mit Metadaten
der drei API--Provider durchegführt, welcher zeigt, dass das Genre bei allen
drei Providern im Schnitt fast identisch ist. Lediglich die Verteilung variiert
hier leicht, es ist jedoch bei allen drei Anbietern nahezu eine Standardverteilung.


Aktuelle Probleme
=================

Bei den Auswertungen und nochmaligen Reflektieren der verwendeten Algorithmen
wurden Probleme aufgedeckt die zum aktuellen Stand des *libhugin* Prototyps
nicht bekannt waren.

Die Problematisch OFDb--Provider API, welche bereits während der Entwicklung auf
einen damals allen Anschein nach funktionierend Mirror, macht weiterhin
Probleme. Hier zeigt das Erheben der Testmetadaten mit der
*libhugin--harvest*--Bibliothek, dass das bei den fehlerhafte Verhalten
weiterhin besteht. Hier werden oft Filme einfach ohne
Inhaltsbeschreibung zurückgegeben. Desweiteren wurde festgestellt, dass die API
je nach Tageszeit und Serverauslastung, im Vergleich zu den anderen Providern,
instabil ist.

Tests der Geschwindigkeit von der *libhugin--harvest*--Bibliothek haben gezeigt,
dass es hier bei den Provider ohne API Performanceunterschiede zu den Providern
mit API gibt. Als Grund wird hier das im Vergleich zum API--Provider
aufwendigere Parsen der kompletten HTTP--Response vermutet. Hier wird aktuell
die ``BeautifulSoup``--Bibliothek verwendet. Eine Änderung des internen Parser
hat die Performance weiterhin verschlechtert. Hier wäre es wünschenswerte andere
Ansätze zu finden, die diesen Vorgang performanter hinbekommen.

Weiterhin hat sich gezeigt, dass hier bei manchen Providern die Metadaten in
keinem einheitlichen Encoding zurückgeliefert werden. Hier gab es Probleme mit
den Umlauten beim Genre ,,Komödie".

Ausblick
========

Zusammengefasst kann gesagt werden, dass die Bibliothek das angesetzte Vorhaben,
eine andere Herangehensweise beim Beschaffen der Metadaten im Vergleich zu den
bisherigen Tools, gut umsetzt wurde. Aktuell gibt es jedoch noch an ein paar
Stellen Probleme wie beispielsweise dem oben genannte Problem mit dem Encoding,
oder auch die Performanceeinbußen bei der Nutzung eines Providers ohne API.

Wie bereits in der Zusammenfassung der Projekarbeit zur Implementierung der
Bibliothek erwähnt, wäre es laut Auto sinnvoll die Bibliothek weiterhin zu
,,entschlacken". Hier wird aktuell die Idee verfolgt die ,,zweigeteilte"
Bibliothek aus dem *libhugin--harvest* und *libhugin-analyze* Teil komplett
separat zu entwickeln.

Generell sollten hier in Zukunft mehre Provider implementiert werden um die
bisherigen Erkentnisse, mit einem größeren Onlinequellenspektrum, zu bestätigen.
Hier sollte bei weiteren Tests neben deutschsprachigen auch mehr Wert auf
fremdsprachige Metadatenquellen gelegt werden.
