#######
Entwurf
#######

Im Folgenden wird der systematische Entwurf der Software aufgezeigt. Die
verwendeten Algorithmen, Probleme, sowie Möglichkeiten der technischen
Umsetzung werden in der Bachelorarbeit genauer beleuchtet und diskutiert.

Grundüberlegungen
=================

Grundprinzip -- Beschaffung der Metadaten
-----------------------------------------

Metadaten werden über verschiedene Onlinequellen bezogen. Hier wird
grundsätzlich zwischen Onlinequellen mit API und ohne API unterschieden.
Onlinequellen mit API bieten dem Entwickler direkt eine Schnittstelle, über
welche die interne Datenbank des Metadatenanbieters abgefragt werden kann. Die
Onlinequellen mit API unterteilen sich in die zwei Technologien RESTful (vgl.
:cite:`fielding2000architectural`) und SOAP (vgl. :cite:`snell2002webservice`).

Folgende Shellsitzung demonstriert einen Zugriff mit dem Webtransfer--Tool
*cURL* (siehe :cite:`curl`) auf die API der OMDb--Onlinequelle (siehe
:cite:`omdb`), es wird nach dem Film ,,The Matrix'' gesucht (Ausgabe gekürzt):

.. code-block:: bash

   $ curl http://www.omdbapi.com/?t=The+Matrix
   {"Title":"The Matrix",
   "Year":"1999",
   "Runtime":"136 min",
   "Genre":"Action, Sci--Fi",
   "Director":"Andy Wachowski, Lana Wachowski",
   "Actors":"Keanu Reeves, Laurence Fishburne, Carrie--Anne Moss, Hugo Weaving",
   "Plot":"A computer hacker learns from mysterious [...]",
   "Country":"USA, Australia",
   "Poster":"http://ia.media-imdb.com/images/M/SX300.jpg",
   "imdbRating":"8.7",
   "imdbID":"tt0133093",
   [...]
   "Type":"movie",
   "Response":"True"
   }

Die *Such--URL* bekommt den Titel als Query--Parameter (``t=The+Matrix``)
übergeben, zurück kommt ein in *JSON* formatiertes Response. Dieses kann nun vom
Aufrufer der API beliebig verarbeitet werden.

Bietet eine Webseite wie beispielsweise *filmstarts.de* (siehe
:cite:`filmstarts`) keine API an, so muss der ,,normale Weg" wie über den
Webbrowser erfolgen. Hierzu muss man herausfinden, aus welchen Parametern sich
die *Such--URL* zusammensetzt, die im Hintergrund an den Webserver geschickt
wird sobald die Suchanfrage losgeschickt wird. Bei *filmstarts.de* setzt sich
die *Such*--URL wie folgt zusammen:

    ``http://www.filmstarts.de/suche/?q=Filmtitel``

Wird nun mit *cURL* die URL mit dem oben genannten Film als Query--Parameter
aufgerufen, so kommt als Antwort ein HTML--Dokument zurück, welches auch der
Webbrowser erhalten würde. Folgende Shellsitzung demonstriert den Aufruf
(Ausgabe gekürzt):

.. code-block:: bash

   $ curl  http://www.filmstarts.de/suche/?q=The+Matrix
   <html>
       <head><title>The Matrix – Suchen auf FILMSTARTS.de</title>
       [content ... ]
   </html>

Man bekommt als Aufrufer der URL die Webseite zurückgeliefert und muss nun die
Daten aus dem Dokument extrahieren. Dies ist in der Regel mühsamer, wie der
Zugriff über eine API, welche die Daten sauber im *JSON*-- oder *XML*--Format
zurückliefert.


Übertragung vom Grundprinzip auf das Pluginsystem
-------------------------------------------------

Ein Ziel bei der Entwicklung der Plugin--Spezifikation ist, den Aufwand für das
Implementieren eines Plugins so gering wie möglich zu halten, um Programmfehler
beziehungsweise Fehlverhalten durch Plugins zu minimieren, aber auch um
Entwickler zu motivieren, Plugins zu schreiben.

Das oben genannte Prinzip beim Beschaffen von Metadaten ist immer gleich und
lässt sich somit gut auf das Pluginsystem übertragen. Die Provider--Plugins
müssen im Prinzip nur folgende zwei Punkte können (siehe Abbildung
:num:`fig-provider-concept`):

    * Aus den Suchparametern die *Such--URL* zusammenbauen.
    * Extrahieren der Daten aus dem zurückgelieferten *HTTP--Response*.

