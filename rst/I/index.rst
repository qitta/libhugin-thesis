##########
Einleitung
##########

.. epigraph::

   | |apostart| *Digital ist besser!* |apoend|

   -- *Marc-Uwe Kling, deutscher Kabarettist*


Motivation
==========

Die Digitalisierung der modernen Konsumgesellschaft schreitet immer weiter
voran. Wo es vor ein paar Jahren noch üblich war die eigene Filmsammlung im
Regal aufzubewahren, wird sie heute oft nur noch digital auf dem
:term:`Home--Theatre--PC`, :term:`Smart--TV`, PC oder anderen Endgeräten digital
aufgezeichnet und verwaltet. Das Aufkommen der digitalen HDTV--Sender` und das
große Angebot an Pay---TV--Sendern hat dem Trend der letzten Jahre nochmal
frischen Auftrieb verpasst. Und hat man mal einen Spielfilm verpasst, so kann
dieser bequem über einen der vielen Online Videorecorder--Dienste nachträglich
bezogen werden. Es geht sogar soweit, dass USB-Sticks (siehe
:cite:`usbstickmovie`) mit Hollywood Spielfilmen beworben und verkauft werden.

Zeichnet man viele Filme auf oder digitalisiert seine Filmsammlung, so muss
man sich mit dem Pflegen der inhaltsbezogen :term:`Metadaten` auseinander setzen.
Das sind Metadaten, wie sie auf jeder DVD/BD--Hülle enthalten sind. Wo noch
im DVD/BD--Regal diese auf der DVD/BD--Hülle zu finden waren, sind
sie nun nach dem digitalisieren nicht vorhanden und müssen vom Benutzer
nachträglich eingepflegt werden. Typische Metadaten bei Filmen sind der Titel,
Jahr, Inhaltsbeschreibung, Cover und Genre.  Diese Metadaten sind bei Filmen im
unterschied zur Musik essentiell, da hierüber die Entscheidung getroffen wird ob
ein Film geschaut wird oder nicht.

Die Metadaten werden in der Regel über Onlinequellen wie beispielsweise die
Internet Movie Database (IMDb, siehe :cite:`imdb`) bezogen. Die Anzahl der
möglichen Onlinedienste die Metadaten bereitstellen, ist hier praktisch
*ungebrenzt*. Viele Abspiel--Anwendungen wie das Windows Media Center oder das
Xbox Media Center (XBMC, siehe :cite:`xbmc`') können ihre Metadaten automatisch
aus dem Internet beziehen. Je nach Anwendung kann es hier im Hintergrund eine
oder mehrere Bezugsquellen für Metadaten geben.

Ein Problem bei der Pflege der Metadaten im Filmbereich ist, dass es hier
keinen Standard gibt der sich durchgesetzt hat. Es gibt einerseits die
Möglichkeit bestimmte Metadaten in bestimmte Container--Formate (siehe
:cite:`containerformate` zu integrieren, andererseits werden diese in separaten
Dateien oder Datenbanken der jeweiligen Abspiel--/Verwaltungssoftware gepflegt.

Ein weiteres Problem ist die *große* Anzahl verschiedener Onlinequellen von
denen die Metadaten bezogen werden. Hier werden von Anwendung zu Anwendung
unterschiedliche Quellen verwendet, die je nach Filmsammlung gut oder weniger
gut geeignet sind. Die Onlinequellen unterscheiden stark in der Qualität, Umfang
und Art der angebotenen Metadaten. Zusätzlich kommt noch das Problem der
Internationalisierung hinzu.

Daraus resultierend sind über die Jahre sogenannte *Movie Manager* entstanden,
die den Benutzer bei der Pflege der Filmsammlung unterstützen sollen. Auch hier
gibt es nicht das *Tool der Wahl*, die Problematik ist weiterhin vorhanden. Es
gibt wieder verschiedene Tools, die nur bestimmte Metadaten--Exportformate
verstehen, nur bestimmte Onlinequellen ansprechen können oder auch nur
unter bestimmten Betriebssystemen verfügbar sind. Die unter Linux vorhandenen
und getesteten *Movie Manager* funktionieren bis auf wenige Ausnahmen
unbefriedigend oder gar nicht, was die Hauptmotivation diese Arbeit ist.

Projektziel
===========

Das Ziel dieser Arbeit ist es eine andere Herangehensweise zu zeigen und ein
offenes pluginbasiertes System zu entwerfen, das die verschiedenen
Metadaten--Exportformate und Metadaten--Bezugsquellen zusammenführt und über
eine *einheitliche Schnittstelle* anbietet. Neben der Funktionalität der
Metadatenbeschaffung, soll es die Möglichkeit der Metadatenaufbereitung (Säubern
von ungewünschten Sonderzeichen, automatische Extraktion von Schlüsselwörtern
aus Inhaltsbeschreibung, etc.) geben.

Die aktuellen Tools zur Metadatenverwaltung verfolgen einen eher *statischen*
Ansatz.  Im Gegensatz dazu soll das System nach dem Baukastenprinzip erweiterbar
sein und durch schreiben neuer Plugins an verschiedene Anforderungen des
Benutzers anpassbar sein.

Im Unterschied zu den bereits vorhandenen Tools die hauptsächliche durch
manuelle Interaktion des Benutzers gesteuert werden, soll das System auf eine
automatisierte Verarbeitung ausgelegt sein. Hier liegt das Augenmerk auf der
Pflege *großer* Filmsammlungen.

Der modulare Aufbau und eine freie Lizenz sollen eine Weiterentwicklung durch
die Community gewährleisten und eine ganz neue Art von Funktionalität bieten.


Projektlizenz und Namensgebung
==============================

Lizenz
------

Um eine communitybasierte Weiterentwicklung zu gewährleisten und damit auch
,,Verbesserungen" an das Projekt zurückfließen zu lassen, wird das System unter
der GPLv3 Lizenz (siehe :cite:`gpl`) entwickelt.

Namensgebung und Logo
---------------------

Um dem Projekt ein ,,Gesicht" zu geben und den Wiedererkennungwert zu steigern,
wird das Projekt auf den Namen ,,libhugin" getauft und ein Logo entwickelt
(siehe Abbildung :num:`fig-huginlogo`), welches einen Raben in Pixelgrafik und
ein Stück Filmrolle zeigt. Der Name Hugin kommt aus der nordischen Mythologie:

.. epigraph::

   *Hugin gehört zum altnordischen Verb huga „denken“, das hierzu zu stellende*
   *Substantiv hugi „Gedanke, Sinn“ ist seinerseits die Grundlage für den Namen*
   *Hugin, der mit dem altnordischen Schlussartikel –in gebildet wurde. Hugin*
   *bedeutet folglich „der Gedanke“.*

                                -- http://de.wikipedia.org/wiki/Hugin_and_Munin


.. _fig-huginlogo:

.. figure:: fig/hugin.png
    :alt: libhugin Logo.
    :width: 30%
    :align: center

    libhugin Logo.

.. http://www.vodprofessional.com/features/introduction-to-video-metadata/
.. https://www.videouniversity.com/articles/metadata-for-video/
