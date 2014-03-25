###########################################
Libhugin Einsatzmöglichkeiten in der Praxis
###########################################

Im Folgenden werden die beiden CLI--Demoanwendungen Geri und Freki vorgestellt,
sowie weitere Einsatzmöglichkeiten.


*Das vorgestellten CLI-Tools stellen nur einen kleinen Ausschnit der Fähigkeiten
der Library dar, die Library selbst ist um jede denkbare Funktionalität
erweiterbar.*

Geri
====

Geri ist eine CLI--Anwendung die zu Demozwecken aber auch als Testwerkzeug für
die libhugin harvest Library verwendet werden kann.

Übersicht der Optionen
----------------------

Ein Überblick über die Funktionalität und Möglichen Optionen zeigt die Hilfe des
Tools:

.. code-block:: bash

   $python tools/geri -h
   Libhugin commandline tool.

   Usage:
     geri (-t <title>) [-y <year>] [-a <amount>] [-p <providers>...] [-c <converter>] \
          [-o <path>] [-l <lang>] [-P <pm>]  [-r <processor>] [-f <pfile>] [-L]
     geri (-i <imdbid>) [-p <providers>...] [-c <converter>] [-o <path>] [-l <lang>] \
          [-r <processor>] [-f <pfile>] [-L]
     geri (-n <name>) [--items <num>] [-p <providers>...] [-c <converter>] [-o <path>]
     geri list-provider
     geri list-converter
     geri list-postprocessing
     geri -h | --help
     geri --version

    Options:
      -t, --title=<title>               Movie title.
      -y, --year=<year>                 Year of movie release date.
      -n, --name=<name>                 Person name.
      -i, --imdbid=<imdbid>             A imdbid prefixed with tt.
      -p, --providers=<providers>       Providers to be used.
      -c, --convert=<converter>         Converter to be used.
      -r, --postprocess=<processor>     Postprocessor to be used.
      -o, --output=<path>               Output folder for converter result [default: /tmp].
      -a, --amount=<amount>             Amount of items to retrieve.
      -l, --language=<lang>             Language in ISO 639-1 [default: de]
      -P, --predator-mode               The magic 'fuzzy search' mode.
      -L, --lookup-mode                 Does a title -> imdbid lookup.
      -f, --profile-file=<pfile>        User specified profile.
      -v, --version                     Show version.
      -h, --help                        Show this screen.


Das Tool eignet sich neben dem Einsatz als Testwerkzeug für Library und Plugins
auch gut für Scripte und somit für automatische Verarbeitung *großer*
Datenmengen.


Filmsuche
---------

Ein Film kann über den Titel oder über die IMDBid gesucht werden. Hier gibt es
die Möglichkeit auch bestimmten Provider, Converter, Sprache und Postproxessing
Plugins anzugeben.

Um das ,,Ausgabeformat'' zu konfigurieren gibt es im Geri--Ordner eine
,,movie.mask'' und ,,person.mask'' Datei. Über diese Datei kann die Ausgabe
formatiert werden. Die Syntax ist simpel, einfach das gewünschte Attribut in
geschweiften klammern. Das ,,num''--Attribut gibt Geri noch die Möglichkeit die
Resultate durch zu nummerieren.

Definition einer Ausgabemaske für Filme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   echo "{num}) {title} ({year}), IMDBid: {imdbid} Provider: {provider}\
   \nInhalt: {plot}" > tools/geri/movie.mask

Filmsuche
~~~~~~~~~

Standard Suche nach Titel mit der Begrenzung auf fünf Ergebnisse:

.. code-block:: bash

   $geri -t "sin city" -a5
   1) Sin City (2005), IMDBid: tt0401792, Provider: TMDBMovie <picture, movie>
   Inhalt: Basin City, genannt Sin City, ist ein düsteres Metropolis, in dem nichts
   und niemand wirklich sicher ist, in dem die Gewalt allgegenwärtig ist [...]

   2) Sin City (2005), IMDBid: tt0401792, Provider: OFDBMovie <movie>
   Inhalt: Basin City, genannt Sin City, ist ein düsteres Metropolis, in dem nichts
   und niemand wirklich sicher ist, in dem die Gewalt allgegenwärtig ist [...]

   3) Sin City (2005), IMDBid: None, Provider: VIDEOBUSTERMovie <movie>
   Inhalt: Willkommen in Sin City.  Diese Stadt begrüßt die Harten, die Korrupten,
   die mit den gebrochenen Herzen.  Einer von ihnen ist Marv [...]

   4) Sin City (2005), IMDBid: tt0401792, Provider: OMDBMovie <movie>
   Inhalt: Four tales of crime adapted from Frank Miller's popular comics focusing
   around a muscular brute who's looking for the person responsible for the [...]

   5) Sin City (2005), IMDBid: None, Provider: FILMSTARSMovie <movie>
   Inhalt: "Sin City" enthält drei lose verbundene und ineinander verschachtelt
   erzählte Episoden: Los geht es mit Hartigan (Bruce Willis) - einem Cop [...]

Hier die Suche kann wie die Optionen zeigen feingranularer konfiguriert werden,
was jedoch hier den Rahmen sprengen würde alle Optionen zu zeigen.

Unschärfesuche
~~~~~~~~~~~~~~

Ein nennenswertes Feature ist die Unschärfesuche. Die getesteten Tools haben
immer ein Problem damit Filme zu finden wenn der Titel nicht exakt geschrieben
ist. Das trifft auch in der Standardkonfiguration für libhugin zu, weil hier die
Webservices auf die man zugreift exakte Suchnegriffe erwarten.

.. code-block:: bash

   # Findet keine Ergebnisse, weil hier ,,Matrix'' flasch geschreiben ist
   gylfie -t "the marix" -a2

   # Mit dem aktivierten ,,Predator-Mode'' findet libhugin providerübergreifend
   # den gesuchten Film
   gylfie -t "the marix" -a2
   1) Matrix (1999), IMDBid: tt0133093, Provider: TMDBMovie <movie, picture>
   Inhalt: Der Hacker Neo wird übers Internet von einer geheimnisvollen Untergrund-
   Organisation kontaktiert.  Der Kopf der Gruppe - der gesuchte Terrorist [...]

   2) Matrix (1999), IMDBid: tt0133093, Provider: OFDBMovie <movie>
   Inhalt: Was ist die Matrix?  Diese Frage quält den Hacker Neo seit Jahren.  Er
   führt ein Doppelleben - tagsüber ist er Thomas Anderson und arbeitet in [...]

Suche über IMDBid
~~~~~~~~~~~~~~~~~

Normalerweise kann nur über die IMDBid gesucht werden wenn es die jeweilige
Plattform unterstützt. Deswegen funktioniert standardmäßig die Suche bei bei
Providern wie Filmstarts oder Videobuster nicht.


.. code-block:: bash

   # Findet keine Ergebnisse, weil Anbieter die Suche über IMDBid nicht
   # unterstützt
   $geri -i "tt0133093" -p videobustermovie -a 1

   # Mit dem ,,Lookup-Mode'' funktioniert auch die Suche über IMDBid bei
   # Anbietern die da normalerweise nicht unterstützen
   $geri -i "tt0133093" -p videobustermovie --lookup-mode
   1) Matrix (1999), IMDBid: None, Provider: VIDEOBUSTERMovie <movie>

   Inhalt: Der Hacker Neo (Keanu Reeves) wird übers Internet von einer
   geheimnisvollen Untergrund-Organisation kontaktiert.  Der Kopf der [...]

   [...]

Einsatz von Postprocessing Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ein noch nennenswertes Feature ist der Einsatz vom Composer Plugin. Dies
ermöglicht dem Benutzer das Ergebnis nach seinen Bedürfnissen zu komponieren und
besitzt die Fähigkeit das normalisierte Genre mehrerer Provider zusammenzuführen.