Um den Download selbst muss sich das Provider--Plugin bei diesem Ansatz nicht
kümmern, das entlastet den Pluginentwickler und übergibt *libhugin* die
Kontrolle über das Downloadmanagement.

.. _fig-provider-concept:

.. figure:: fig/provider-concept-svg.pdf
    :alt: Grundprinzip Kommunikationsablauf mit Provider--Plugin
    :width: 90%
    :align: center

    Grundprinzip Kommunikationsablauf mit Provider--Plugin.


Damit der Provider weiß, welche *Roh--Daten* er zurückliefern soll, muss
hierfür noch eine Struktur mit Attributen festgelegt werden, an welche sich alle
Provider--Plugins halten müssen.

Für den Prototypen richten sich die möglichen Attribute nach der
TMDb--Onlinequelle (siehe *libhugin*--API :cite:`movieprovider`).


Libhugin Architektur Überblick
==============================

Die Bibliothek soll über die Metadatenbeschaffung hinaus Werkzeuge zur
Metadatenanalyse bereitstellen. Um eine saubere Trennung zwischen
den beiden zu schaffen, wird die Bibliothek in die zwei Teile
*libhugin--harvest* und *libhugin--analyze* aufgeteilt (siehe Abbildung
:num:`fig-harvest-arch`).

**libhugin--harvest**

Dieser Teil soll für die Metadatenbeschaffung zuständig sein und Schnittstellen
für die folgenden Pluginarten bereitstellen:

    * Provider
    * Postprocessor
    * Converter

.. _fig-harvest-arch:

.. figure:: fig/arch-overview-svg.pdf
    :alt: Architekturübersicht von libhugin
    :width: 80%
    :align: center

    Die Grafik zeigt eine Architekturübersicht der *libhugin*--Bibliothek welche
    sich in die zwei Teile *libhugin--harvest* und *libhugin--analyze* aufteilt.

**libhugin--analyze**

Dieser Teil soll für die nachträgliche Metadatenanalyse zuständig sein und
Schnittstellen für folgende Pluginarten bereitstellen:

    * Modifier
    * Analyzer
    * Comparator

Der Analyze--Teil der Bibliothek soll eine interne Datenbank besitzen, in welche
externe Metadaten zur Analyse importiert werden. So können alle Plugins auf
einem *definierten* Zustand arbeiten.

Klassenübersicht *libhugin--harvest*
------------------------------------

Die Architektur von *libhugin* ist objektorientiert. Aus der Architekturübersicht
und den Anforderungen an das System wurden folgende Klassen und Schnittstellen
abgeleitet, Abbildung :num:`fig-klassenuebersicht-harvest` zeigt eine
Klassenübersicht von *libhugin--harvest* samt Interaktion mit den Schnittstellen.

Im Folgenden werden die grundlegenden Objekte und Schnittstellen
erläutert.

.. _fig-klassenuebersicht-harvest:

.. figure:: fig/klassenuebersicht-harvest-svg.pdf
    :alt: Libhugin--harvest Klassenübersicht mit Klasseninteraktion
    :width: 100%
    :align: center

    *Libhugin--harvest* Klassenübersicht mit Klasseninteraktion.


**Session**

Diese Klasse bildet den Grundstein für *libhugin--harvest*. Über eine Sitzung
konfiguriert der Benutzer das System und hat Zugriff auf die verschiedenen
Plugins.

Von der Session werden folgende Methoden bereitgestellt:

``create_query(**kwargs):`` Schnittstelle zur Konfiguration der Suchanfrage. Die
Methode gibt ein Query--Objekt zurück, das einem Python Dictionary (Hashtabelle)
entspricht.  Diese Methode dient als Hilfestellung für den Benutzer der API.
Theoretisch kann der Benutzer die Query auch manuell zusammenbauen. ``Kwargs``
ist eine optionale Liste aus Key--Value--Paaren. Für weitere Informationen und
Konfigurationsparameter siehe *libhugin*--API :cite:`queryapi`.


``submit(query):`` Schnittstelle um eine Suchanfrage zu starten. Die Methode
gibt eine Liste mit gefundenen Metadaten als *Ergebnisobjekte* zurück.

