#######
Entwurf
#######

Im Folgenden wird der systematische Entwurf der Software dargestellt. Die
verwendeten Algorithmen, Probleme, sowie Möglichkeiten der technischen
Umsetzung werden in der Bachelorarbeit genauer beleuchtet und diskutiert.

Grundüberlegungen
=================

Grundprinzip -- Beschaffung der Metadaten
-----------------------------------------

Metadaten werden über verschiedene Onlinequellen bezogen. Hier wird
grundsätzlich zwischen Onlinequellen mit API und ohne API unterschieden.
Onlinequellen mit API bieten dem Entwickler direkt eine Schnittstelle über die, die
interne Datenbank des Metadatenanbieters abgefragt werden kann.

Folgendes Bash--Snippet demonstriert einen Zugriff mit dem Webtransfer--Tool
*cULR* (siehe :cite:`curl`) auf die API der ,,The Open Movie
Database"--Onlinequelle (siehe :cite:`omdb`), es wird nach dem Film ,,The
Matrix'' gesucht:

.. code-block:: bash

   $ curl http://www.omdbapi.com/?t=The+Matrix

   # Ausgabe gekürzt
   {"Title":"The Matrix",
   "Year":"1999",
   "Runtime":"136 min",
   "Genre":"Action, Sci-Fi",
   "Director":"Andy Wachowski, Lana Wachowski",
   "Actors":"Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
   "Plot":"A computer hacker learns from mysterious [...]",
   "Country":"USA, Australia",
   "Poster":"http://ia.media-imdb.com/images/M/SX300.jpg",
   "imdbRating":"8.7",
   "imdbID":"tt0133093",
   [...]
   "Type":"movie",
   "Response":"True"
   }%

Der *Such--URL* bekommt den Titel als Query--Parameter (``t=The+Matrix``)
übergeben, zurück bekommt man ein in *Json* formatiertes Response. Dieses kann
nun vom Aufrufer der API nach belieben verarbeitet werden.

Bietet eine Webseite wie beispielsweise ,,filmstarts.de'' (siehe
:cite:`filmstarts`) keine API an, so muss der ,,normale Weg'' wie über den
Webbrowser erfolgen. Hierzu muss man herausfinden aus welchen Parametern sich
die *Such--URL* zusammensetzt, die im Hintergrund an den Webserver geschickt
wird sobald die Suchanfrage losgeschickt wird. Bei ,,filmstarts.de`` setzt sich
die ,,Such--URL'' wie folgt zusammen:

    ``http://www.filmstarts.de/suche/?q={Filmtitel}``

Rufen wir nun *cURL* mit der URL und unseren Film als Query--Parameter auf so
erhalten wir als Response ein HTML--Dokument, welches auch der Webbrowser
erhalten würde. Folgendes Bash--Snippet demonstriert den Aufruf:

.. code-block:: bash

   $ curl  http://www.filmstarts.de/suche/?q=The+Matrix

   # Ausgabe gekürzt
   <html xmlns="http://www.w3.org/1999/xhtml" xmlns:og="http://ogp.me/ns#"
   xmlns:fb="http://www.facebook.com/2008/fbml"
   xml:lang="de" lang="de">
   <head><title>The Matrix – Suchen auf FILMSTARTS.de</title>
   <meta http-equiv="Content-Language" content="DE" /><meta
   http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta
   http-equiv="imagetoolbar" content="no" />
   [...]
   </html>

Man bekommt als Aufrufer der URL die Webseite zurückgeliefert und muss nun die
Daten aus dem Dokument extrahieren. Dies ist in der Regel mühsamer ist, wie der
Zugriff über eine API, die die Daten sauber im *Json*-- oder *XML*--Format
zurückliefert.



Übertragung vom Grundprinzip auf das Pluginssytem
-------------------------------------------------

Ein Ziel bei der Entwicklung der Plugin--Spezifikation ist, den Aufwand für das
implementieren eines Plugins so gering wie möglich zu halten, um Programmfehler
bzw. Fehlverhalten durch Plugins zu minimieren, aber auch um Entwickler zu
motivieren Plugins zu schreiben.

