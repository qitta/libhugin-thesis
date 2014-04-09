##########################################
Metadatenquellen, Software und Problematik
##########################################

Die vorgestellten Plattformen, Player und Tools zeigen nur einen Ausschnitt.
Alle Plattformen, Player und Tools aufzulisten ist aufgrund der Vielfalt
beziehungsweise Komplexität nicht möglich.

Metadatenarten und Quellen
==========================

Metadatenarten
--------------

Grundsätzlich lassen sich Film--Metadaten in zwei Kategorien
einordnen. Metadaten, die das Videoformat (Auflösung, Bitrate, ...) beschreiben
und Metadaten, die den Inhalt beschreiben. Metadaten zur Beschreibung des
Videoformats können je nach Container--Format direkt in die Datei eingebettet
werden (siehe :cite:`metadatenarten`).

Inhaltsbezogene Metadaten sind Daten, die bei der Digitalisierung nachträglich
gepflegt werden müssen. Typischerweise sind das Attribute wie Titel,
Erscheinungsjahr, Genre, Inhaltsbeschreibung, Cover und noch einige weitere.

Metadatenquellen
----------------

**Bezug von Metadaten**

Zum Bezug der Metadaten werden verschiedene Onlinequellen genutzt. Im Prinzip
eignet sich *jede* Seite, die Filminformationen pflegt als Metadatenquelle. Zu
den gängigen Metadatenquellen --- neben zahlreichen anderen Quellen --- zählen:

 * *Internet Movie Database (IMDb)*, englischsprachig
 * *The Movie Database (TMDb)*, multilingual, community--gepflegt
 * *Online Filmdatenbank (OFDb)*, deutschsprachig, community--gepflegt

**IMDb** ist mehr oder weniger der ,,Platzhirsch" unter den Metadatenquellen.
Für viele ist Sie die Standardbezugsplattform. Über die bei der IMDb für
jeden Film gepflegte *IMDb ID* kann ein Film genau identifiziert werden. Da
diese ID eindeutig ist, wird sie oft auch von anderen Onlinequellen mit erfasst
und gepflegt, um auch über diese eine Suche zu ermöglichen. Leider bietet IMDb
keine deutschsprachigen Daten an. Auch die grafischen Daten wie Cover und
Hintergrundbilder sind hier, im Vergleich zu anderen Quellen, von schlechterer
Qualität.

**TMDb** ist eine hauptsächlich Community gepflegte Onlinequelle. Die hier
gepflegten Filme enthalten neben den Standardmetadaten auch hochauflösende
Cover und Hintergrundbilder (sogenannte Backdrops und Fanart). Die Datenbank
wird oft von Open--Source--Projekten wie auch dem XBMC verwendet.

**OFDb** ist eine im deutschen Raum bekannte Filmdatenbank, welche
deutschsprachige Metadaten pflegt.

Die Metadaten, die von den jeweiligen Plattformen bezogen werden unterscheiden
sich stark in ihrer Qualität, Art und Umfang.  Insbesondere die
Inhaltsbeschreibung ist hier sehr vielfältig --- von kurz und knapp bis sehr
ausführlich. Schaut man sich beispielsweise für den Film *,,Per Anhalter durch die
Galaxis (2005)"* die deutsche Inhaltsbeschreibung auf den vier Film--Plattformen
*cinefacts.de* (siehe :cite:`cinefacts-paddg`), *filmstarts.de* (siehe
:cite:`filmstarts-paddg`), *OFDb.de* (siehe :cite:`ofdb-paddg`) und *TMDb*
(siehe :cite:`tmdb-paddg`) an, so wird man feststellen, dass jede dieser
Plattformen eine andere deutsche Inhaltsbeschreibung gepflegt hat. Je nach
persönlichen Präferenzen möchte man nur eine bestimmte Art von
Inhaltsbeschreibung einpflegen.


Software und Metadatenformate
=============================

Abspielsoftware
---------------

