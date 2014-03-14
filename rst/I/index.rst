##########
Einleitung
##########

.. epigraph::

   | |apostart| *Digital ist besser!* |apoend|

   -- *Marc-Uwe Kling, deutscher Kabarettist*


Motivation
==========

:dropcaps:`Die` Digitalisierung der modernen Konsumgesellschaft schreitet mehr
voran.  Wo es vor ein paar Jahren noch üblich war die eigene Filme-Sammlung im
Regal aufzubewahren, wird sie heute oft nur noch digital auf dem Home-Theater
PC, Smart-TV, PC oder anderen Endgeräten digital verwaltet und aufgezeichnet.
Das Aufkommen der digitalen HDTV-Sender und das große Angebot an Pay-TV Sendern
hat dem Trend der letzten Jahre nochmal frischen Auftrieb verpasst. Und hat man
mal einen Spielfilm verpasst, so kann dieser bequem über einen der vielen Online
Videorecorder-Dienste nachträglich bezogen werden. Es geht sogar soweit, dass
USB-Sticks [#f1]_ mit Hollywood Spielfilmen beworben und verkauft werden.

Zeichnet man viele Filme auf, oder digitalisiert seine Filmesammlung, so muss
man sich mit dem Pflegen der inhaltsbezogenen Metadaten auseinander setzen.
Das sind Metadaten wie Sie auf jeder DVD/Blu--Ray Hülle enthalten sind. Wo noch
im DVD/Blu--Ray Regal diese auf der DVD/Blu--Ray--Hülle zu finden waren, sind
sie nun nach dem digitalisieren nicht vorhanden und müssen vom Benutzer
nachträglich eingepflegt werden. Typische Metadaten bei Filmen sind der Titel,
Jahr, Beschreibung DVD-Cover und Genre.  Diese Metadaten sind bei Filmen im
unterschied zur Musik essentiell, da hierüber die Entscheidung getroffen wird ob
ein Film geschaut wird oder nicht.

Das Problem bei der Pflege der Metadaten im Videobereich besteht darin, dass es
hier keinen Standard gibt der sich durchgesetzt hat. Es gibt einerseits die
Möglichkeit bestimmte Metadaten in bestimmte Containerformate [#f2]_
integrieren, andererseits werden diese in separaten Dateien oder Datenbanken
gepflegt wie beim Windows Media Center oder Xbox Media Center. Ein weiteres
Problem das hinzukommt, sind die verschiedenen Onlinequellen von denen die
Metadaten bezogen werden. Hier werden von Anwendung zu Anwendung
unterschiedliche Quellen verwendet. Die Anzahl an der möglichen Onlinedienste
die Metadaten bereitstellen, ist hier praktisch *ungebrenzt*. Viele Anwendungen
können ihre Metadaten automatisch aus beziehen.  Je nach Anwendung kann es hier
im Hintergrund eine oder mehrere Bezugsquellen für Metadaten geben.

Ein weiteres Problem beim Bezug von Film--Metadaten ist, dass sich die
Online-Quellen stark in der Qualität und Umfang unterscheiden. Oft kommt noch
das Problem der Lokalisierung dazu.

Daraus resultierend sind über die Jahre sog. *Movie Manager* entstanden, die
einen bei der Pflege der Filmesammlung unterstützen sollen. Auch hier gibt es
nicht das *Tool der Wahl*. Es gibt wieder verschiedene Tools, die nur bestimmte
Metadaten Export-Formate verstehen, nur bestimmte Online Metadatenquellen
ansprechen können oder nur unter bestimmten Betriebssystemen verfügbar sind.

Projektziel
===========

Das Ziel dieser Arbeit ist es ein plugin basiertes System zu entwerfen, das die
verschiedenen Metadaten--Exportformate und Metadaten--Onlinequellen
zusammenführt und über eine *einheitliche Schnittstelle* anbietet. Der modulare
Aufbau soll gewährleisten, dass sich das System jederzeit um neue Onlinequellen
und Metadaten Exportmöglichkeiten erweitern lässt. Des weiteren soll es die
Möglichkeit geben, bereits vorhandene Datenbanken zu importieren, analisieren
und fehlerhafte oder fehlende Daten automatisiert zu korrigieren oder zu
ergänzen.

Zusammengefasst soll das System gut an die jeweilige *Umgebung* und
*Bedürfnisse* des Benutzers anpassbar sein.  Im Gegensatz zu den bereits
vorhandenen *Movie Management--Tools*, bei denen fehlende Metadaten manuell vom
Benutzer nachgepflegt werden müssen, soll das System mehr auf automatisierte
Verarbeitung ohne zutun des Benutzers ausgelegt sein.

.. rubric:: Footnotes

.. [#f1] http://www.amazon.de/Layer-Cake-Film-Flash-Drive/dp/B001Q3LOTQ
.. [#f2] http://encodingwissen.de/formatedschungel/container


.. http://www.vodprofessional.com/features/introduction-to-video-metadata/
.. https://www.videouniversity.com/articles/metadata-for-video/
