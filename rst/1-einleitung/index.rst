##########
Einleitung
##########

Motivation
==========

Heutzutage wird der Großteil unserer Medien digital konsumiert und verwaltet.
Ein großer Teil ist, neben der Musiksammlung, die private Filmsammlung. Nach dem
Digitalisieren müssen die Filmmetadaten, die in der Regal auf der DVD--Hülle
stehen, gepflegt werden. Hier bietet oft die Abspielsoftware die Möglichkeit, die
Metadaten über diverse Onlinequellen, wie beispielsweise über IMDb, zu beziehen.
Eine andere Möglichkeit, die private Filmsammlung zu pflegen, bieten die
sogenannten Movie--Metadaten--Manager. Diese Software ist speziell für das
Verwalten von Filmmetadaten konzipiert.

Bei der Pflege der Metadaten ist man jedoch auf die Rahmenbedingungen der
jeweiligen Software beschränkt. Nutzt man mehrere Applikationen um eine
Filmsammlung zu pflegen, kommt es oft zu Datenredundanzen, Inkonsistenzen und
anderen Problemen.

Um die ,,Beschränkungen" der aktuellen Applikationen abzumildern, wurde vom
Autor das modulare Filmmetadaten Such- und Analysesystem *libhugin* entwickelt
:cite:`cpiechula`. Dieses System ist pluginbasierend und bietet somit dem
Benutzer die Möglichkeit es an die eigenen Bedürfnisse anzupassen.

Diese Arbeit behandelt die Theorie zu dem vom Autor entwickelten modularen
Filmmetadaten Such- und Analysesystems *libhugin*. Es werden die verwendeten
Ansätze und Algorithmen erklärt und Alternativansätze aufgezeigt.


Ziel
====

Ziel der Arbeit ist es, die verwendeten Ansätze der Bibliothek zu evaluieren und
bisherige Annahmen über Filmmetadaten stichprobenartig anhand der in der
Projektarbeit implementierten Metadatenanbieter--Plugins zu untersuchen. Die
Untersuchung der Metadaten soll Aufschluß, über die weitere Vorgehensweise bei
der Weiterentwicklung der Bibliothek, geben.

Des Weiteren geht es darum die verwendete Algorithmik als Entwicker nochmals zu
beleuchten und Verbesserungen abzuleiten oder Probleme zu beheben.

Zielgruppe
==========

Zu der Zielgruppe gehören Personen, die an der Weiterentwicklung der Bibliothek
beteiligt sind, sowie auch Personen die sich einen Überblick über die
verwendeten Ansätze und Unterschiede bei den Metadatenquellen schaffen wollen.
