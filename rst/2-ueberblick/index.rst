##########################################
Libhugin Metadaten Such- und Analysesystem
##########################################

Allgemeines zum System
======================

Die zu evaluierende Bibliothek *libhugin* wurde entworfen, weil es mit den
aktuellen Applikationen zur Metadaten Beschaffung und Pflege immer wieder zu
Probleme kommt. Oft werden beispielsweise ausländische Filme nicht gefunden, die
Inhaltsbeschreibung liegt nur in einer bestimmten Sprache vor oder es kommt zu
Redundanzen bei den Metadaten, wenn auf mehrere Onlinequellen parallel
zugegriffen wird (vgl. :cite:`cpiechula`). Zu den bekannten Applikationen
(Abspielsoftware), sogenannte Media--Center, gehören beispielsweise das
XBMC--Media--Center oder das Windows--Media--Center.

Bei der entwickelten Bibliothek wird eine andere Herangehensweise im Vergleich
zu den bereits existierenden Applikationen gezeigt. Es wurde ein modulares
System entworfen, welches sich nach dem Baukastenprinzip an die jeweiligen
Anforderungen gut anpassen lässt. Das Konzept der Metadatenbeschaffung wurde
gleichzeitig um die Funktionalität der Metadatenaufbereitung erweitert.

Die Bibliothek wurde in die zwei Teile *libhugin--harvest*
(Metadatenbeschaffung) und *libhugin--analyze* (Metadatenaufbereitung)
aufgeteilt. Der *libhugin-harvest* Teil der Bibliothek ist um die folgenden drei
Pluginarten erweiterbar:

    * Provider, Zugriff auf Onlinequellen.
    * Postprocessor, Manipulation der Metadaten direkt nach dem Herunterladen.
    * Converter, Unterstützung verschiedener Metadaten--Exportformate.

Der *libhugin-analyze* Teil der Bibliothek dient zur nachträglichen
Manipulation und Analyse der Metadaten, hier gibt es die Möglichkeit folgende
Pluginarten zu implementieren:

    * Analyzer, Analyse der Metadaten.
    * Modifier, Direkte Modifikation der Metadaten.
    * Comparator, Vergleich der Metadaten verschiedener Filme untereinander.

Die Bibliothek wurde in der Programmiersprache Python (Version 3.3) entworfen.


Asynchrone Ausführung
=====================

Bestimmte Teile von *libhugin* wurden multithreaded entwickelt. Hierzu zählen
die Downloadqueue so wie die Möglichkeit die Suchanfrage asynchron
loszuschicken.

Da der Zugriff auf Onlinequellen je nach Serverauslastung und Internetanbindung
in der Performance stark variiert, wurde das Herunterladen der Metadaten
parallelisiert. Das parallele Herunterladen zeigt deutliche
Geschwindigkeitsvorteile im Vergleich zur seriellen Verarbeitung (siehe
Abbildung :num:`fig-threaded-download`).




Normalisierung der Metadaten
============================

Die Normalisierung der Metadaten aus unterschiedlichen Quellen ist sehr
schwierig, da es bei den Filmmetadaten keinen einheitlichen Standard gibt. Um
fehlerhafte oder fehlende Metadaten über unterschiedliche Quellen zu ergänzen,
müssen die Metadaten normalisiert werden. Dieses Problem wird nun Anhand vom
Genre Attribut, welches in der internen Metadaten--Datenbank des XBMC abgelegt
wurde, beispielhaft erklärt.

Wird beispielsweise der Spielfilm ,,The Matrix (1999)" über drei verschiedene
Onlinequellen bezogen, so erhält man, falls das Genre ,,Science Fiction" bei den
jeweiligen Quellen gepflegt wurde, oft eine unterschiedliche Schreibweise.

    * TMDb (www.themoviedb.org): Science Fiction
    * IMDb (www.imdb.com): Sci--Fi
    * OFDb (www.ofdb.de): Science--Fiction

Wird nun der Film ,,The Matrix (1999)" über TMDb bezogen und der Film ,,Matrix
Revolutions (2003)" über IMDb, weil er beispielsweise bei TMDb nicht gepflegt
ist, so wird in diesem Fall das Genre mit den zwei unterschiedlichen
Schreibweisen ,,Science Fiction" und ,,Sci--Fi" bezogen.

Durch diesen Umstand haben wir eine Genreinformation redundant in unserem
XBMC--Center gepflegt. Es ist also nicht mehr möglich dieses Filmgenre eindeutig
zu identifizieren. Es ist somit weder eine Gruppierung nach diesem Genre noch
eindeutige eindeutige Filterung möglich.

Dieses Problem betrifft grundsätzlich alle Filmmetadaten Attribute, jedoch
lassen sich andere Attribute wie die Inhaltsbeschreibung problemlos austauschen,
diese von Natur aus individuell und sich somit nicht normalisieren lässt.

Da das Filmgenre, neben der Inhaltsbeschreibung, zu den wichtigsten
Auswahlkriterien bei Filmen zählt, wurde hier bei *libhugin* ein statisches
Konzept der Normalisierung umgesetzt.

Die Normalisierung bei *libhugin* bildet hierzu jedes Genre einer Onlinequelle
auf einem Globalen Genre ab.




.. epigraph::

   | |apostart| *Human beings, who are almost unique in having the ability to learn from the*
   | |apopar|  *experience of others, are also remarkable for their apparent disinclination to do so.* |apoend|

   -- *Douglas Adams, ,,Last Chance to See''*

You can reference a section by its label. This chapter is
Chapter |nbsp| :ref:`ch-refs`.

.. _sec-refs-sub1:

Subsection
==========

This subsection is Section |nbsp| :ref:`sec-refs-sub1`.

Citations
=========

COLLADA |nbsp| :cite:`collada` is a cool 3D file format. I wrote a paper about
3D stuff |nbsp| :cite:`icmepaper`. The website we built is running |nbsp|
:cite:`open3dhub`. The bibliography is in bibtex format.

Footnotes
=========

Reference a footnote |nbsp| [#foot-something]_.

External Links
==============

You can link to a `website <http://google.com/>`_.

.. rubric:: Footnotes

.. [#foot-something] This is a footnote at the end of the page or document.

