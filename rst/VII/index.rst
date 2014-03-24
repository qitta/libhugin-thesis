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


Das Tool eignet sich neben dem Einsatz als Testwerkzeug für Library und Plugins
auch gut für Scripte und somit für automatische Verarbeitung *großer*
Datenmengen.

Im Angang C wird die Anewendung Anhand von Beispielen demonstriert.


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


Implementierung von libhugin in das Open Source Projekt XBMC
============================================================

Neben der Kommandozeilentools Geri und Freki wurde konzeptuell für das Xbox
Media Center ein Plugin geschreiben das libhugin als Metadaten--Dienst Nutzen
kann.


Da die direkte Integration in das XBMC aufgrund der begrenzten Zeit der
Projektarbeit nicht möglich ist, wurde hier der Ansatz eines ,,Proxy--Dienstes''
angewandt. Für Libhugin wurde mittels dem Webframework Flask ein *minimalier*
Webservice geschreiben, welcher über eine eigenst definierte API Metadaten an
das XBMC liefert.

* xbmc plugin
* vor und nachteile

Weitere Einsatzmöglichkeiten
============================

* libnotify
* scripting


