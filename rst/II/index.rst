#################################
Digitale Videodaten und Metadaten
#################################

*Der folgende Teil soll einen Überblick über gängige Metadaten--Plattformen,
Player und Video--Management--Tools verschaffen, anhand welcher die
Schwierigkeiten beim Video--Metadaten pflegen erläutert werden.*

*Die vorgestellten Plattformen, Player und Tools zeigen nur einen Ausschnitt,
alle bekannten Plattformen, Player und Tools aufzulisten ist aufgrund der
Vielfalt bzw.  Komplexität nicht möglich.*


Metadatenarten und Quellen
==========================

Metadatenarten
--------------

:dropcaps:`Grundsätzlich` lassen sich Video--Metadaten in zwei Kategorien
einordnen. Metadaten die das Videoformat (Auflösung, Bitrate, ...) beschreiben
und Metadaten die den Inhalt beschreiben. Metadaten zur Beschreibung des
Videoformat können je nach Container-Format direkt in in die Datei eingebettet
werden.

Inhaltsbezogene Metadaten sind Daten die bei der Digitalisierung nachträglich
gepflegt werden müssen. Gängige Metadaten hier sind:

    * Titel
    * Erscheinungsjahr
    * IMDB-ID
    * Genre
    * Bewertung
    * Cover (i.d.R. DVD/BD--Cover)
    * Fanart, Backdrops (zusätzliches Bildmaterial)
    * Inhaltsbeschreibung
    * Regisseur
    * Besetzung
    * Produktionsland
    * Schlagwörter


Metadatenquellen
----------------

**Bezug von Metadaten**

Zum Bezug der Metadaten werden verschiedene Onlineplattformen genutzt. Im
Prinzip eignet sich *jede* Seite die Filminformationen pflegt als
Metadatenquelle. Viele Plattformen bieten hier direkt eine API an, um den Zu den
oft genutzten Metadatenquellen --- neben zahlreichen anderen Quellen --- zählen:

 * Internet Movie Database (IMDb), englischsprachig
 * The Movie Database (TMDb), multilingual, Community gepflegt
 * Online Filmdatenbank (OFDb), deutschsprachig, Community gepflegt

**Unterschiede und Qualität**

Alle drei genannten Metadatenquellen haben je nach Art, Umfang und Qualität der
Metadaten ihre ,,Stärken'' und ,,Schwächen''.

**IMDb** ist mehr oder weniger der ,,Platzhirsch'' unter den Metadatenquellen. Sie
ist eine Art ,,Quasistandard--Bezugsplattform". Über die bei der IMDb für jeden
Film gepflegte sog. IMDb-ID kann ein Film genau identifiziert werden. Da diese
ID eindeutig ist, wird sie oft auch von anderen Onlinedatenbanken mit erfasst
und gepflegt um auch über diese eine Suche zu ermöglichen. Leider bietet IMDb
keine deutschsprachigen Daten an. Auch die Cover und Fanart Daten sind hier von
niedriger Qualität.

**TMDb** ist eine hauptsächlich Community gepflegte Datenbank. Die hier gepflegten
Filme enthalten neben den ,,Standard Metadaten'' auch hochauflösende Cover und
Hintergrundbilder (Backdrops, Fanart). Die Datenbank wird oft und gerne von Open
Source Projekten wie auch dem Xbox Media Center verwendet.

**OFDb** ist eine im deutschen Raum bekannte Filmdatenbank, welche deutschsprachige
Metadaten pflegt.

Die Metadaten die von den jeweiligen Plattformen bezogen werden unterscheiden
sich stark in ihrer Qualität. Insbesondere auch die Filmbeschreibungen sind hier
sehr vielfältig -- von kurz und knapp bis sehr ausführlich. Schaut man sich
beispielsweise für den Film ,,Per Anhalter durch die Galaxis (2005)'' die
deutsche Inhaltsbeschreibung auf den vier Video--Plattformen *cinefacts.de*
(siehe :cite:`cinefacts-paddg`), *filmstars.de* (siehe :cite:`filmstars-paddg`),
*ofdb.de* (siehe :cite:`ofdb-paddg`) und *themoviedb.org* (siehe
:cite:`tmdb-paddg`), so wird man feststellen, dass jede dieser Plattformen eine
andere deutsche Inhaltsbeschreibung gefplegt hat.