Das o.g. Prinzip beim Beschaffen von Metadaten ist immer gleich und lässt sich
somit gut auf das Pluginsystem übertragen. Die Provider--Plugins müssen im
Prinzip *nur* folgendes zwei Punkte können:

    * aus den Suchparametern die *Such--URL* zusammenbauen
    * extrahieren der Daten aus dem zurückgelieferten *HTTP--Response*

Um den Download selbst muss sich der Provider bei diesem Ansatz nicht kümmern,
das ,,entlastet" den Pluginentwickler und übergibt *libhugin* die Kontrolle über
das Downloadmanagement.

.. _fig-provider-concept:

.. figure:: fig/provider-concept-svg.pdf
    :alt: Grundprinzip Provider--Plugins
    :width: 80%
    :align: center

    Grundprinzip der Provider--Plugins.


Damit der Provider weiß, welche ,,Roh--Daten'' er zurückliefern soll, muss
hierfür noch eine Struktur mit Attributen festgelegt werden, an welche sich alle
Provider--Plugins halten müssen. Für den Prototypen richten sich die möglichen
Attribute an der TMDb Onlinequelle (siehe hierzu auch libhugin API:
:cite:`movieprovider`).

Libhugin Architektur Überblick
==============================

Die Bibliothek soll über die Metadatenbeschaffung hinaus Werkzeuge zur
Metadatenanalyse bereitstellen. Um eine saubere Trennung zwischen
Metadatenbeschaffung und Metadatenanalyse zu schaffen, wird die Bibliothek in
die zwei Teile *libhugin harvest* und *libhugin analyze* aufgeteilt.

**libhugin harvest:** Dieser Teil (siehe Abbildung :num:`fig-harvest-arch`) soll
für die Metadatenbeschaffung zuständig sein und Schnittstellen für die folgenden
Pluginarten bereitstellen:

    * Provider--Plugins
    * Postprocessing--Plugins # TODO: Postprocessor
    * Output--Converter--Plugins

.. _fig-harvest-arch:

.. figure:: fig/arch-overview-svg.pdf
    :alt: Architekturübersich libhugin
    :width: 80%
    :align: center

    Architekturübersicht libhugin.

**libhugin analyze:** Dieser Teil (siehe Abbildung :num:`fig-harvest-arch`) soll
für nachträgliche Metadatenanalyse zuständig sein und Schnittstellen für
folgende Pluginarten bereitstellen.

    * Modifier--Plugins
    * Analyzer--Plugins
    * Comperator--Plugins

Der Analyze Teil der Bibliothek soll eine interne Datenbank besitzen, in welche
externe Metadaten zur Analyse importiert werden. So können alle Plugins auf
einem ,,definiertem" Zustand arbeiten.

Klassenübersicht libhugin harvest
---------------------------------

Die Architektur von libhugin ist objektorientiert. Aus der Architekturübersicht
und den Anforderungen an das System wurden folgende Klassen und Schnittstellen
abgeleitet, Abbildung :num:`fig-klassenuebersicht-harvest` zeigt eine
Klassenübersicht von libhugin harvest samt Interaktion mit den Schnittstellen.

Im folgenden werden die Grundlegenden Objekte und Schnittstellen
erläutert.

.. _fig-klassenuebersicht-harvest:

.. figure:: fig/klassenuebersicht-harvest-svg.pdf
    :alt: Libhugin harvest Klassenübersicht und Interaktion.
    :width: 80%
    :align: center

    Libhugin harvest Klassenübersicht und Interaktion.


**Session:** Diese Klasse bildet den Grundstein für libhugin harvest. Über eine
Sitzung konfiguriert der Benutzer das System und hat Zugriff auf die
verschiedenen Plugins. Von der Session werden folgende Methoden bereit gestellt:

