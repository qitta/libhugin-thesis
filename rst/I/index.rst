##########
Einleitung
##########

.. epigraph::

   | |apostart| *Digital ist besser!* |apoend|

   -- *Marc-Uwe Kling, deutscher Kabarettist*


Motivation
==========

:dropcaps:`Die` Digitalisierung der modernen Konsumgesellschaft schreitet immer
weiter voran. Wo es vor ein paar Jahren noch üblich war die eigene Filmesammlung
im Regal aufzubewahren, wird sie heute oft nur noch digital auf dem
Home--Theater PC [#f0]_, Smart--TV, PC oder anderen Endgeräten digital
aufgezeichnet und verwaltet. Das Aufkommen der digitalen HDTV-Sender und das
große Angebot an Pay-TV Sendern hat dem Trend der letzten Jahre nochmal frischen
Auftrieb verpasst. Und hat man mal einen Spielfilm verpasst, so kann dieser
bequem über einen der vielen Online Videorecorder-Dienste nachträglich bezogen
werden. Es geht sogar soweit, dass USB-Sticks [#f1]_ mit Hollywood Spielfilmen
beworben und verkauft werden.

Zeichnet man viele Filme auf oder digitalisiert seine Filmesammlung, so muss
man sich mit dem Pflegen der inhaltsbezogenen Metadaten auseinander setzen.
Das sind Metadaten, wie sie auf jeder DVD/BD--Hülle enthalten sind. Wo noch
im DVD/BD--Regal diese auf der DVD/BD--Hülle zu finden waren, sind
sie nun nach dem digitalisieren nicht vorhanden und müssen vom Benutzer
nachträglich eingepflegt werden. Typische Metadaten bei Filmen sind der Titel,
Jahr, Inhaltsbeschreibung, Cover und Genre.  Diese Metadaten sind bei Filmen im
unterschied zur Musik essentiell, da hierüber die Entscheidung getroffen wird ob
ein Film geschaut wird oder nicht.

Die Metadaten werden in der Regel über Onlineportale wie beispielsweise die
Internet Movie Database (IMDb) bezogen. Die Anzahl der möglichen Onlinedienste
die Metadaten bereitstellen, ist hier praktisch *ungebrenzt*. Viele Anwendungen
wie das Windows Media Center oder das Xbox Media Center (XBMC) können ihre
Metadaten automatisch aus dem Internet beziehen. Je nach Anwendung kann es hier
im Hintergrund eine oder mehrere Bezugsquellen für Metadaten geben.

Ein Problem bei der Pflege der Metadaten im Videobereich ist, dass es hier
keinen Standard gibt der sich durchgesetzt hat. Es gibt einerseits die
Möglichkeit bestimmte Metadaten in bestimmte Containerformate [#f2]_ zu
integrieren, andererseits werden diese in separaten Dateien (dvdid.xml--Format
[#f3]_ beim Windows Media Center, movie.nfo--Format [#f4]_, beim Xbox Media
Center) oder Datenbanken der jeweiligen Abspiel--/Verwaltungssoftware gepflegt.

oder Xbox Media Center. Ein weiteres Problem das hinzukommt, sind die
verschiedenen Onlinequellen von denen die Metadaten bezogen werden. Hier werden
von Anwendung zu Anwendung unterschiedliche Quellen verwendet, die je nach
Filmesammlung gut oder weniger gut geeignet sind.

Ein weiteres Problem beim Bezug von Film--Metadaten ist, dass sich die
Onlinequellen stark in der Qualität, Umfang und Art der angebotenen Metadaten
unterscheiden. Hier gibt es Quellen die einerseits gute hochauflösende Cover
anbieten, aber keine Inhaltsbeschreibung oder Dienste die ausführliche
Inhaltsbeschreibungen liefern, jedoch keine Bilddaten wie Cover oder Fanart. Oft
kommt hier noch das Problem der Lokalisierung hinzu.

Daraus resultierend sind über die Jahre sog. *Movie Manager* entstanden, die
einen bei der Pflege der Filmesammlung unterstützen sollen. Auch hier gibt es
nicht das *Tool der Wahl*, die Problematik ist weiterhin vorhanden. Es gibt
wieder verschiedene Tools, die nur bestimmte Metadaten Export-Formate verstehen,
nur bestimmte Online Metadatenquellen ansprechen können oder auch nur unter
bestimmten Betriebssystemen verfügbar sind.

Projektziel
===========

Das Ziel dieser Arbeit ist es ein plugin basiertes System zu entwerfen, das die
verschiedenen Metadaten--Exportformate und Metadaten--Bezugsquellen
zusammenführt und über eine *einheitliche Schnittstelle* anbietet.

Der modulare Aufbau und eine freie Lizenz sollen eine Entwicklung durch die
Community gewährleisten, so dass sich das System jederzeit um neue Plugins
erweitern lässt.

Des weiteren soll ein *Analyse--Teil* entstehen, der die Möglichkeit bietet bereits
vorhandene Datenbanken zu importieren, zu analisieren und fehlerhafte oder
fehlende Daten *automatisiert* zu korrigieren bzw. zu ergänzen.

*Anders* als bei den vorhandenen Media Managern, soll hier der Analyse--Teil
der Library erweiterbar sein. Zusätzlich soll es hier, über die Datenbeschaffung
hinweg und im Unterschied zu den bereits vorhanden Lösungen, Möglichkeiten zur
Metadatenaufbereitung (Säubern von ungewünschten Sonderzeichen, automatische
Extraktion von Schlüsselwörtern aus Inhaltsbeschreibung) geben.

Zusammengefasst soll das System gut an die jeweilige *Umgebung* und
*Bedürfnisse* des Benutzers anpassbar sein.  Im Gegensatz zu den bereits
vorhandenen *Movie Management--Tools*, bei denen fehlende Metadaten manuell vom
Benutzer explizit nachgepflegt werden müssen, soll das System mehr auf
automatisierte Verarbeitung ohne zutun des Benutzers ausgelegt sein.

.. rubric:: Footnotes

.. [#f0] Ein auf PC Komponenten basierendes Gerät zur Wiedergabe multimedialer
         Inhalte, dieser wird oft mit sog. Media Center Software wie dem Xbox
         Media Center betrieben
.. [#f1] http://www.amazon.de/Layer-Cake-Film-Flash-Drive/dp/B001Q3LOTQ
.. [#f2] http://encodingwissen.de/formatedschungel/container
.. [#f3] http://dvdxml.com/p/faq/faq.php?0.cat.2.3
.. [#f4] http://wiki.xbmc.org/index.php?title=NFO_files/movies

.. http://www.vodprofessional.com/features/introduction-to-video-metadata/
.. https://www.videouniversity.com/articles/metadata-for-video/