Manche Filmbeschreibungen erzählen den ganzen Film, andere verraten fast gar
nichts. Je nach persönlichen Präferenzen, möchte man nur eine bestimmte Art von
Inhaltsbeschreibung einpflegen.


Software und Metadatenformate
=============================

Medienplayer
------------

Die Darstellung einer mit Metadaten gepflegten Filmesammlung erfolgt in den
meisten Fällen über sog.  ,,Media Center''--Software, die für den ,,Home-Theater
Betrieb'' im Wohnzimmer angepasst ist. Beispiele hierfür wären das Windows Media
Center oder auch das freie Xbox Media Center (Abb. :num:`fig-xbmcscreenshot`,
siehe auch :cite:`xbmc`), welches in letzter Zeit noch einmal durch den
Raspberry PI (siehe :cite:`raspberry`) Bekanntschaft erlangt hat. Neben den PC
basierten Lösungen gibt es hier auch zahlreiche Standalone Lösungen wie
beispielsweise Popcorn Hour (siehe :cite:`popcornhour`).

Die Media Center können ihre Metadaten i.d.R. je nach Applikation von einer oder
mehrerer Metadatenquellen beziehen. Sie bieten dem Benutzer jedoch oft nicht die
Möglichkeit Korrekturen durchzuführen und sind somit nur bedingt zum *pflegen*
von großen Filmesammlungen geeignet.

.. _fig-xbmcscreenshot:

.. figure:: fig/xbmc-screenshot.png
    :alt: In XBMC gepflegte Filmesammlung
    :width: 70%
    :align: center

    Screenshot einer im Xbox Media Center gefpegten Filmesammlung.


Video Management Tools
----------------------

Neben den Media Center Lösungen gibt es spezielle Tools für die Pflege und
Korrektur von Film--Metadaten, sog.  *Video--Management--Tools*. Ein
Video--Management--Tool, welches es unter *unixoden* Betriebssystemen seit kurzem
gibt ist MediaElch (Abb.  :num:`fig-mediaelch`, siehe auch :cite:`mediaelch`).

Diese Programme beziehen ihre Metadaten auf die gleiche Art und Weise wie auch
die Media Center Lösungen. Die Management Tools bieten dem Benutzer die
zusätzliche Möglichkeit fehlerhafte Metadaten manuell zu korrigieren und zu
ergänzen.

Da die Programme nur für die Pflege von Metadaten gedacht sind, gibt es hier
immer import/export--Schnittstellen, welche wiederrum auf bestimmte Formate
begrenzt sind.

Bestimmte Onlinequellen wie die Internet Movie Database, bieten ihre Metadaten
nur in englischer Sprache an. Möchte man eine deutsche Inhaltsbeschreibung
haben, so muss man auf einen Anbieter zugreifen der diese in deutscher Sprache
pflegt. Je nach Anwendung wird dies aber nicht immer unterstützt.

.. _fig-mediaelch:

.. figure:: fig/mediaelch.png
    :alt: Übersicht MediaElch Video Management Tool.
    :width: 70%
    :align: center

    Screenshot Video Management Tool MediaElch.


Metadatenformate
----------------