Die Darstellung einer mit Metadaten gepflegten Filmsammlung erfolgt in den
meisten Fällen über sogenannte Media--Center--Software, die für den
Home--Theater--PC Betrieb im Wohnzimmer angepasst ist.

Beispiele hierfür wären das Windows--Media--Center oder auch das freie
XBMC (siehe Abbildung :num:`fig-xbmcscreenshot`), welches in letzter Zeit noch
einmal durch den *Raspberry Pi* (siehe :cite:`raspberry`) Bekanntschaft erlangt
hat. Neben den PC--basierten Lösungen gibt es hier auch zahlreiche
Standalone--Lösungen wie beispielsweise Popcorn Hour (siehe
:cite:`popcornhour`).

.. _fig-xbmcscreenshot:

.. figure:: fig/xbmc-screenshot.png
    :alt: Screenshot einer im XBMC gepflegten Filmesammlung.
    :width: 90%
    :align: center

    Screenshot einer im XBMC gepflegten Filmesammlung.

Die Media--Center--Software kann ihre Metadaten in der Regal je nach Applikation
von einer oder mehreren Onlinequellen beziehen. Sie bieten dem Benutzer jedoch
in der Regal nicht die Möglichkeit Korrekturen durchzuführen und sind somit nur
bedingt zum Pflegen von großen Filmsammlungen geeignet.


Movie--Metadaten--Manager
-------------------------

Neben den Media--Center--Lösungen gibt es spezielle Tools für die Pflege und
Korrektur von Film--Metadaten, sogenannte *Movie--Metadaten--Manager*. Ein
Movie--Management--Tool, welches es unter *unixoden* Betriebssystemen
gibt, ist beispielsweise MediaElch (siehe Abbildung :num:`fig-mediaelch`, siehe
:cite:`mediaelch`). Hier gibt es unter Linux noch weitere Tools (siehe
:cite:`moviemanager`).

Diese Programme beziehen ihre Metadaten auf die gleiche Art und Weise wie auch
die Media--Center--Lösungen. Die Management--Tools bieten dem Benutzer
zusätzlich die Möglichkeit, fehlerhafte Metadaten manuell zu korrigieren oder
Metadaten zu ergänzen.

Da die Programme nur für die Pflege von Metadaten gedacht sind, gibt es hier
immer Import- und Exportschnittstellen, welche wiederum auf bestimmte Formate
(siehe Metadatenformate, :ref:`ref-metadatenformate`) begrenzt sind.

Bestimmte Onlinequellen wie die IMDb, bieten ihre Metadaten nur in englischer
Sprache an. Möchte man eine deutsche Inhaltsbeschreibung haben, so muss man auf
eine Onlinequelle zugreifen, die diese in deutscher Sprache pflegt. Je nach
Anwendung wird dies aber nicht immer unterstützt.

.. _fig-mediaelch:

.. figure:: fig/mediaelch.png
    :alt: Screenshot vom Movie--Metadaten--Manager MediaElch.
    :width: 90%
    :align: center

    Screenshot vom Movie--Metadaten--Manager MediaElch.


.. _ref-metadatenformate:

Metadatenformate
----------------

Im Gegensatz zum Musikbereich hat sich bei der Pflege von Metadaten im
Filmbereich kein Standard durchgesetzt. Hier wird je nach Abspiel- oder
Verwaltungssoftware jeweils ein anderes Format verwendet.

Das XBMC speichert seine Metadaten beispielsweise intern in einer
Datenbank und schreibt diese beim Exportieren in :term:`XML`--Dateien, das
sogenannte *nfo*--Format raus (siehe :cite:`xbmcnfo`). Nutzt man eine andere
Abspielsoftware wie das Windows--Media--Center, so werden die Metadaten im
*dvdxml*--Format, auch ein *XML* basiertes Format, abgespeichert (siehe
:cite:`dvdxml`). Hier gibt es noch zahlreiche andere Formate, auch bei den
Movie--Metadaten--Managern, auf die nicht weiter eingegangen wird.