.. code-block:: bash

   # Zuerst passen wir unsere movie.mask an damit wir das Genre und das
   # normalisierte Genre sehen
   echo "{num}) {title} ({year}), IMDBid: {imdbid}, Provider: {provider}\
   \nGenre: {genre}\nGenre normalisiert: {genre_norm} \n\nInhalt: {plot}" > movie.mask

   geri -t "feuchtgebiete" -r composer -f userprofile -ptmdbmovie,ofdbmovie -a2


Freki
=====

Freki ist für Demonstrationszwecke und das Testen der libhugin analyze Library
entwickelt worden.

Übersicht der Optionen
----------------------

Folgend zum Überblick der Funktionalität die Hilfe des Kommandozeilentools
Freki:

.. code-block:: bash

   $python tools/freki
   Usage:
     freki create <database> <datapath>
     freki list <database>
     freki list <database> attr <attr>
     freki list <database> analyzerdata
     freki list-modifier | list-analyzer
     freki (analyze | modify) plugin <plugin> <database>
     freki (analyze | modify) plugin <plugin> pluginattrs <pluginattrs> <database>
     freki export <database>
     freki -h | --help
     freki --version

Freki erlaubt dem Benutzer eine ,,Datenbank'' aus externen Metadaten zu
generieren. Auf dieser Datenbank kann man folgend mit den Analyzern und
Modifiern die libhugin hier anbietet arbeiten und beispielsweise seine Metadaten
zu säubern. Ist man mit dem Gesamtergebnis zufrieden so kann die Datenbank
wieder ,,exportiert'' werden. Es werden die ,,neuen'' Metadaten in die
entsprechenden Metadatenfiles geschreiben.


Folgend eine kurze Demonstration des CLI--Tools.

Erstellen einer Datenbank
-------------------------

Hierzu wird die Helferfunktion (siehe Anhang)
verwendet. Im Odner ,,movies'' befinden sich zwei Filme die mit dem Xbox Meda
Center getaggt wurden.

.. code-block:: bash

    $freki create mydb.db ./movies


Datenbank Inhalt und Analyzer--Data anzeigens
---------------------------------------------

Datenbank anzeigen
~~~~~~~~~~~~~~~~~~

Listen des Inhalts der erstellten Datenbank. Der Plot wurde wegen der
Übersichtlichkeit gekürzt. Wie die Ausgabe zeigt wurden die Attribute title,
originaltitle, genre, director, year und plot eingelesen.

.. code-block:: bash

    $freki list mydb.db
    0) All Good Things (2010)
    {'director': 'Andrew Jarecki',
     'genre': ['Drama', 'Mystery', 'Suspense', 'Thriller'],
     'originaltitle': 'All Good Things',
     'plot': 'Historia ambientada en los años 80 y centrada en un heredero de
     una dinastía de Nueva York que se enamora de una chica de otra clase
     [..]',
     'title': 'All Beauty Must Die',
     'year': '2010'}

    1) Alien³ (1992)
    {'director': 'David Fincher',
     'genre': ['Action', 'Horror', 'Science Fiction'],
     'originaltitle': 'Alien³',
     'plot': 'Después de huir con Newt y Bishop del planeta Alien, Ripley se
     estrella con su nave en Fiorina 161, un planeta prisión. Desgraciadamente
     [...]',
     'title': 'Alien 3',
     'year': '1992'}

Analyzer--Data anzeigen
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $freki list mydb.db analyzerdata
    0) All Good Things (2010)
    {}
    1) Alien³ (1992)
    {}

Da noch nichts weiter analysiert wurde, sieht man hier nur *leere* Klammern.

Modifier/Analyzer anzeigen und anwenden
---------------------------------------

Analyzer und Modifier anzeigen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Anzeigen der vorhandenen Analyzer:

.. code-block:: bash

    $freki list-analyzer
    Name:       MovieFileAnalyzer
    Description:    Analayze movie files, extract video or audio information.
    Parameters:     {}

    Name:       PlotLang
    Description:    Analyzes the language of a given plot.
    Parameters:     {'attr_name': <class 'str'>}