``create_query(**kwargs)``: Schnittstelle zur Konfiguration der Suchanfrage. Die
Methode gibt ein Query--Objekt zurück, das einem Python Dictionary entspricht.
Diese Methode dient als ,,Hilfestellung" für den Benutzer der API. Theoretisch
kann der Benutzer die Query auch manuell zusammenbauen. Für weitere
Informationen und Konfigurationsparameter siehe libhugin API :cite:`queryapi`.


``submit(query)``: Schnittstelle um eine Suchanfrage zu starten. Die Methode
gibt eine Liste mit gefundenen Metadaten als ,,Result--Objekte" zurück.

Die Methode holt sich eine Downloadqueue und einen Cache, falls dieser vom
Benutzer über die Query nicht deaktiviert wurde. Anschließend generiert sie für
jeden Provider eine sogenannte `Job--Struktur`. Diese `Job--Struktur` kapselt
jeweils einen Provider, die Suchanfrage und die ,,Zwischenergebnisse" die
während der Suchanfrage generiert werden.

Zur Veranschaulichung eine Job--Struktur in Python Dictionary Notation:

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

Nachdem ein Job fertiggestellt wurde, wird er in ein ,,Result--Objekt" gekapselt.
Am Ende der ``submit(query)``--Methode wird eine Liste mit ,,Result--Objekten''
an den Aufrufen zurückgegeben.


``submit_async()``: Methode für eine asynchrone Nutzung der API. Diese führt
``submit(query)`` asynchron aus und gibt ein Python Future Objekt zurück,
welches die Anfrage kapselt. Durch Aufrufen der ``done()``--Methode auf dem
Future--Objekt, kann festgestellt werden ob die Suchanfrage bereits fertig ist.
Ein Aufruf der ``result()``--Methode auf dem Future--Objekt liefert das
eigentliche ,,Result--Objekt" zurück.

Für mehr Informationen siehe Python API :cite:`futures`.

``provider_plugins(pluginname=None)``: Diese Methode gibt eine Liste mit den
Provider--Plugins zurück oder bei Angabe eines Plugins, dieses direkt.

``postprocessing_plugins(pluginname)``: Analog zu ``provider_plugins(pluginname=None)``.

``converter_plugins(pluginname)``: Analog zu ``provider_plugins(pluginname=None)``.

``cancel()``: Diese Methode dient zum Abbrechen einer asynchronen Suchanfrage.
Hier sollte anschließend noch die ``clean_up()``--Methode aufgerufen werden um
alle Ressourcen wieder freizugeben.

``clean_up()``: Methode zum aufräumen nach dem Abbrechen einer asynchronen
Suchanfrage. Die Methode blockt solange noch nicht alle Ressourcen freigegeben
wurden.

**Queue:** Die Queue kapselt die Parameter der Suchanfrage. Sie wird direkt mit
den Parametern der Suchanfrage instantiiert, hierbei werden bestimmte Werte die
übergebenen werden, validiert und *Standardwerte* gesetzt.

**Cache:** Der Cache wird intern verwendet um erfolgreiche Suchanfragen
persistent zwischenzuspeichern. So können die Daten bei wiederholter Anfrage aus
dem Cache geladen werden. Dadurch gewinnt man Geschwindigkeit und der
Metadatenanbieter wird entlastet. Zum persistenten speichern wird ein Python
Shelve (siehe :cite:`shelve`) verwendet.

``open(path, cache_name)``: Öffnet den übergebenen Cache.

``read(key)``: Liest Element an Position *key* aus dem Cache.

``write(key, value)``: Schreibt das Element *value* an Position *key* in den
Cache.

``close()``: Schließt den Cache.


**Downloadqueue:** Die Downloadqueue ist für den eigentlichen Download der Daten
zuständig. Sie arbeitet mit den oben genannten Job-Strukturen. Die
Provider--Plugins müssen so keine eigene Downloadqueue implementieren.

``push(job)``: Fügt einen `Job` der Downloadqueue hinzu.

``pop()``: Holt den nächsten fertigen `Job` aus der Downloadqueue.