Dieser Umstand erschwert das Pflegen der Film--Metadaten zusätzlich. Für die
beiden genannten Formate bieten Movie--Metadaten--Manager häufig Import- und
Exportmöglichkeiten an. Jedoch können andere Player oder auch
Standalone--Lösungen hier wiederum ganz andere Formate verwenden, die von der
Metadaten--Pflegesoftware nicht unterstützt werden.


Probleme bei der Metadatenpflege
================================

Unbekannte und ausländische Filme
---------------------------------

In den meisten Fällen werden bei den oben beispielhaft genannten Anwendungen die
richtigen Metadaten für die *bekannten* Hollywood Filme gefunden. Hat man aber
eine Filmsammlung, die viele *Independent Filme* [#f1]_ oder nicht amerikanische
Verfilmungen enthält, so kommt es immer wieder zu Problemen. Die grundlegenden
Probleme hier sind, dass ein Film entweder gar nicht gefunden wird, nur ein Teil
der Metadaten gefunden wird oder diese eben nur in einer bestimmten Sprache
bezogen werden können.

Werden Metadaten für einen bestimmten Film über die standardmäßig eingestellte
Onlinequelle nicht gefunden, so gibt es häufig die Möglichkeit eine andere
Onlinequelle zu verwenden. Hierbei entstehen jedoch neue Probleme, die nun
folgend betrachtet werden.

Redundante Metadaten
--------------------

**Grundlegende Problematik**

Redundanzen treten in der Regal auf, wenn bei einer Filmsammlung die Daten aus
unterschiedlichen Quellen stammen. Damit ist gemeint, dass beispielsweise das
Genre auf unterschiedlichen Plattformen unter einem anderen Namen gepflegt ist.
Beim Herunterladen von Metadaten aus mehreren Quellen, wird beispielsweise das
Genre ,,SciFi" von einer Onlinequelle und das Genre ,,Science--Fiction" von
einer andere Quelle bezogen. Durch diesen Umstand ist das eigentlich eindeutige
Genre Science Fiction in diesem Fall zweimal in der lokalen Datenbank
vorhanden. Neben dem Genre sind auch weitere Attribute von der
Redundanz--Problematik betroffen, jedoch ist das Genre, neben der
Inhaltsbeschreibung, laut Meinung des Autors, eins der wichtigsten Attribute, da
es maßgeblich in die Entscheidung der Filmauswahl einfließt.

Folgende Punkte führen konkret im unten genannten Beispiel (siehe Praxisbeispiel
für Dateninhomogenität, :ref:`ref-beispiel`) zu Redundanzen:

**Schreibweise des Genres**

Die Schreibweise der gepflegten Genres unterscheidet sich (siehe Abbildung
:num:`table-robocop`). Hier ist bei TMDb das Genre ,,Science Fiction'' und bei
OFDb ,,Science-Fiction'' gepflegt.

**Internationalisierung**

Je nach Onlinequelle ist das Genre in einer unterschiedlichen Sprache gepflegt.
IMDb listet hier das Genre ,,Comedy" (siehe Abbildung :num:`table-feuchtgebiete`),
TMDb die deutsche Bezeichnung ,,Komödie".


Divergente Metadaten
--------------------

**Divergente Genres**

Die OFDb--Quelle liefert für den Film *Feuchtgebiete (2013)* das Genre *Erotik*,
dieses Genre existiert bei IMDb (siehe :cite:`imdbgenre`) und bei TMDb
:cite:`tmdbgenre` gar nicht.

.. _ref-beispiel:

Praxisbeispiel für Dateninhomogenität
-------------------------------------

Um das Problem zu veranschaulichen, betrachten wir, parallel zur oben genannten
Problematik, Auszüge von Metadaten der drei Onlinequellen *IMDb*, *TMDb* und
*OFDb*.

Ausgehend von der Annahme, dass die Inhaltsbeschreibung (engl. Plot) und das
Genre zu den *wichtigsten* Kriterien bei der Filmauswahl gehören und diese somit
*sauber* gepflegt sein müssen, werden diese nachfolgend explizit betrachtet.

In unserem Beispiel befinden sich folgende vier Filme in der Filmsammlung, die
mit Metadaten versorgt werden sollen:

    1) *,,After.Life (2010)"*, US--amerikanischer Spielfilm
    2) *,,Feuchtgebiete (2013)"*, deutsche Romanverfilmung
    3) *,,Nymphomaniac (2013)"*, europäischer Spielfilm
    4) *,,RoboCop (2014)"*, US-amerikanischer Spielfilm

