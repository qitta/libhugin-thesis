###############
Zusammenfassung
###############

Verwendete Algorithmik
======================

Die Evaluation der Bibliothek und der Metadaten konnte die bisher getroffenen
Annahmen bestätigen. Das Downloadverhalten skaliert über mehrere Threads gut.
Die Algorithmik für den Zeichenkettenvergleich wurde angepasst, um auch
Filmtitel mit nachziehenden Artikeln zu finden. Hier skaliert der Algorithmus
basierend auf der Damerau--Levenshtein--Distanz weiterhin gut (siehe Kabitel
:ref:`standardsuche` Abbildung :num:`fig-finalstringcompare`). Die zusätzliche
Gewichtung vom Jahr, erwies sich mit der kleinen Testdatenmenge als
wirkungsvoll (siehe Kapitel :ref:`standardsuche`, Abbildung :num:`fig-ratingstr`).

Der verwendete Ansatz beim ,,Lookup"--Mode funktioniert ebenso wkirkungsvoll.
Dieser Ansatz wurde zum Normalisieren der Filmtitel für die
Metadaten--Stichprobe verwendet.

Weitere Ansätze, wie die Implementierung der Unschärfesuche, können nur schwer
beurteilt werden. Hier gibt es je falsch geschriebenen Titel Toleranzen. Im
Grunde kommt es hier auf die Genauigkeit der Suchmaschine an. Kleine Stichproben
in der Projektarbeit zeigten eine hohe Erfolgsquote (siehe :cite:`cpiechula`,
Kapitel 7.4 Demoanwendungen).

Die verwendeten Algorithmen bei den Plugins greifen aktuell zum Teil auf externe
Tools zurück, wie beispielsweise das *FileTypeAnalyze* Plugin. Hier wären in
naher Zukunft Ansätze, die sich mehr in die Bibliothek integrieren, wünschenswert.


Untersuchungen der Metadaten
============================

Die Annahmen über die Metadaten wurden mit einer Stichprobe von 2500 Filmen fast
vollständig bestätigt. Das Genrespektrum sowie Gewichtung bei den Onlinequellen
ist hier sehr unterschiedlich (siehe Kapitel :ref:`genreinformationen`,
Abbildung :num:`fig-genres`). Des Weiteren variiert der Detailgrad des Genres pro
Film, je nach Datenquellen mehr oder weniger stark. Durchschnittlich kommt es hier
zu Abweichungen von mehr als einem Genre (siehe Kapitel :ref:`genreinformationen`,
Abbildung :num:`fig-genre-avg`).

Die Annahme und persönliche Erfahrung des Autors, dass es hier Differenzen beim
Erscheinungsjahr gibt, wurden bestätigt (siehe Kapitel :ref:`yeardiff`,
Abbildung :num:`fig-yeardiff`).

Die Annahme, dass die Metadaten lückenhaft gepflegt sind, was die
Grundproblematik der Metadatenbeschaffung unterstreicht, wurde anhand der
Stichprobe bestätigt (siehe Kapitel :ref:`unvoll`, Abbildung
:num:`fig-completeness`).

Die Annahme, dass sich die Filmbewertungen je nach Plattform stark unterscheiden,
konnte nicht direkt bestätigt werden (siehe :ref:`ratingkapitel`, Abbildung
:num:`fig-rating`). Hier wurde ein Test mit Metadaten der drei API--Provider
durchgeführt, welcher zeigt, dass die Bewertung bei allen drei Providern im
Schnitt fast identisch ist. Lediglich die Verteilung variiert hier leicht, es
ist jedoch bei allen drei Anbietern eine ähnliche Verteilung zu beobachten
(siehe Kapitel :ref:`ratingkapitel`, Abbildung :num:`fig-rating`).


Aktuelle Probleme
=================

Bei den Auswertungen und nochmaligem Reflektieren der verwendeten Algorithmen
wurden Probleme aufgedeckt, die zum aktuellen Zeitpunkt des *libhugin*--Prototyps
nicht bekannt waren.

Die problematische OFDb--Provider API, welche bereits während der Entwicklung
auf einen damals allen Anschein nach funktionierenden Mirror zugegriffen hat,
macht weiterhin Probleme. Hier zeigt das Erheben der Testmetadaten mit der
*libhugin--harvest*--Bibliothek, dass das fehlerhafte Verhalten weiterhin
besteht (siehe Kapitel :ref:`unvoll`, Abbildung :num:`fig-completeness`). Hier
werden Filme häufig ohne Inhaltsbeschreibung zurückgegeben.  Des Weiteren
wurde festgestellt, dass die API je nach Tageszeit und Serverauslastung, im
Vergleich zu den anderen Providern, instabil ist (siehe Kapitel
:ref:`timeoutverhalten`, Abbildung :num:`fig-timeout`).

Tests der Geschwindigkeit von der *libhugin--harvest*--Bibliothek haben gezeigt,
dass es hier bei den Providern ohne API Performanceunterschiede zu den Providern
mit API gibt (siehe Kapitel :ref:`antwortzeiten`, Abbildung
:num:`fig-hugindownload`, Abbildung :num:`fig-hugindownload-cache`). Als Grund
wird hier das im Vergleich zum API--Provider aufwendigere Parsen der kompletten
HTTP--Response vermutet. Hier wird aktuell die ``BeautifulSoup``--Bibliothek
verwendet. Eine Änderung des internen Parsers hat die Performance weiterhin
verschlechtert. Hier wäre es wünschenswert, andere Ansätze zu finden, die diesen
Vorgang performanter ausführen.

Weiterhin hat sich gezeigt, dass hier bei zwei Providern die Metadaten in
keinem einheitlichen Encoding zurückgeliefert werden. Hier gab es Probleme mit
den Umlauten beim Genre ,,Komödie".

Ausblick
========

Zusammengefasst kann gesagt werden, dass mit dem *libhugin*--Prototyp das
angesetzte Vorhaben, eine andere Herangehensweise beim Beschaffen der Metadaten,
im Vergleich zu den bisherigen Tools, gut umsetzt wurde. Aktuell gibt es jedoch
noch vereinzelt Probleme, wie beispielsweise das oben genannte Problem
mit dem Encoding oder auch die Geschwindigkeitseinbußen bei der Nutzung eines
Providers ohne API.

Wie bereits in der Zusammenfassung der Projekarbeit (siehe :cite:`cpiechula`, 8
Zusammenfassung) zur Implementierung der Bibliothek erwähnt, wäre es laut Autor
sinnvoll, die Bibliothek weiter zu ,,verschlanken". Hier wird aktuell die Idee
verfolgt, die ,,zweigeteilte" Bibliothek aus dem *libhugin--harvest* und
*libhugin-analyze* Teil komplett separat zu entwickeln.

Generell sollten in Zukunft mehrere Provider implementiert werden, um die
bisherigen Erkenntnisse mit einem größeren Onlinequellenspektrum zu
bestätigen.  Hier sollte bei weiteren Tests neben deutschsprachigen auch mehr
Wert auf fremdsprachige Metadatenquellen gelegt werden.