Die Methode initialisiert eine Downloadqueue und einen Zwischenspeicher (Cache),
falls dieser vom Benutzer über die Query nicht deaktiviert wurde. Anschließend
generiert sie für jeden Provider eine sogenannte *Job*--Struktur. Diese
*Job*--Struktur kapselt jeweils einen Provider, die Suchanfrage und die
Zwischenergebnisse, die während der Suchanfrage generiert werden.

Zur Veranschaulichung, eine leere *Job*--Struktur in Python--Notation:

.. code-block:: python

    job_structure = {
        'url': None,          # URL die als nächstes von Downloadqueue geladen werden soll
        'provider': None,     # Referenz auf Provider--Plugin
        'future': None,       # Referenz auf Future Objekt bei async. Ausführung
        'response': None,     # Ergebnis des Downloads, Http Response
        'return_code': None,  # Return Code der Http Anfrage
        'retries_left': None, # Anzahl der noch übrigen Versuche
        'done': None,         # Flag das gesetzt wird wenn Job fertig ist
        'result': None        # Ergebnis der Suchanfrage
    }

Nachdem ein Job fertiggestellt wurde, wird er in ein *Ergebnisobjekt* gekapselt.
Am Ende der ``submit()``--Methode wird eine Liste mit *Ergebnisobjekten*
an den Aufrufer zurückgegeben. Das *Ergebnisobjekt* kapselt die folgenden
Informationen:

    * Provider, welcher das Ergebnis geliefert hat.
    * Suchparemeter, welche für die Suchanfrage verwendet wurden.
    * Metadatenart, Movie oder Person.
    * Anzahl der Downloadversuche.
    * Das eigentliche Ergebnis als Hashtabelle.


Der prinzipielle Ablauf der ``submit()``--Methode wird in Abbildung
:num:`fig-submit` dargestellt.

.. _fig-submit:

.. figure:: fig/submit.pdf
    :alt: Prinzipieller Ablauf der Submit Methode
    :width: 50%
    :align: center

    Prinzipieller Ablauf der Submit Methode.

``submit_async()``: Methode für eine asynchrone Nutzung der API. Diese führt
``submit()`` asynchron aus und gibt ein Python *Future--Objekt* zurück,
welches die Anfrage kapselt. Durch Aufrufen der ``done()``--Methode auf dem
*Future--Objekt*, kann festgestellt werden ob die Suchanfrage bereits fertig ist.
Ein Aufruf der ``result()``--Methode auf dem *Future--Objekt* liefert das
eigentliche *Ergebnisobjekt* zurück. Für mehr Informationen siehe Python API
:cite:`futures`.

``provider_plugins(pluginname=None)``: Diese Methode gibt eine Liste mit den
Provider--Plugins zurück oder bei Angabe eines Plugins, dieses direkt. Mit
``pluginname=None`` wird der Standardwert gesetzt, falls kein Wert übergeben
wird.

``postprocessor_plugins(pluginname=None)``: Analog zu ``provider_plugins()``.

``converter_plugins(pluginname=None)``: Analog zu ``provider_plugins()``.

``cancel()``: Diese Methode dient zum Abbrechen einer asynchronen Suchanfrage.
Hier sollte anschließend noch die ``clean_up()``--Methode aufgerufen werden um
alle Ressourcen wieder freizugeben.

``clean_up()``: Methode zum Aufräumen nach dem Abbrechen einer asynchronen
Suchanfrage. Die Methode blockt solange noch nicht alle Ressourcen freigegeben
wurden.

**Queue**

Die Queue kapselt die Parameter der Suchanfrage. Sie wird direkt mit
den Parametern der Suchanfrage instanziiert, hierbei werden bestimmte Werte, die
übergeben werden, validiert und *Standardwerte* gesetzt.


**Cache**

Der Cache wird intern verwendet, um erfolgreiche Suchanfragen persistent
zwischenzuspeichern. So können die Daten bei wiederholter Anfrage aus dem Cache
geladen werden. Dadurch gewinnt man Geschwindigkeit und der Metadatenanbieter
wird entlastet. Zum persistenten Speichern wird ein Python Shelve (siehe
:cite:`shelve`) verwendet.