Die Inhaltsbeschreibung ist in der Regel problemlos austauschbar, jedoch
unterscheidet sie sich auch je nach Quelle in der Formatierung, Ausführlichkeit
und Sprachstil.  Nicht alle Inhaltsbeschreibungen haben beispielsweise hinter
dem Rollennamen immer den Namen des Schauspielers in Klammern. Sollen die
Metadaten in deutscher Sprache gepflegt werden, so fällt IMDb raus, da diese
Onlinequelle nur Metadaten in englischer Sprache anbietet. Die Onlinequelle wird
aber bezüglich des Genrevergleichs mit in die Tabellen aufgenommen.


**After.Life (2010):** Die Daten bei TMDb werden in verschiedenen Sprachen
gepflegt und sind in der Regel *qualitativ hochwertig*. Der erste Film wurde
bei TMDb gut eingepflegt, die Inhaltsbeschreibung ist deutschsprachig, das Genre
*feingranular* gepflegt. Des Weiteren bietet TMDb hochauflösende grafische
Metadaten (Cover, Hintergrundbilder). Bei OFDb ist das Genre ,,Mystery" nicht
gepflegt und zudem gibt es nur ein niedrig auflösendes Cover und keine
Hintergrundbilder (siehe Abbildung :num:`table-afterlife`).

.. figtable::
    :label: table-afterlife
    :spec: l|l|l|l
    :caption: Übersicht Metadatenquellen für den Film After.Life (2010)
    :alt: Übersicht Metadatenquellen für den Film After.Life (2010)

    +----------+------------------------+----------------------------------+-------------------------+
    | *Quelle* | *IMDb*                 | *TMDb*                           | *OFDb*                  |
    +==========+========================+==================================+=========================+
    | *Plot*   | englischsprachig       | deutschsprachig                  | deutschsprachig         |
    +----------+------------------------+----------------------------------+-------------------------+
    | *Genre*  | Drama, Horror, Mystery | Drama, Horror, Mystery, Thriller | Drama, Horror, Thriller |
    +----------+------------------------+----------------------------------+-------------------------+

*Zusammenfassung zum Genre:* austauschbar, unterschiedlich *feingranular* gepflegt

**Feuchtgebiete (2013):** Der zweite Film ist bei TMDb und OFDb gut gepflegt.
Jedoch fällt auf, dass das gepflegte Genre bei diesen beiden Onlinequellen keinen
Schnittmenge aufweist. Beim betrachten des Wikipedia--Artikels (siehe
:cite:`feuchtgebiete`) zum Film wird klar, dass das bei OFDb gepflegte Genre
auch seine Daseinsberechtigung hat.

.. figtable::
    :label: table-feuchtgebiete
    :spec: l|l|l|l
    :caption: Übersicht Metadatenquellen für den Film Feuchtgebiete (2013)
    :alt: Übersicht Metadatenquellen für den Film Feuchtgebiete (2013)

    +----------+------------------+-----------------+-----------------+
    | *Quelle* | *IMDb*           | *TMDb*          | *OFDb*          |
    +==========+==================+=================+=================+
    | *Plot*   | englischsprachig | deutschsprachig | deutschsprachig |
    +----------+------------------+-----------------+-----------------+
    | *Genre*  | Drama, Comedy    | Drama, Komödie  | Erotik          |
    +----------+------------------+-----------------+-----------------+

*Zusammenfassung zum Genre:* divergent, Problem der Internationalisierung