Anzeigen der vorhandenen Modifier:

.. code-block:: bash

    $freki list-modifier
    Name:       PlotChange
    Description:    Allows to exchange plot to given language.
    Parameters:     {'attr_name': <class 'str'>, 'change_to': <class 'str'>}

    Name:       PlotCleaner
    Description:    Removes brackets e.g. brakets with actor name from plot.
    Parameters:     {'attr_name': <class 'str'>}


Anwenden von Analyzern und Modifiern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Anwenden von Analyzern
""""""""""""""""""""""

.. code-block:: bash

    # Anwenden des plotlang plugins auf der mydb.db Datenbank
    $freki analyze plugin plotlang mydb.db

    # Betrachten der Analyzer-Daten nach der Analyse
    $python tools/freki list mydb.db analyzerdata
    0) All Good Things (2010)
    {'PlotLang': 'es'}
    1) Alien³ (1992)
    {'PlotLang': 'es'}

Wie man nun sieht, wurde hier die verwendete Sprache der Plots analysiert. Das
Plugin hat sich in das Analyzerdata--Array mit seinem ermittelten Ergebnis
reingeschreiben.

Anwenden von Modifiern
""""""""""""""""""""""

.. code-block:: bash

    # Anwenden des PlotChange Modifier-Plugins um
    # die Sprache des Plots auf deutsch zu ändern
    $freki modify plugin plotchange pluginattrs attr_name='plot',change_to=de mydb.db


    # Betrachten der Metadaten nach Einsatz des Plugins
    $freki list mydb.db
    0) All Good Things (2010)
    {'director': 'Andrew Jarecki',
     'genre': ['Drama', 'Mystery', 'Suspense', 'Thriller'],
     'originaltitle': 'All Good Things',
     'plot': 'David Marks, Sohn einer reichen New Yorker Familie, verliebt sich
     in die junge Katie McCarthy, die nicht zu seinen Kreisen gehört. Doch dann [...]',
     'title': 'All Beauty Must Die',
     'year': '2010'}

    1) Alien³ (1992)
    {'director': 'David Fincher',
     'genre': ['Action', 'Horror', 'Science Fiction'],
     'originaltitle': 'Alien³',
     'plot': 'Nachdem Ellen Ripley, die kleine Newt, Soldat Hicks und der
     Android Bishop von LV 426 entkommen sind und sich mit dem Raumschiff USS [...]','
     'title': 'Alien 3',
     'year': '1992'}


Wie in dem Beispiel zu sehen ist wurde der Plot bei den Filme von der spanischen
Version auf eine deutsche Version geändert.

Exportieren der Daten
---------------------

Die modifzierten Metadaten können nun ins Produktivsystem zurückgespielt werden.
Dies geht bei Freki über die export Funktion, hier wieder wieder die o.g.
Helperfunktion verwendet.

.. code-block:: bash

    #Betrachten der des Plots der nfo-Dateien vor dem export (gekürzt)
    $cat movies/All\ Good\ Things\ \(2010\)/movie.nfo | grep plot
    <plot>Historia ambientada en los años 80 y centrada en un heredero de una
    dinastía de Nueva York que se enamora de una chica de otra clase social. [...]</plot>

    $freki export mydb.db
    ./movies/All Good Things (2010)/movie.nfo
    ./movies/Alien³ (1992)/movie.nfo

    #Betrachten der des Plots der nfo-Dateien nach dem export (gekürzt)
    $ cat movies/All\ Good\ Things\ \(2010\)/movie.nfo | grep plot
    <plot>David Marks, Sohn einer reichen New Yorker Familie, verliebt sich in
    die junge Katie McCarthy, die nicht zu seinen Kreisen gehört. [...]</plot>

Betrachtet man nun die nfo--Dateien der jeweiligen Filme, so sieht man dass
hier sich hier die Sprache von spanisch auf deutsch geändert hat.