Ein  weiterer Punkt der erwähnt werden sollte, ist dass es bei der Archivierung
der Metadaten keinen durchgesetzten Standard gibt. Hier werden je nach
Playersoftware verschiedene Formate verwendet. Das Xbox Media Center speichert
seine Metadaten intern in einer Datenbank und schreibt diese beim ,,Export'' in
xml--Dateien [#f0]_, sog nfo-Files raus (siehe :cite:`xbmcnfo`). Nutzt man eine
andere Abspielsoftware wie das Windows Media Center, so werden die Metadaten im
dvdxml-Format, auch ein xml basiertes Format abgespeichert (siehe :cite:`dvdxml`).

Dieser Umstand erschwert das Pflegen der Video--Metadaten zusätzlich. Für die
beiden genannten Formaten bieten Video Management Tools oft import/export
Möglichkeiten. Jedoch können andere Player oder auch Standalone Lösungen hier
wiederum ganz andere Formate verwenden, die von der Metadaten--Pflegesoftware
noch nicht unterstützt werden.


Problematik
===========

Unbekannte/ausländische Filme
-----------------------------

In den meisten Fällen werden bei den oben beispielhaft genannten Anwendungen die
richtigen Metadaten für die ,,bekannten'' Hollywood Filme gefunden. Hat man aber
eine Filmesammlung die viele *Independent Filme* [#f1]_ oder nicht amerikanische
Verfilmungen enthält, so kommt es immer wieder zu Problemen. Die grundlegenden
Probleme hier sind, dass ein Film entweder gar nicht gefunden wird, nur ein Teil
der Metadaten gefunden wird oder diese eben nur in einer bestimmten Sprache
bezogen werden können.

Wird ein bestimmter Film beim standardmäßig verwendeten Anbieter nicht
gefunden, so könnte man diesen normalerweise über einen anderen Anbieter
beziehen. Das ist jedoch nicht möglich, ohne dass dabei zusätzliche Probleme
entstehen. Im Folgenden werden diese Probleme anhand eines Beispiels erläutert.


Dateninhomogenität
------------------

Dieses Problem tritt in der Regal auf wenn bei einer Filmesammlung die Daten aus
unterschiedlichen Quellen stammen.

Um das Problem zu veranschaulichen, betrachten wir Auszüge von Metadaten der
drei o.g. Onlinedatenbanken. An einem Beispiel lässt sich die Problematik am
besten erklären.

Wir gehen von der Annahme aus, dass wir eine deutschsprachige
Inhaltsbeschreibung möchten und die folgenden drei Filme in unserer
Filmesammlung mit Metadaten versorgen wollen:

    1) ,,After.Life (2010)'', US-amerikanischer Spielfilm, Agnieszka Wojtowicz-Vosloo
    2) ,,Feuchtgebiete (2013)'', deutsche Romanverfilmung, Charlotte Roche
    3) ,,Nymphomaniac (2013)'', europäisches Drama, Lars von Trier
    4) ,,RoboCop (2014)'', US-amerikanischer Spielfilm, José Padilha


Die zweite Annahme die wir treffen ist, dass die Inhaltsbeschreibung und das
Genre zu den *wichtigsten* Kriterien bei der Filmauswahl gehören und diese somit
*sauber* gepflegt sein müssen.

Möchte man seine Metadaten in deutscher Sprache pflegen, so fällt kategorisch
der IMDb Anbieter weg, da hier nur englischsprachige Informationen bezogen
werden.


**After.Life (2010)**

.. figtable::
    :label: table-afterlife
    :caption: Übersicht Metadatenquellen für den Film After.Life (2010)
    :alt: Übersicht Metadatenquellen für den Film After.Life (2010)

    +-------+------------------------+----------------------------------+-------------------------+
    |       | IMDb                   | TMDb                             | OFDb                    |
    +=======+========================+==================================+=========================+
    | Plot  | englischsprachig       | deutschsprachig                  | deutschsprachig         |
    +-------+------------------------+----------------------------------+-------------------------+
    | Genre | Drama, Horror, Mystery | Drama, Horror, Mystery, Thriller | Drama, Horror, Thriller |
    +-------+------------------------+----------------------------------+-------------------------+