**Nymphomaniac (2013):** Hier ist bei TMDb die Inhaltsbeschreibung in Deutsch
nicht vorhanden. Der Film ist im Vergleich zu Hollywood--Blockbuster in
Deutsch relativ schlecht gepflegt. Bei OFDb ist wie auch beim ersten Film, eine
deutschsprachige Inhaltsangabe vorhanden. Zur großen Überraschung ist hier das
Genre im Vergleich zu den beiden anderen Onlinequellen *feingranularer* gepflegt
--- was laut Wikipedia (siehe :cite:`nymphomaniac`) den Filminhalt besser
widerspiegelt (siehe Abbildung :num:`table-nymphomaniac`).

.. figtable::
    :label: table-nymphomaniac
    :spec: l|l|l|l
    :caption: Übersicht Metadatenquellen für den Film Nymphomaniac (2013)
    :alt: Übersicht Metadatenquellen für den Film Nymphomaniac (2013)

    +----------+------------------+------------------+--------------------+
    | *Quelle* | *IMDb*           | *TMDb*           | *OFDb*             |
    +==========+==================+==================+====================+
    | *Plot*   | englischsprachig | englischsprachig | deutschsprachig    |
    +----------+------------------+------------------+--------------------+
    | *Genre*  | Drama            | Drama            | Drama, Erotik, Sex |
    +----------+------------------+------------------+--------------------+

*Zusammenfassung zum Genre:* divergent, unterschiedlich *feingranular* gepflegt

**RoboCop (2014):** Der vierte Film, eine Hollywood Remake--Produktion ist hier
bei allen drei Anbietern sehr gut gepflegt (siehe Abbildung :num:`table-robocop`).

.. figtable::
    :label: table-robocop
    :spec: l|l|l|l
    :caption: Übersicht Metadatenquellen für den Film RoboCop (2014)
    :alt: Übersicht Metadatenquellen für den Film RoboCop (2014)

    +----------+-----------------------+--------------------------------+------------------------------------------+
    | *Quelle* | *IMDb*                | *TMDb*                         | *OFDb*                                   |
    +==========+=======================+================================+==========================================+
    | *Plot*   | englischsprachig      | deutschsprachig                | deutschsprachig                          |
    +----------+-----------------------+--------------------------------+------------------------------------------+
    | *Genre*  | Action, Crime, Sci-Fi | Action, Science Fiction, Krimi | Action, Krimi, Science-Fiction, Thriller |
    +----------+-----------------------+--------------------------------+------------------------------------------+

*Zusammenfassung zum Genre:* unterschiedliche Schreibweise, divergent, Problem der
Internationalisierung, unterschiedlich *feingranular* gepflegt

Beim Bezug von Metadaten der vier Filme wird deutlich, welche Probleme bei der
Beschaffung dieser entstehen können. Diese Probleme werden beim *,,aktuellen
Stand der Technik"* durch den Benutzer mühsam manuell behoben. Bei kleinen
Filmsammlungen ist der Aufwand der manuellen Nachpflege noch vertretbar, nicht
jedoch bei *größeren* Sammlungen von mehreren hundert Filmen.


Auswirkungen
------------

Abspielsoftware wie das XBMC erlaubt es dem Benutzer, die Filme nach Genre zu
gruppieren und zu filtern. Durch dieses *Feature* kann der Benutzer einen Film
nach seinen Vorlieben aussuchen. Durch die Redundanzen ist eine eindeutige
Gruppierung nicht mehr möglich. Die Folge ist ein ungeordneter Zustand.

.. _ref-probleme-metadatensuche:

Probleme bei der Metadatensuche
===============================

Grundlegende Probleme
---------------------

**Exakte Suchstrings**

Viele Metadaten--Tools erwarten exakte Suchbegriffe. Falsch geschriebene Filme
wie ,,The Marix" oder ,,Sin Sity'' werden oft nicht gefunden (siehe Abbildung
:num:`table-movietools`).

**Suche nach IMDb ID**