Xbox Meda Center Plugin Integration
===================================

XBMC Plugin
-----------

Neben der Kommandozeilentools Geri und Freki wurde *konzeptuell* für das Xbox
Media Center ein Plugin (siehe Abb.: :num:`fig-xbmcscreenshot-hugin`) geschrieben das
libhugin als Metadaten--Dienst Nutzen kann.

Das XBMC erlaubt es sogenannte Scraper zu schreiben. Diese arbeiten vom
Grundprinzip ähnlich wie die Provider von libhugin. Das ,,Problem'' bei dessen
Scrapern ist, dass diese vollständig mittels Regulärer Ausdrücke innerhalb von
XML--Dateien geschrieben sind. Dies ist nach Meinung des Autors
fehleranfälliger, aufwändiger und nur schwer lesbar. Des Weiteren sind hier die
Möglichkeiten des Postprocessing nur begrenzt umsetzbar.

Die Referenzimplementierung des offiziellen TMDb--Scrapers hat insgesamt über 600
lines of code, recht kryptischer regulärer Ausdrücke (siehe X und Y). Die
Implementierung des libhugin Plugins in das XBMC hat an dieser Stelle nur 23
lines of code (siehe Z).  Das liegt daran, dass der libhugin Proxy hier dem XBMC
die Daten bereits im benötigten Format über das nfo OutputConverter--Plugin
liefern kann.


.. _fig-xbmcscreenshot-hugin:

.. figure:: fig/hugin_xbmc.png
    :alt: Libhugin im XBMC als Plugin
    :width: 70%
    :align: center

    libhugin im XBMC Scraper Meune.


libhugin--Proxy
---------------

Da die direkte Integration in das XBMC aufgrund der begrenzten Zeit der
Projektarbeit nicht möglich ist, wurde hier der Ansatz eines ,,Proxy--Dienstes''
angewandt. Für Libhugin wurde mittels dem Webframework Flask ein *minimalier*
Webservice geschreiben (siehe Anhang: hhh), welcher über eine eigens definierte
API Metadaten an das XBMC liefert.

Der Libhugin--Proxy zeigt konzeptuell die Integration von libhugin als
Netzwerkdienst, welcher eine RESTful API bereitstellt. Der implementierte
Test--API bietet die folgenden Schnittstellen:

    * ``/search/<titlename or imdbid>``, Suche nach Film über Titel oder IMDBid
    * ``/movie/<position>``, Zugriff auf einen bestimmten Film
    * ``/stats``, Server ,,Statistik'', welche zeigt ob Postprocessing aktiviert ist
    * ``/toggle_pp``, Postprocessing aktivieren/deaktivieren
    * ``/shutdown``, Server herunterfahren

Die Implementierung des Proxy zeigt, dass es problemlos möglich ist mit relativ
wenig Aufwand, libhugin als ,,neuen'' Dienst für Multimedia--Anwendungen und
auch Metadaten Management Tools zu verwenden.

Hierbei kommt die Flexibilität und Anpassbarkeit des System den bisherigen Tools
zu gute. Auf diese Art und Weise lassen sich alle Postprocessing Verfahren und
Features die libhugin bietet in bereits existierende Tools integrieren.

Unterschiede TMDb XBMC und TMDb libhugin
----------------------------------------

Im Vergleich zum XBMC TMDb--Scraper bietet der libhugin XBMC Scraper (Provider
zum Testen auch auf nur TMDb konfiguriert) zusätzliche Features.

    * Suche über IMDBid möglich
    * Unschärfesuche möglich, dadurch auch erhöhte Trefferquote
    * Postprocessing, je nach dazugeschalteten Plugin möglich

Beim Nutzen weiter Provider sowie Plugins wie dem Composer Plugin eröffnen sich
hier für das XBMC ganz neue Möglichkeiten seine Metadaten nach den eigenen
Wünschen ,,zusammen zu bauen'' ohne Dabei auf externe Video Metadaten Management
Tools zugreifen zu müssen.