``running_jobs()``: Gibt die Anzahl der `Jobs` die in Verarbeitung sind.


**GenreNormalize:** GenreNormalize kann von den Provider--Plugins verwendet
werden um das Genre zu normalisieren. Hierzu müssen die Provider eine
Genre--Mapping--Datei erstellen.  Für mehr Informationen siehe auch API
:cite:`movieprovider`.

``normalize_genre(genre)``: Normalisiert ein Genre anhand einer festgelegten
Lookup--Table.

``normalize_genre_list(genrelist)``: Normalisiert eine Liste aus Genres wie
``normalize_genre()``.

Die Problematik der Genre--Normalisierung ist Bestandteil der Bachelorarbeit.

**PluginHandler:** Das Pluginsystem wurde mit Hilfe der Yapsy--Bibliothek (siehe
:cite:`yapsy`) umgesetzt. Es bietet folgende Schnittstellen nach außen:

``activate_plugin_by_category(category)``: Aktiviert Plugins einer bestimmten
Kategorie. Bei libhugin harvest gibt es die Kategorien  Provider,
Postprocessing und Converter.

``deactivate_plugin_by_category(category)``: Deaktiviert Plugins einer bestimmten
Kategorie.

``get_plugins_from_category(category)``: Liefert Plugins einer bestimmten
Kategorie zurück.

``is_activated(category)``: Gibt ``True`` zurück wenn eine Kategorie bereits aktiviert
ist ansonsten ``False``.

Plugininterface libhugin harvest
--------------------------------

Libhugin harvest bietet für jeden Plugintyp eine bestimmte Schnittstelle an,
die vom jeweiligen Plugintyp implementiert werden muss.

.. _fig-harvest-plulgin-interface:

.. figure:: fig/harvest-plugin-interface.pdf
    :alt: libhugin harvest plugins interface
    :width: 80%
    :align: center

    libhugin harvest plugins interface


Diese libhugin harvest Plugins haben die Möglichkeiten von den folgenden
Oberklassen abzuleiten, Mehrfachableitung ist unter Python möglich:

**Provider Plugins Schnittstellen:**

**IMovieProvider**: Plugins die textuelle Metadaten für Filme beschaffen.

**IMoviePictureProvider**: Plugins die grafische Metadaten für Filme beschaffen.

**IPersonProvider**: Plugins die textuelle Metadaten für Personen beschaffen.

**IPersonPictureProvider**: Plugins die grafische Metadaten für Personen
beschaffen.

**ITVShowProvider**: Plugins die textuelle Metadaten für Serien beschaffen.

**ITVShowPictureProvider**:Plugins die textuelle Metadaten für Serien
beschaffen.


``build_url(search_params)``: Diese Methode bekommt die Such--Parameter
übergeben und baut aus diesen die Such--URL zusammen.
Für weitere Informationen siehe auch API :cite:`buildurl`.

``parse_response(response, search_params)``: Diese Methode bekommt die
HTTP-Response zu der vorher von ``build_url(search_params)`` erstellten
Anfrage--URL. Die Methode ist für das extrahieren der Attribute aus dem Response
zuständig. Sie gibt entweder eine neue URL zurück die angefordert werden soll,
oder befüllt das *result_dictionary* und gibt dieses zurück. Weitere
Für weitere Informationen siehe auch API :cite:`parseresponse`.

``supported_attrs()``
Diese Methode gibt eine Liste mit Attributen zurück die vom Provider befüllt
werden.


**Postprocessing Plugins Schnittstellen:**

**IPostProcesssing**: Plugins die als Postprocessing--Plugins fungieren.

``process()``: Diese Methode bekommt ein Liste mit Result--Objekten übergeben und
manipuliert dieses nach bestimmten Kriterien oder gibt eine neue Liste mit
,,Result--Objekten'' zurück.


**OutputConverter Plugins Schnittstellen:**

**IOutputConverter**: Plugins die als OutputConverter--Plugins fungieren.