Die Suche nach der IMDb ID ist bei den getesteten Tools häufig nicht möglich,
obwohl diese von manchen Onlineanbietern unterstützt wird (siehe Abbildung
:num:`table-movietools`).

Probleme bei Movie--Metadaten--Managern
---------------------------------------

Es wurden neben der Abspielsoftware XBMC und dem
Movie--Metadaten--Manager MediaElch, die bereits genannten
Movie--Metadaten--Manager (siehe :cite:`moviemanager`) *GCstar*, *vMovieDB*,
*Griffith* und *Tellico* betrachtet. Die Resultate hier waren eher *ernüchternd*
(siehe Abbildung :num:`table-movietools`). Bei den beiden Media--Managern GCstar
und vMovieDB hat die Metadatensuche nicht funktioniert, hier wurde nichts
gefunden. Das Verhalten wurde auf zwei Systemen nachgeprüft. Beim XBMC wurden
die Plugins für die Onlinequellen TMDb und Videobuster getestet. Für die
Unschärfesuche wurde nach *,,Sin Sity"* und nach *,,The Marix"* gesucht.


.. figtable::
    :label: table-movietools
    :spec: l|l|l|l
    :caption: Übersicht Movie--Metadaten--Manager und Funktionalität
    :alt: Übersicht Movie--Metadaten--Manager und Funktionalität

    +--------------------+------------------------+----------------------------+---------------------------+
    | *Software*         | *XBMC*                 | *MediaElch*                | *Tellico*                 |
    +====================+========================+============================+===========================+
    | *IMDB ID Suche*    | nein                   | nur über IMDb u. TMDb      | nein                      |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Unschärfesuche*   | nein                   | nein                       | nur IMDb, teilweise       |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Onlinequellen*    | verschiedene (plugin)  | verschiedene (6)           | wenige (3)                |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Metadatenformate* |  :math:`\times`        | nur XBMC                   | nein                      |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Datenkorrektur*   | :math:`\times`         | ja, manuell                | ja, manuell               |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Bemerkungen*      | pluginbasierte Scraper | Onlinequellen kombinierbar | :math:`\times`            |
    +--------------------+------------------------+----------------------------+---------------------------+
    | *Typ*              | Medien--Player         | Movie--Metadaten--Manager  | Movie--Metadaten--Manager |
    +--------------------+------------------------+----------------------------+---------------------------+


Die nicht funktionierenden Movie--Manager *GCstar* und *vMovieDB* wurde nicht
mit aufgenommen.  Das Tool Griffith wurde auch aus der Tabelle genommen, da hier
von den 40 Onlinequellen nur einzelne Quellen funktioniert haben --- IMDb hat
auch nicht funktioniert.


Anforderungen an das Projekt
============================

Viele der genannten Schwierigkeiten lassen sich aufgrund ihrer Natur und der
aktuellen Kombination aus Abspielsoftware und Movie--Metadaten--Manager nicht
oder nur mit manuellen Eingriff durch den Benutzer beheben. Bei *großen*
Filmsammlungen ist dies jedoch mit keinem vernünftigen Aufwand umsetzbar.

Idee: Modulare Herangehensweise
===============================

Es soll *kein neuer* Movie--Metadaten--Manager entwickelt werden. Die Idee ist
es, dem Entwickler beziehungsweise Endbenutzer einen *modularen
Werkzeugbaukasten* in Form einer pluginbasierten Bibliothek über eine
einheitliche Schnittstelle bereitzustellen, welcher an die persönlichen
Bedürfnisse anpassbar ist.

Des Weiteren soll die zusätzliche Funktionalität der Datenanalyse,
beispielsweise basierend auf Data--Mining Algorithmik, möglich sein. Das
Hauptaugenmerk des Systems liegt, im Gegensatz zu den bisherigen
Movie--Metadaten--Managern, auf der *automatisierten* Verarbeitung großer
Datenmengen.

.. rubric:: Footnotes

.. [#f1] Bezeichnung für Filme, die von Produktionsfirmen finanziert werden,
         welche nicht zu den großen US Studios gehören.
