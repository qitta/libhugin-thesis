##########
Einleitung
##########

Motivation
==========

Heutzutage wird der Großteil unserer Medien digital konsumiert und verwaltet.
Ein großer Teil ist, neben der Musiksammlung, die private Filmsammlung. Nach dem
Digitalisieren müssen die Filmmetadaten, die in der Regel auf der DVD--Hülle
stehen, gepflegt werden. Hier bietet oft die Abspielsoftware die Möglichkeit,
die Metadaten über diverse Onlinequellen, wie beispielsweise über IMDb (siehe
:ref:`imdb`), zu beziehen.  Eine andere Möglichkeit, die private Filmsammlung zu
pflegen, bieten die sogenannten Movie--Metadaten--Manager. Diese Software ist
speziell für das Verwalten von Filmmetadaten konzipiert.

Bei der Pflege der Metadaten ist man jedoch auf die Rahmenbedingungen der
jeweiligen Software beschränkt. Nutzt man andererseits mehrere Applikationen um
eine Filmsammlung zu pflegen, kommt es oft zu Datenredundanzen, Inkonsistenzen
und anderen Problemen.

Um diese ,,Beschränkungen" der aktuellen Applikationen abzumildern, wurde vom
Autor das modulare Filmmetadaten Such- und Analysesystem *libhugin* entwickelt
:cite:`cpiechula`. Dieses System ist pluginbasierend und bietet somit dem
Benutzer die Möglichkeit, es an die eigenen Bedürfnisse anzupassen.

Diese Arbeit behandelt die Theorie zu dem vom Autor entwickelten modularen
Filmmetadaten Such- und Analysesystems *libhugin*. Des Weiteren sollen die
Metadaten der von *libhugin* verwendeten Metadatenquellen untersucht werden.

Ziel
====

Ziel der Arbeit ist es, die verwendeten Ansätze der Bibliothek zu evaluieren und
bisherige Annahmen über Filmmetadaten stichprobenartig anhand der in der
Projektarbeit implementierten Metadatenanbieter--Plugins zu untersuchen. Das
Ziel hier ist, die verwendeten Ansätze nochmals kritisch zu reflektieren und
mögliche bisher noch nicht bekannte Probleme zu identifizieren.

Neben der Evaluierung der Bibliothek, soll die Untersuchung der Metadaten soll
Aufschluß, über die weitere Vorgehensweise bei der Weiterentwicklung der
Bibliothek, geben.

Zusammengefasst soll der aktuelle Prototyp und bisherige Annahmen über die
Verteilung und die Probleme mit Metadaten untersucht werden.

Zielgruppe
==========

Zu der Zielgruppe gehören Personen, die an der Weiterentwicklung der Bibliothek
beteiligt sind, sowie auch Personen die sich einen Überblick über die
verwendeten Ansätze und Unterschiede bei den Metadatenquellen schaffen wollen.