``convert()``: Diese Methode bekommt ein ,,Result--Objekt'' übergeben und gibt
die String--Repräsentation von diesem in einem spezifischen Metadatenformat wieder.


Klassenübersicht libhugin analyze
---------------------------------

.. _fig-klassenuebersicht-analyze:

.. figure:: fig/klassenuebersicht-analyze-svg.pdf
    :alt: Libhugin analyze Klassenübersicht und Interaktion.
    :width: 80%
    :align: center

    Libhugin analyze Klassenübersicht und Interaktion.



**Session:** Diese Klasse bildet den Grundstein für libhugin analyze. Sie stellt
analog zur libhugin harvest Session die API bereit.

``add(metadata_file, helper)``: Diese Methode dient zum *importieren* externer
Metadaten. Sie erwartet eine Datei mit Metadaten und als Callback--Funktion eine
*Helferfunktion* (siehe :ref:`helperfunc`) welche weiß wie die Metadaten zu
extrahieren sind.

``analyzer_plugins(pluginname=None)``: Liefert eine Liste mit den vorhandenen
Analyzer--Plugins zurück. Bei Angabe eines bestimmten Pluginnamen, wird dieses
Plugin direkt zurückgeliefert.

``modifier_plugins(pluginname=None)``: Analog zu
``analyzer_plugins(pluginname=None)``.

``comperator_plugins(pluginname=None)``: Analog zu
``analyzer_plugins(pluginname=None)``.

Folgende weitere Methoden erlauben es die libhugin analyze Plugins vom *externe*
Daten anzuwenden:

``analyze_raw(plugin, attr, data)``: Wrapper Methode, welche es erlaubt die
Analyzer--Plugins auf *externen* Daten auszuführen.

``modify_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``compare_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``get_database()``: Liefert die interne Datenbank (Python Dictionary) zurück.


Für das Öffnen und Schließen der interne Datenbank der Session gibt es folgende
zwei Methoden:

``databse_open(databasename)``: Lädt die angegebene Datenbank.
``databse_close()``: Schließt und schreibt die aktuelle Datenbank persistent auf
die Festplatte.


.. _helperfunc:

**Helferfunktion**

Die Helferfunktion hat folgende Schnittstelle:

    ``helper_func(metadata, attr_mask)``

Der ``attr_mask`` Parameter gibt die Abbildungen der Attribute zwischen der
*externen* und *internen* Datenbank an.

Wir nehmen an unsere Metadaten sind im *Json--Format* gespeichert, beim Einlesen
der *Json--Datei* wird diese zu einer :term:`Hashmap` konvertiert die wie folgt
aussieht.

.. code-block:: bash

    metadata_the_movie = {

        'Filmtitel' = 'The Movie',
        'Erscheinungsjahr' = '2025',
        'Inhaltsbeschreibung' = 'Es war einmal vor langer langer Zeit...'
    }

Folgendes Python--Pseudocode--Snippet zeigt nun die Funktionalität der
*Helferfunktion*, welche die Abbildung von externer Quelle auf interne Datenbank
verdeutlicht:

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


**Movie:** Die Movie Klasse repräsentiert ein ,,Metadaten--Objekt" welches in
der internen Datenbank zur Analyze gespeichert wird. Es enthält folgende
Attribute:

    * Schlüssel, über den die Metadaten eindeutig zugeordnet werden können
    * Pfad zur Metadatendatei
    * Hashmap mit den Metadaten
    * Hashmap mit Analyzer--Analysedaten
    * Hashmap mit Comperator--Analysedaten

Plugininterface libhugin analyze
--------------------------------

Libhugin analyze bietet für jeden Plugintyp eine bestimmte Schnittstelle an,
die vom jeweiligen Plugintyp implementiert werden muss.

.. _fig-analyze-plulgin-interface:

.. figure:: fig/analyze-plugin-interface.pdf
    :alt: libhugin analyzeplugins interface
    :width: 80%
    :align: center

    libhugin analyze plugins interface


Die libhugin analyze Plugins haben die Möglichkeiten von den folgenden
Oberklassen abzuleiten, Mehrfachableitung ist unter Python möglich:

**Modifier Plugins Schnittstellen:**

**IModifier**: Plugins die die Metadaten direkt modifizieren.

``modify(self, movie, kwargs)``: Die Standardmethode für Modifierplugins. Die
Methode bekommt ein Movie Objekt und optional Keyword--Argumente übergeben. Die
nötigen Keyword--Argumente können über die ``parameters()``--Methode erfragt
werden.

``modify_all(self, database, kwargs)``: Analog zur ``modify(movie,
kwagrs)``--Methode. Diese Methode arbeitet jedoch nicht mit nur einem Movie
Objekt sondern mit der ganzen ,,Datenbank".

``parameters(self)``: Die Methode listet die Keyword--Argumente für ein
Modifierplugin.

**Analyzer Plugins Schnittstellen:**

**IAnalyzer**: Plugins die für die Analyse der Metadaten zuständig sind. Diese
Plugins schreiben ihre Analysedaten in das ,,Analyzerdata" Attribut des
Movie--Objekts.

``analyze(self, movie, kwargs)``: Die Standardmethode für Analyzerplugins. Die
Anwendung hier ist analog den Modifierplugins.

``analyze_all(self, database, kwargs)``: Analog Modifierplugins.

``parameters(self)``: Analog Modifierplugins.


**Comperator Plugins Schnittstellen:**

**IComparator**: Plugins die Daten beispielsweise vergleichen können für
statistische Zwecke.

``compare(self, movie_a, movie_b, kwargs)``: Die Standardmethode für
Comperatorplugins. Diese erwartet als Parameter zwei Movie Objekte die
vergleichen werden sollen. Die Keyword--Argumente können analog den Modifier--
und Analyzerplugins verwendet werden.

``compare_all(self, database, kwargs)``: Diese Methode vergleicht alle Movie
Objekt Kombinationen aus der Datenbank.

``parameters(self)``: Analog Modifier-- und Analyzerplugins.


Bibliothek Dateistruktur
========================

Die folgende Auflistung zeigt die die Ordnerstruktur Bibliothek.
Normalerweise enthält unter Python jeder Ordner eine `__init__.py--Datei` welche
diesen Ordner dann als ,,Modul" erscheinen lässt. Diese wurden wegen der
Übersichtlichkeit weggelassen.

.. code-block:: python

    hugin
    |-- harvest/                           # libhugin harvest Ordner
    |   |-- session.py                     # Implementierungen der o.g. Klassen
    |   |-- query.py                       #              -- || --
    |   |-- cache.py                       #              -- || --
    |   |-- downloadqueue.py               #              -- || --
    |   |-- pluginhandler.py               #              -- || --
    |   |
    |   |-- converter/                      # Ordner für Converter Plugins
    |   |-- postprocessing/                 # Ordner für Postprocessing Plugins
    |   |-- provider/                       # Ordner für Provider Plugins
    |   |   |-- genrefiles/                 # Genre Dateien für ,,Normalisierung''
    |   |   |   |-- normalized_genre.dat    # Globale Normalisierungstabelle Genre
    |   |   |-- result.py                   # Implementierung ,,ErgebnisObjekt''
    |   |   |-- genrenorm.py                # Implementierung Genrenormalisierung
    |-- utils/                              # Gemeinsame Hilfsfunktionen
    |   |-- logutil.py
    |   |-- stringcompare.py
    |
    |-- analyze/                            # libhugin analyze Ordner
    |   |-- session.py                      # Implementierungen der o.g. Klassen
    |   |-- movie.py                        # Implementierung des ,,Movie'' Objektes
    |   |-- pluginhandler.py
    |   |-- rake.py                         # Implementierung Rake Algorithmus (BA)
    |   |-- analyzer/                       # Ordner für Analyzer Plugins
    |   |-- comparator/                     # Ordner für Modifier Plugins
    |   |-- modifier/                       # Ordner für Comperator Plugins
    |-- filewalk.py                         # Helferfunktion für import/export