``open(path, cache_name)``: Öffnet den übergebenen Cache.

``read(key)``: Liest Element an Position *key* aus dem Cache.

``write(key, value)``: Schreibt das Element *value* an Position *key* in den
Cache.

``close()``: Schließt den Cache.


**Downloadqueue**

Die Downloadqueue ist für den eigentlichen Download der Daten zuständig. Sie
arbeitet mit den oben genannten *Job*--Strukturen. Die Provider--Plugins müssen
so keine eigene Downloadqueue implementieren.

``push(job)``: Fügt einen `Job` der Downloadqueue hinzu.

``pop()``: Holt den nächsten fertigen `Job` aus der Downloadqueue.

``running_jobs()``: Gibt die Anzahl der `Jobs` die in Verarbeitung sind zurück.


**GenreNormalize**

GenreNormalize kann von den Provider--Plugins verwendet werden, um das Genre zu
normalisieren. Hierzu müssen die Provider eine Genre--Mapping--Datei erstellen.
Für mehr Informationen siehe auch API :cite:`movieprovider`.

``normalize_genre(genre)``: Normalisiert ein Genre anhand einer festgelegten
Abbildungstabelle.

``normalize_genre_list(genrelist)``: Normalisiert eine Liste aus Genres jeweils
mittels der ``normalize_genre()`` Funktion.

Die Problematik der Genrenormalisierung ist Bestandteil der Bachelorarbeit.



**PluginHandler**

Das Pluginsystem wurde mit Hilfe der *Yapsy*--Bibliothek (siehe
:cite:`yapsy`) umgesetzt. Es bietet folgende Schnittstellen nach außen:

``activate_plugin_by_category(category)``: Aktiviert Plugins einer bestimmten
Kategorie.

``deactivate_plugin_by_category(category)``: Deaktiviert Plugins einer bestimmten
Kategorie.

``get_plugins_from_category(category)``: Liefert Plugins einer bestimmten
Kategorie zurück.

``is_activated(category)``: Gibt einen Wahrheitswert zurück, wenn eine Kategorie
bereits aktiviert ist.


Plugininterface libhugin--harvest
---------------------------------

*Libhugin--harvest* bietet für jeden Plugintyp eine bestimmte Schnittstelle an,
die vom jeweiligen Plugintyp implementiert werden muss (siehe Abbildung :num:`fig-harvest`).

.. _fig-harvest:

.. figure:: fig/harvest-plugin-interface.pdf
    :alt: Libhugin--harvest Plugin Schnittstellenbeschreibung
    :width: 100%
    :align: center

    Libhugin--harvest Plugin Schnittstellenbeschreibung.


Diese *libhugin--harvest* Plugins haben die Möglichkeiten von verschiedenen
Oberklassen abzuleiten (siehe Abbildung :num:`table-harvest-plugins`).
Mehrfachableitung ist unter Python möglich.

.. figtable::
    :label: table-harvest-plugins
    :spec: l|l|l|l
    :caption: Libhugin Plugininterfaces für die verschiedenen libhugin--harvest Plugins.
    :alt: Libhugin Plugininterfaces für die verschiedenen libhugin--harvest Plugins

    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *Schnittstellenname*     | *text*             | *grafisch*         | *Beschreibung*                                       |
    +==========================+====================+====================+======================================================+
    | *IMovieProvider*         | :math:`\checkmark` |                    | Provider--Plugins, liefert Filmmetadaten             |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *IMoviePictureProvider*  |                    | :math:`\checkmark` | Provider--Plugins, liefert Filmmetadaten             |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *IPersonProvider*        | :math:`\checkmark` |                    | Provider--Plugins, liefert Personenmetadaten         |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *IPersonPictureProvider* |                    | :math:`\checkmark` | Provider--Plugins, liefert Personenmetadaten         |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *IPostProcessor*         |                    |                    | Postprocessor--Plugins für Metadatennachbearbeitung  |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+
    | *IConverter*             |                    |                    | Converter--Plugins für verschiedene Metadatenformate |
    +--------------------------+--------------------+--------------------+------------------------------------------------------+


Plugins, die für die Metadatenbeschaffung zuständig sind, müssen von den
Providerklassen ableiten (siehe Abbildung :num:`table-harvest-plugins`). Des
Weiteren müssen diese Plugins die folgenden Methoden implementieren:

``build_url(search_params)``: Diese Methode bekommt die *Such--Parameter*
übergeben und baut aus diesen die *Such--URL* zusammen.
Für weitere Informationen siehe auch API :cite:`buildurl`.

``parse_response(response, search_params)``: Diese Methode bekommt die
HTTP--Response zu der vorher von ``build_url(search_params)`` erstellten
*Anfrage--URL*. Die Methode ist für das Extrahieren der Attribute aus dem Response
zuständig. Sie gibt entweder eine neue URL zurück, die angefordert werden soll,
oder befüllt eine Hashtabelle mit gefundenen Attributen und gibt diese zurück.
Für weitere Informationen siehe auch *libhugin*--API :cite:`parseresponse`.

``supported_attrs()``: Diese Methode gibt eine Liste mit Attributen zurück die
vom Provider befüllt werden.



Plugins, die für die Metadatennachbearbeitung zuständig sind, müssen von
*IPostProcessor* ableiten (siehe Abbildung :num:`table-harvest-plugins`).
Des Weiteren müssen diese Plugins die folgenden Methoden implementieren:

``process(results, **kwargs)``: Diese Methode bekommt ein Liste mit
*Ergebnisobjekten* übergeben und manipuliert dieses nach bestimmten Kriterien
oder gibt eine neue Liste mit *Ergebnisobjekten* zurück.

``parameters()``: Die Methode listet die Keyword--Argumente für ein
*Postprocessor*--Plugin.


Plugins, die für das Konvertieren der Ergebnisse in bestimmte Metadatenformate
zuständig sind, müssen von *IConverter* ableiten (siehe Abbildung
:num:`table-harvest-plugins`).  Des Weiteren müssen diese Plugins die folgenden
Methoden implementieren:

``convert(results, **kwargs)``: Diese Methode bekommt ein *Ergebnisobjekt*
übergeben und gibt die String--Repräsentation von diesem in einem spezifischen
Metadatenformat wieder.

``parameters()``: Die Methode listet die Keyword--Argumente für ein
Converter--Plugin.

Klassenübersicht *libhugin--analyze*
------------------------------------

Dieser Teil der *libhugin*--Bibliothek ist für die nachträgliche Metadatenaufbereitung
zuständig (siehe Abbildung :num:`fig-klassenuebersicht-analyze`).

.. _fig-klassenuebersicht-analyze:

.. figure:: fig/klassenuebersicht-analyze-svg.pdf
    :alt: Libhugin--analyze Klassenübersicht und Interaktion
    :width: 100%
    :align: center

    *Libhugin--analyze* Klassenübersicht mit Klasseninteraktion.



**Session**

Diese Klasse bildet den Grundstein für *libhugin--analyze*. Sie stellt analog
zur *libhugin--harvest* Session die API bereit.

``add(metadata_file, helper)``: Diese Methode dient zum Importieren externer
Metadaten. Sie erwartet eine Datei mit Metadaten (`metadata_file`) und als
Callback--Funktion eine *Helferfunktion* welche weiß, wie die Metadaten zu
extrahieren sind.

Kurzer Exkurs zur *Helferfunktion*. Die *Helferfunktion* hat folgende
Schnittstelle:

    ``helper_func(metadata, attr_mask)``

Der ``attr_mask`` Parameter gibt die Abbildungen der Attribute zwischen der
*externen* und *internen* Datenbank an.

Wir nehmen an unsere Metadaten sind im *JSON*--Format gespeichert, beim Einlesen
der *JSON--Datei* wird diese zu einer :term:`Hashtabelle` konvertiert, die wie
folgt aussieht:

.. code-block:: bash

    metadata_the_movie = {
        'Filmtitel' = 'The Movie',
        'Erscheinungsjahr' = '2025',
        'Inhaltsbeschreibung' = 'Es war einmal vor langer langer Zeit...'
    }

Folgendes Python--Snippet zeigt nun die Funktionalität der *Helferfunktion*,
welche die Abbildung von externer Quelle auf die interne Datenbank verdeutlicht:

.. code-block:: python

    attr_mask = {
        'Filmtitel': 'title',
        # Filmtitel = Attributname unter welchem der Filmtitel
        # in der externen Metadatendatei hinterlegt ist
        # title = Attributname unter dem der Titel
        # in der internen Datenbank abgelegt werden soll
        #
        # folgenden zwei Attribute analog zum Filmtitel
        'Erscheinungsjahr' = 'year',
        'Inhaltsbeschreibung': 'plot'
    }

   def helper(metadata, attr_mask):
       internal_repr = {}

       for metadata_key, internal_db_key in attr_mask.items():
           internal_repr[internal_db_key] = metadata[metadata_key]

       return internal_repr


Weitere Methoden der Session Klasse:

``analyzer_plugins(pluginname=None)``: Liefert eine Liste mit den vorhandenen
Analyzer--Plugins zurück. Bei Angabe eines bestimmten Pluginnamen, wird dieses
Plugin direkt zurückgeliefert.

``modifier_plugins(pluginname=None)``: Analog zu
``analyzer_plugins()``.

``comparator_plugins(pluginname=None)``: Analog zu
``analyzer_plugins()``.

Folgende weitere Methoden erlauben es, die *libhugin--analyze* Plugins auf *externe*
Daten anzuwenden:

``analyze_raw(plugin, attr, data)``: Wrapper Methode, welche es erlaubt die
Analyzer--Plugins auf *externen* Daten auszuführen.

``modify_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``compare_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``get_database()``: Liefert die interne Datenbank (Python Dictionary) zurück.


Für das Öffnen und Schließen der internen Datenbank der Session gibt es folgende
zwei Methoden:

``database_open(databasename)``: Lädt die angegebene Datenbank.

``database_close()``: Schließt und schreibt die aktuelle Datenbank persistent auf
die Festplatte.


**Movie**

Die Movie Klasse repräsentiert ein Metadatenobjekt welches in der internen
Datenbank zur Analyse gespeichert wird. Es enthält folgende Attribute:

    * Schlüssel, über den die Metadaten eindeutig zugeordnet werden können.
    * Pfad zur Metadatendatei.
    * Hashtabelle mit den Metadaten.
    * Hashtabelle mit Analyzer--Analysedaten.
    * Hashtabelle mit Comparator--Analysedaten.


**PluginHandler**

Die PluginHandler--Klasse hat analog zum *libhugin--harvest* die folgenden
Schnittstellen:

``activate_plugin_by_category(category)``: Aktiviert Plugins einer bestimmten
Kategorie.

``deactivate_plugin_by_category(category)``: Deaktiviert Plugins einer bestimmten
Kategorie.

``get_plugins_from_category(category)``: Liefert Plugins einer bestimmten
Kategorie zurück.

``is_activated(category)``: Gibt einen Wahrheitswert zurück, wenn eine Kategorie
bereits aktiviert ist.

Plugininterface libhugin--analyze
---------------------------------

*Libhugin--analyze* bietet für jeden Plugintyp eine bestimmte Schnittstelle an,
die vom jeweiligen Plugintyp implementiert werden muss (siehe Abbildung :num:`fig-analyze`).

.. _fig-analyze:

.. figure:: fig/analyze-plugin-interface.pdf
    :alt: Libhugin--analyze Plugin Schnittstellenbeschreibung
    :width: 100%
    :align: center

    Libhugin--analyze Plugin Schnittstellenbeschreibung.


Die *libhugin--analyze* Plugins haben die Möglichkeiten, von den folgenden
Oberklassen abzuleiten. Mehrfachableitung ist unter Python möglich:

.. figtable::
    :label: table-analyze-plugins
    :spec: l|l|
    :caption: Libhugin Plugininterfaces für die verschiedenen libhugin--analyze Plugins.
    :alt: Libhugin Plugininterfaces für die verschiedenen libhugin--analyze Plugins

    +----------------------+-------------------------------------------------------------------------+
    | *Schnittstellenname* | *Beschreibung*                                                          |
    +======================+=========================================================================+
    | *IModifier*          | Modifier--Plugins, die Metadaten direkt modifizieren.                   |
    +----------------------+-------------------------------------------------------------------------+
    | *IAnalyzer*          | Analyzer--Plugins, die für die Analyse der Metadaten zuständig sind.    |
    +----------------------+-------------------------------------------------------------------------+
    | *IComparator*        | Comparator--Plugins, die Metadaten für statistische Zwecke vergleichen. |
    +----------------------+-------------------------------------------------------------------------+