Die Daten bei TMDb werden in verschiedenen Sprachen gepflegt und sind i.d.R.
*qualitativ hochwertig*. Unser erster Film wurde bei TMDb gut eingepflegt, die
Inhaltsbeschreibung ist deutschsprachig, das Genre feingranular gepflegt. Des
weiteren bietet uns TMDb auch gleich hochauflösende Cover und Film-Fanart. Bei
OFDb ist das Genre ,,Mystery'' nicht gepflegt und zudem gibt es nur ein
niedrigauflösendes Cover und kein Fanart (siehe Tabelle :num:`table-afterlife`).


**Feuchtgebiete (2013)**

.. figtable::
    :label: table-feuchtgebiete
    :caption: Übersicht Metadatenquellen für den Film Feuchtgebiete (2013)
    :alt: Übersicht Metadatenquellen für den Film Feuchtgebiete (2013)

    +-------+------------------+-----------------+-----------------+
    |       | IMDb             | TMDb            | OFDb            |
    +=======+==================+=================+=================+
    | Plot  | englischsprachig | deutschsprachig | deutschsprachig |
    +-------+------------------+-----------------+-----------------+
    | Genre | Drama, Comedy    | Drama, Komödie  | Erotik          |
    +-------+------------------+-----------------+-----------------+

Unser zweiter Film ist bei TMDb und OFDb gut gefplegt. Was hier jedoch auffällt
ist, dass das gepflegte Genre bei diesen beiden Anbietern keinen Schnittpunkt
hat. Liest man sich zu dem Film den Wikipedia Artikel (siehe
:cite:`feuchtgebiete`) durch, so hat auch das bei OFDb gepflegte Genre seine
Daseinsberechtigung.


**Nymphomaniac (2013)**

.. figtable::
    :label: table-nymphomaniac
    :caption: Übersicht Metadatenquellen für den Film Nymphomaniac (2013)
    :alt: Übersicht Metadatenquellen für den Film Nymphomaniac (2013)

    +-------+------------------+------------------+--------------------+
    |       | IMDb             | TMDb             | OFDb               |
    +=======+==================+==================+====================+
    | Plot  | englischsprachig | englischsprachig | deutschsprachig    |
    +-------+------------------+------------------+--------------------+
    | Genre | Drama            | Drama            | Drama, Erotik, Sex |
    +-------+------------------+------------------+--------------------+

Hier ist bei TMDb die Inhaltsbeschreibung in deutsch nicht vorhanden. Der Film
ist im Vergleich zu ,,Hollywood''-Blockbuster in deutsch relativ schlecht
gepflegt. Bei OFDb ist wie auch beim ersten Film, eine deutschsprachige
Inhaltsangabe vorhanden. Zur großen Überraschung ist hier das Genre im vergleich
zu den beiden anderen Metadatenanbietern feingranularer gefplegt -- was laut
Wikipedia (siehe :cite:`nymphomaniac`) auch besser zum Film passen würde (siehe
Tabelle :num:`table-nymphomaniac`).


**RoboCop (2014)**

.. figtable::
    :label: table-robocop
    :caption: Übersicht Metadatenquellen für den Film RoboCop (2014)
    :alt: Übersicht Metadatenquellen für den Film RoboCop (2014)

    +-------+-----------------------+--------------------------------+------------------------------------------+
    |       | IMDb                  | TMDb                           | OFDb                                     |
    +=======+=======================+================================+==========================================+
    | Plot  | englischsprachig      | deutschsprachig                | deutschsprachig                          |
    +-------+-----------------------+--------------------------------+------------------------------------------+
    | Genre | Action, Crime, Sci-Fi | Action, Science Fiction, Krimi | Action, Krimi, Science-Fiction, Thriller |
    +-------+-----------------------+--------------------------------+------------------------------------------+

Der vierte Film, eine Hollywood Remake--Produktion ist hier bei allen drei
Anbietern sehr gut gepflegt (siehe Tabelle :num:`table-robocop`)