Weitere Einsatzmöglichkeiten
============================

Scripting Tasks
---------------

Die Einsatzmöglichkeiten sind je nach Szenario anpassbar. Für einfache
Anwendungen lassen sich auch Geri und Freki bereits direkt verwenden.

Ein schönes Beispiel für einen Scripting--Task ist das ,,normalisieren'' der
Ordnerstruktur/Benennung von großen Filmesammlungen.

Hierzu reicht es einfach die ,,movie.mask'' von Geri anzupassen und ein kleines
Bash--Script zu schreiben:

.. code-block:: bash

   # Anpassen unserer movie.mask
   $echo "{title} ({year}), [{imdbid}]" > tools/geri/movie.mask

   # So schaut das minimalistiche rename script aus
   #!/bin/bash

   for movie in $1/*; do
       old_name=$(basename "$movie")
       new_name=$(geri -t "$old_name" -P --language=en -a1 -p tmdbmovie);
       mv -v "$f" "$1/$new_name";
   done


Um eine schlampig gepflegte Filmesammlung zu ,,simulieren'', erstellen wir
einfach ein paar Ordner mit Filmen die falsch geschrieben sind und lassen unser
Script laufen:

.. code-block:: bash

   $mkdir movies/{"alien1","alien 2","geständnisse","ironman2","iron man3","iron men 1",\
   "jung unt schon","marix","oonly good forgives","teh marix 2"}

   $ ./rename.sh movies
   ‘movies/alien1’ -> ‘movies/Alien (1979), [tt0078748]’
   ‘movies/alien 2’ -> ‘movies/Aliens (1986), [tt0090605]’
   ‘movies/geständnisse’ -> ‘movies/Confessions (2010), [tt1590089]’
   ‘movies/ironman2’ -> ‘movies/Iron Man 2 (2010), [tt1228705]’
   ‘movies/iron man3’ -> ‘movies/Iron Man 3 (2013), [tt1300854]’
   ‘movies/iron men 1’ -> ‘movies/Iron Man (2008), [tt0371746]’
   ‘movies/jung unt schon’ -> ‘movies/Young & Beautiful (2013), [tt2752200]’
   ‘movies/marix’ -> ‘movies/The Matrix (1999), [tt0133093]’
   ‘movies/oonly good forgives’ -> ‘movies/Only God Forgives (2013), [tt1602613]’
   ‘movies/teh marix 2’ -> ‘movies/The Matrix Reloaded (2003), [tt0234215]’


An diesem Beispiel sieht man wie ,,gut'' die Unschärfesuche funktionieren kann.
Bei diesem kleinem Testsample haben wir eine Trefferwahrscheinlichkeit von 100%.


D--Bus
------


Eine weitere Möglichkeit neben dem ,,Proxy--Server--Ansatz'' wäre D--Bus zu
verwenden. DBus ist ein Framework das unter Linux zur Interprocesskommunikation
verwendet wird. Man kann hier beispielsweise libhugin als D--Bus--Service laufen
lassen und jede andere beliebige Anwendung hätte die Möglichkeit
programmiersprachenunabhängig mit libhugin zu kommunizieren.


libnotify
---------

Ein weiterer Ansatz libhugin zu nutzen wäre über *libnotify* denkbar. Das ist
eine Library die Änderungen am Dateisystem erkennt. Man kann hier z.B. einen
bestimmten Ordner "monitoren" indem man ,,inofitywatch'' auf diesem Ordner
,,lauschen'' lässt. Hier wäre z.B. ein Szenario denkbar, dass sobald man eine
Videodatei in einen bestimmten Ordner kopiert hat bzw. diese nach dem
Aufzeichnet beispielsweise mit einem VDR in einen bestimmten Ordner
verschoben wurde, man dann einfach über libnotifywatch ein Script ,,triggert''
welches einen Ordner anlegt, die Datei und Ordner umbenennt und die
entsprechenden Metadaten für den Film sucht und im Ordner ablegt.