Plugins, die Metadaten modifizieren, müssen von *IModifier* ableiten (siehe
Tabelle :num:`table-analyze-plugins`). Diese Plugins müssen folgende Methoden
implementieren:

``modify(movie, **kwargs)``: Die Standardmethode für Modifierplugins. Die
Methode bekommt ein *Movie--Objekt* und optional Keyword--Argumente übergeben.
Die nötigen Keyword--Argumente können über die ``parameters()``--Methode erfragt
werden.

``modify_all(database, **kwargs)``: Analog zur ``modify(movie,
kwagrs)``--Methode. Diese Methode arbeitet jedoch nicht mit nur einem Movie
Objekt sondern mit der ganzen ,,Datenbank".

``parameters()``: Die Methode listet die Keyword--Argumente für ein Modifierplugin.


Plugins, die für die Analyse der Metadaten zuständig sind, müssen von *IAnalyzer*
ableiten (siehe Abbildung :num:`table-analyze-plugins`). Diese Plugins schreiben
ihre Analysedaten in das *Analyzerdata*--Attribut des *Movie--Objekts*.  Sie
müssen folgende Methoden implementieren:

``analyze(movie, **kwargs)``: Die Standardmethode für Analyzerplugins. Die
Anwendung hier ist analog den Modifierplugins.

``analyze_all(database, **kwargs)``: Analog Modifierplugins.

``parameters()``: Analog Modifierplugins.

Plugins, die Metadaten für statistische Zwecke analysieren und vergleichen
können, müssen von *IComparator* ableiten (siehe Abbildung
:num:`table-analyze-plugins`). Des Weiteren müssen diese Plugins folgende
Methoden implementieren:

``compare(movie_a, movie_b, **kwargs)``: Die Standardmethode für
Comparatorplugins. Diese erwartet als Parameter zwei *Movie--Objekte*, die
verglichen werden sollen. Die Keyword--Argumente können analog den Modifier--
und Analyzerplugins verwendet werden.

``compare_all(database, **kwargs)``: Diese Methode vergleicht alle
*Movie--Objekt* Kombinationen aus der Datenbank.

``parameters()``: Analog Modifier-- und Analyzerplugins.


Bibliothek Dateistruktur
========================

Die folgende Auflistung zeigt die Ordnerstruktur der Bibliothek.  Normalerweise
enthält unter Python jeder Ordner eine `__init__.py--Datei` welche diesen Ordner
dann als Modul erscheinen lässt. Diese wurden wegen der Übersichtlichkeit
weggelassen.

.. code-block:: python

    hugin
    |-- harvest/                           # *libhugin--harvest* Ordner
    |   |-- session.py                     # Implementierungen der Session
    |   |-- query.py                       # Implementierungen der Query
    |   |-- cache.py                       # Implementierungen vom Cache
    |   |-- downloadqueue.py               # Implementierungen der Downloadqueue
    |   |-- pluginhandler.py               # Implementierungen vom PluginHandler
    |   |
    |   |-- converter/                      # Ordner für Converter--Plugins
    |   |-- postprocessor/                  # Ordner für Postprocessor--Plugins
    |   |-- provider/                       # Ordner für Provider--Plugins
    |   |   |-- genrefiles/                 # Genre Dateien für ,,Normalisierung"
    |   |   |   |-- normalized_genre.dat    # Globale Normalisierungstabelle Genre
    |   |   |-- result.py                   # Implementierung ,,ErgebnisObjekt"
    |   |   |-- genrenorm.py                # Implementierung Genrenormalisierung
    |-- utils/                              # Gemeinsame Hilfsfunktionen
    |   |-- logutil.py
    |   |-- stringcompare.py
    |
    |-- analyze/                            # *libhugin--analyze* Ordner
    |   |-- session.py                      # Implementierungen der o.g. Klassen
    |   |-- movie.py                        # Implementierung des ,,Movie'' Objektes
    |   |-- pluginhandler.py
    |   |-- rake.py                         # Implementierung Rake Algorithmus
    |   |-- analyzer/                       # Ordner für Analyzer--Plugins
    |   |-- comparator/                     # Ordner für Comparator--Plugins
    |   |-- modifier/                       # Ordner für Modifier--Plugins
    |-- filewalk.py                         # Helferfunktion für Import/Export