**Zusammenfassung**

Wo die Inhaltsbeschreibung noch relativ *problemlos* zwischen den
unterschiedlichen Metadatenanbietern austauschbar ist, treten beim Genre mehrere
Schwierigkeiten auf:


**Unterschiedliche Sprache**

Je nach Metadatenanbieter ist das Genre in einer unterschiedlichen Sprache
bezogen wird. IMDb listet hier das Genre ,,Comedy'' (siehe Tabelle
:num:`table-feuchtgebiete`), TMDb die deutsche Bezeichnung ,,Komödie''. Dieser
Umstand würde in unserer Datenbank nach dem Einpflegen die beiden Genres
,,Comedy'' und ''Komödie'' einpflegen, was eine Gruppierung bzw. Auswahl von
Filmen nach einem bestimmten Genre unmöglich macht bzw. einschränkt.


**Divergente Genres**

Die OFDb--Quelle lieferet das Genre ,,Erotik'', dieses Genre existiert bei IMDb
(siehe :cite:`imdbgenre`) und bei TMDb :cite:`tmdbgenre` gar nicht.


**Uneinheitliche Schreibweise der Genres**

Die Schreibweise der gepflegten Genres unterscheidet sich (siehe
:num:`table-robocop`). Hier ist bei TMDb das Genre ,,Science Fiction'' und bei
OFDb ,,Science-Fiction'' gepflegt, was wieder zwei Einträge beim parallelen
Nutzen der beiden Anbieter in unsere Datenbank schreiben würde.

Beim Bezug von drei Filmen wird deutlich welche *Probleme* bei der Beschaffung
der Metadaten enstehen können. Diese Probleme werden beim *aktuellen Stand der
Technik* durch den Benutzer mühsam manuell gepflegt. Bei kleinen Filmesammlungen
ist der Aufwand der manuellen *nachpflege* noch vertretbar, nicht jedoch bei
*größeren* Sammlungen von mehreren hundert Filmen.

Weitere Probleme
-----------------

**Exakte Suchstrings**

Die Metadatentools erwarten i.d.R. exakte Suchbegriffe. Bei den getesteten Tools
wird bei Eingabe von "the marix" kein Film gefunden.

**Suche nach IMDB-ID**

Die Suche nach der IMDB-ID ist bei den getestenten Tools nicht möglich, obwohl
diese von manchen Onlineanbietern unterstützt wird.



Erkentnisse und Anforderungen an das Projekt
============================================

**Vielen der genannten Schwierigkeiten lassen sich aufgrund ihrer Natur und dem
aktuellen Kombination aus Abspielsoftware und Management Tools nicht oder nur
mit manuellen Eingriff durch den Benutzer beheben beheben.**


Idee
====

Die Idee ist es eine andere Herangehensweise umzusetzen mit dem Ziel die
genannten Probleme abzumildern oder zu beheben.

Es soll *kein neues* Metadaten Management Tool entwickelt werden. Die Idee ist
es dem Entwickler bzw. Endbenutzer einen ,,Werkzeugbaukasten'' in Form einer
Bibliothek über eine einheitliche Schnittstelle bereitzustellen, welcher an die
persönlichen Bedürfnisse anpassbar mit der zusätzlichen Funktionalität der
Datenanalyse basierend auf Data-Mining Algorithmen. Abbildung X zeigt den
konzeptuellen Ansatz.

Das Hauptaugenmerk hier liegt, im Gegensatz zu den bisherigen Metadaten
Management Tools, auf der *automatisierten* Verarbeitung großer Datenmengen.

.. rubric:: Footnotes

.. [#f0] Extensible Markup Language (XML), ist eine Auszeichnungssprache zur hierarchisch strukturierten Darstellung von Daten in Textdateien.
.. [#f1] Bezeichnung für Filme, die von Produktionsfirmen finanziert werden,
         welche nicht zu den großen US Studios gehören.
