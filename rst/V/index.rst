#######
Entwurf
#######

*Im folgenden wird der systematische Entwurf der Software dargestellt. Die
verwendetetn Algorithmen, Probleme, sowie Möglichgeiten der technischen
Umsetzung werden in der Bachelorarbeit genauer beleuchtet und diskutiert.*

Grundüberlegungen
=================

Grundprinzip -- Beschaffung der Metadaten
-----------------------------------------

*Im folgenden wird das Grundprinzip der Metadatenbeschaffung erläutert und daraus
ableitend die Schnittstellen--Spezifikation für die Plugins definiert.*

Metadaten werden über verschiedene Webplattformen bezogen. Hier wird
grundsätzlich zwischen Anbietern mit API und Anbietern ohne API unterschieden.
Anbieter mit API bieten dem Entwickler direkt eine Schnittstelle über die, die
interne Datenbank des Metadatenanbieters abgefragt werden kann.

Folgendes Bash--Snippet demonstriert einen Zugriff mit dem Webtransfer--Tool
*cULR* (siehe :cite:`curl`) auf die API des ,,The Open Movie
Database''--Webdienstes (siehe :cite:`omdb`), es wird nach dem Film ,,The
Matrix'' gesucht:

.. code-block:: bash

   $ curl http://www.omdbapi.com/?t=The+Matrix
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

Der *Such--URL* bekommt den Titel  als Queryparameter (``t=The+Matrix``)
übergeben, zurück bekommt man ein in *Json* formatiertes Response. Dieses kann
nun vom Aufrufer der API nach belieben verarbeitet werden.

Bietet ein Webseite wie beispielsweise ,,filmstars.de'' (siehe
:cite:`filmstars`) keine API an, so muss der ,,normale Weg'' wie über den
Webbrowser erfolgen. Hierzu muss man herausfinden wie sich die *Such--URL*
aussieht die im Hintergrund an den Webserver geschickt wird sobald man den
,,Suche''--Button auf der Webseite betätigt hat. Bei ,,filmstars.de`` setzt sich
die ,,Such--URL'' wie folgt zusammen:

    ``http://www.filmstarts.de/suche/?q={Filmtitel}``

Rufen wir nun *cURL* mit der Url und unseren Film als Query--Parameter auf so
erhalten wir die HTML--Dokument als ,,HTTP--Response'' das auch der Webbrowser
erhalten würde. Folgendes Bash--Snippet demonstriert den aufruf:

.. code-block:: bash

   $ curl  http://www.filmstarts.de/suche/?q=The+Matrix
   <html xmlns="http://www.w3.org/1999/xhtml" xmlns:og="http://ogp.me/ns#"
   xmlns:fb="http://www.facebook.com/2008/fbml"
   xml:lang="de" lang="de">
   <head><title>The Matrix – Suchen auf FILMSTARTS.de</title>
   <meta http-equiv="Content-Language" content="DE" /><meta
   http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta
   http-equiv="imagetoolbar" content="no" />
   [...]
   </html>

Die Ausgabe wurde gekürzt. Man bekommt als Aufrufer der Url die Webseite
zurückgeliefert und muss nun die Daten aus dem Dokument extrahieren, was in der
Regel mühsamer ist, wie über eine API, die die Daten sauber im *Json*-- oder
*XML*--Format zurückliefert.


Pluginsystem
------------

Ein Ziel bei der Entwicklung der Pluginspezifikation ist, den Aufwand für das
implementieren eines Plugins so gering wie möglich zu halten, um Softwarebugs
bzw. Fehlverhalten durch Plugins zu minimieren, aber auch um Entwickler zu
*motivieren* Plugins zu schreiben.

Übertragung vom Grundprinzip auf das Pluginssytem
-------------------------------------------------

Der das Prinzip beim Beschaffen von Metadaten ist immer gleich lässt sich somit
gut auf Provider--Plugins übertragen. Die Provider--Plugins müssen im Prinzip
*nur* folgendes zwei Punkte können:

    * aus den Suchparametern die *Such--Url* zusammenbauen
    * extrahieren der Daten aus dem zurückgelieferten *HTTP--Response*

Um den Download selbst muss sich der Provider bei diesem Ansatz nicht kümmern,
das ,,entlastet'' den Pluginentwickler und übergibt libhugin die Kontrolle über
das Downloadmanagement.

.. _fig-provider-concept

.. figure:: fig/provider-concept-svg.pdf
    :alt: Grundprinzip Provider--Plugins
    :width: 100%
    :align: center

    Grundprinzip der Provider--Plugins.


Damit der Provider weiß, welche ,,Roh--Daten'' er zurückliefern soll, muss
hierfür noch eine Struktur mit Attributen festgelegt werden, an welche sich alle
Provider--Plugins halten müssen.

.. **Grundprinzip Postprocessing--Plugins und Converter--Plugins**
..
.. Hier wird davon ausgegangen das ein Plugin eine bestimmte Operation auf einem
.. definierten ,,Ergebnisobjekt'' durchführt. Das Prinzip ist trivial, ein
.. ,,Ergebnisobjekt'' wird an das Plugin gegeben und das Plugin führt die gewünschte
.. Operation auf diesem durch oder gibt ein neues definiertes Ergebnis zurück.
..
.. **Normalisierung vom Genre**
..
.. Das Genre ist ein wichtiges Attribut unter den Film--Metadaten. Da hier das
.. Problem der Normalisierung besteht, wird für den libhugin Prototypen eine
.. globale Genreliste definiert. Provider--Plugins haben nun die Möglichkeit eine
.. Normalisierung des Genre durchzuführen indem sie eine Liste mit Abbildungen
.. bereitstellen. Die Abbildungen bilden ein oder mehrere Provider--Genre auf genau
.. einem globalen Genre ab.
..
.. .. code-block:: bash
..
..     lokale Genre (Provider)                                    globales Genre
..     -----------------------                                   ---------------
..     Provider A, Genre SciFi        -- wird abgebildet auf --> Science Fiction
..     Provider A, Genre Horrorfilm   -- wird abgebildet auf --> Horror
..
..     Provider B, Genre Sci-Fi       -- wird abgebildet auf --> Science Fiction
..     Provider B, Genre Splatter     -- wird abgebildet auf --> Horror
..
..     Provider C, Genre Zukunftsfilm -- wird abgebildet auf --> Science Fiction
..     Provider C, Genre Horror       -- wird abgebildet auf --> Horror
..
..
.. Weitere Informationen, Probleme und Ansätze zur Genre Normalisierung werden in
.. der Bachelorarbeit diskutiert.

Libhugin Architektur Überblick
==============================

Die Library soll über die Metadatenbeschaffung hinaus Werkzeuge zur
Metadatenanalyse bereitstellen. Um eine saubere Trennung zwischen
Metadatenbeschaffung und Metadatenanalyse zu schaffen, wird die Library in die
zwei Teile *libhugin harvest* und *libhugin analyze* aufgeteilt.

**libhugin harvest**

Dieser Teil (siehe Abbildung :num:`fig-harvest-arch`) soll für die
Metadatenbeschaffung zuständig sein und Schnittstellen für die folgenden
Pluginarten bereitstellen:

    * Provider--Plugins
    * Postprocessing--Plugins
    * Output--Converter--Plugins

.. _fig-harvest-arch

.. figure:: fig/arch-overview-svg.pdf
    :alt: Architekturübersich libhugin
    :width: 100%
    :align: center

    Architekturübersicht libhugin.

**libhugin analyze**

Dieser Teil (Abbildung :num:`fig-analyze-arch`) soll für nachträgliche
Metadatenanalyse zuständig sein und Schnittstellen für folgende Pluginarten
bereitstellen.

    * Modifier--Plugins
    * Analyzer--Plugins
    * Comperator--Plugins

Der Analyze Teil der library soll eine interne Datenbank besitzen, in welche
externe Metadaten zur Analyse importiert werden. So können alle Plugins auf
einem ,,definiertem'' Zustand arbeiten.


Klassen-- und Schnittstellenübersicht
=====================================

Die Architektur von libhugin ist objektorientiert. Aus der Architektur und den
Anforderungen an das System wurden folgende Klassen und Schnittstellen
abgeleitet, Abbildung X zeigt eine Klassenübersicht samt interaktion mit den
Schnittstellen. Im folgenden werden die Grundlegenden Objekte und Schnittstellen
erläutert.

.. _fig-klassenuebersicht-harvest

.. figure:: fig/klassenuebersicht-harvest-svg.pdf
    :alt: Libhugin harvest Klassenübersicht und Interaktion.
    :width: 100%
    :align: center

    Libhugin harvest Klassenübersicht und Interaktion.

Libhugin harvest
----------------

Session
~~~~~~~

Diese Klasse bildet den Grundstein für libhugin harvest. Über eine Sitzung
konfiguriert der Benutzer das ,,System'' und hat Zugriff auf die verschiedenen
Plugins. Von der Session werden folgende Methoden bereit gestellt:

**create_query(**kwargs)**: Schnittstelle zur Konfiguration der Suchanfrage. Die
Methode gibt ein Query--Objekt zurück, das eine Python Dictionary entspricht.
Diese Methode dient als ,,Hilfestellung'' für den Benutzer der API. Theoretisch
kann der Benutzer die Query auch manuell zusammenbauen.

**submit(query)**: Schnittstelle um eine Suchanfrage ,,loszuschicken''. Die
Methode gibt eine Liste mit gefundenen Metadaten als ,,Result--Objekte'' zurück.
Die Methode holt eine Downloadqueue und einen Cache, falls dieser vom Benutzer
über die Query nicht deaktiviert wurde. Anschließendund generiert für jeden Provider eine
sog. *Job--Struktur*. Diese *Job--Struktur* kapselt jeweils einen Provider, die
Suchanfrage und die ,,Zwisschenergebnisse'' die während des Submit--Aufrufs
generiert werden.

Zur Übersicht eine Job--Struktur in Python Dictionary Notation:

.. code-block:: python

    job_structure = {
        'url': None,          # Url die als nächstes von Downloadqueue geladen werden soll
        'provider': None,     # Referenz auf Provider--Plugin
        'future': None,       # Referenz auf Future Objekt bei async.  Ausführung
        'response': None,     # Ergebnis des Downloads, Http Response
        'return_code': None,  # Return Code der Http Anfrage
        'retries_left': None, # Anzahl der noch übrigen Versuche
        'done': None,         # Flag das gesetzt wird wenn Job fertig ist
        'result': None        # Ergebnis der Suchanfrage
    }

Nachdem ein Job fertiggestellt wurde, wird er in ein Result--Objekt gekapselt.
Am Ende der ``submit``--Methode wird eine Liste mit Result--Objekten an den
Aufrufen zurückgegeben.


**submit_async()**: Methode für eine asynchrone Nutzung der API.

**submit(query)** asynchron aus und gibt ein Python Future Objekt zurück,
welches die Anfrage kapselt. Durch Aufrufen der **done()** Methode auf dem
Future--Objekt, kann festgestellt werden ob die Suchanfrage bereits fertig ist.
Ein Aufruf der **result()**--Methode auf dem Future--Objekt liefert das
eigentliche Result--Objekt zurück. Für mehr Informationen siehe Python API
[lin,].

**provider_plugins(pluginname=None)**: Diese Methode gibt eine Liste mit den
Provider--Plugins zurück oder bei Angabe eines Pluginnamen, dieses direkt.

**postprocessing_plugins(pluginname)**: Analog zu **provider_plugins(pluginname=None)**.

**converter_plugins(pluginname)**: Analog zu **provider_plugins(pluginname=None)**.

**cancel()**: Diese Methode dient zum abbrechen eine asynchronen Suchanfrage.
Hier sollte folgend noch die **clean_up()**--Methode aufgerufen werden um alle
Ressourcen wieder freizugeben.

**clean_up()**: Methode zum *aufräumen* nach dem Abbrechen einer asynchronen
Anfrage. Die Methode blockt solange noch nicht alle Ressourcen freigegeben
wurden.

Queue
~~~~~

Die Queue kapselt die Parameter der Suchanfrage. Sie wird direkt mit den
Parametern der Suchanfrage *instanziiert*, hierbei werden bestimmte Werte die
übergebenen Werte validiert und *Standardwerte* gesetzt.

Cache
~~~~~

Der Cache wird intern verwendet um erfolgreiche Ergebnisse von Suchanfragen
persistent zwischenzuspeichern. So können die Daten bei wiederholter Anfrage aus
dem Cache geladen werden. Dadurch gewinnt man Performance und der
Metadatenanbieter wird entlastet. Zum persistenten speichern wird ein Python
Shelve verwendet.

**open(path, cache_name)**: Öffne den übergebenen Cache.

**read(key)**: Liest Element an Position **key** aus dem Cache.

**write(key, value)**: Schreibt das Element **value** an Position **key** in den Cache.

**close()**: Schließe den Cache.


Downloadqueue
~~~~~~~~~~~~~

Die Downloadqueue ist für den eigentlichen Download der Daten zuständig. Sie
arbeitet mit Job-Strukturen. Die Provider--Plugins müssen so keine
eigene Downloadqueue implementieren. Durch eine zentrale Downloadqueue bleibt
die Kontrolle über den Download der Daten bei libhugin selbst und nicht bei den
Plugins.

**pop()**: Fügt einen *Job* der *Downloadqueue* hinzu.

**push()**: Holt den nächsten fertigen *Job* aus der *Downloadqueue*.

**running_jobs()**: Gibt die Anzahl der *Jobs* die in Verarbeitung sind.

GenreNormalize
~~~~~~~~~~~~~~

GenreNormalize kann von den Provider--Plugins verwendet werden um das Genre zu
normalisieren.

**normalize_genre(genre)**: Normalisiert ein Genre Anhand einer festgelegten
Lookup--Table. Weitere Informationen hierzu in der Bachelorarbeit.

**normalize_genre_list(genrelist)**: Normalisiert eine Liste aus Genres wie
**normalize_genre()**.

PluginHandler
~~~~~~~~~~~~~

Das Pluginsystem wurde mit Hilfe der Yapsy--Library umgesetzt. Es bietet
folgende Schnittstellen nach außen:

**activate_plugin_by_category(category)**: Aktiviert *Plugins* einer bestimmten
Kategorie. Bei libhugin harvest gibt es die Kategorien  *Provider*,
*Postprocessing* und *Converter*.

**deactivate_plugin_by_category(category)**: Deaktiviert *Plugins* einer bestimmten
Kategorie.

**get_plugins_from_category(category)**: Liefert Plugins einer bestimmten Kategorie
zurück.

**is_activated(category)**: Gibt ``True`` zurück wenn eine Kategorie bereits aktiviert
ist ansonsten ``False``.


libhugin harvest Plugininterface
--------------------------------

Libhugin harvest bietet für jeden Plugintyp eine bestimmte Schnittstellen an,
die vom jeweiligen Plugintyp implementiert werden müssen.

.. _fig-harvest-plulgin-interface

.. figure:: fig/harvest-plugin-interface.pdf
    :alt: libhugin harvest plugins interface
    :width: 100%
    :align: center

    libhugin harvest plugins interface

Provider--Plugins
~~~~~~~~~~~~~~~~~

Diese Plugins haben die Möglichkeiten von den folgenden Oberklassen abzuleiten:

**IMovieProvider**: Plugins die textuelle Metadaten für Filme beschaffen.

**IMoviePictureProvider**: Plugins die grafische Metadaten für Filme beschaffen.

**IPersonProvider**: Plugins die textuelle Metadaten für Personen beschaffen.

**IPersonPictureProvider**: Plugins die grafische Metadaten für Personen
beschaffen.

**ITVShowProvider**:Plugins die textuelle Metadaten für Serien beschaffen.

**ITVShowPictureProvider**:Plugins die textuelle Metadaten für Serien
beschaffen.

Jedes konkrete Provider--Plugin muss folgende Methoden implementieren:

``build_url(search_params)``: Diese Methode bekommt die Suchparamenter übergeben
und baut aus diesen die Such--URL zusammen.

``parse_response(response, search_params)``: Diese Methode bekommt die
HTTP-Response zu der vorher von ``build_url(search_params)`` erstellten Anfrage--URL. Die
Methode ist für das *parsen* der Response zuständig. Sie gibt entweder eine neue
URL zurück die angefordert werden soll, oder befüllt das *result_dictionary* und
gibt dieses zurück.

``supported_attrs()``
Diese Methode gibt eine Liste mit Attributen zurück die vom Provider befüllt
werden.

Für weitere Informationen zur Schnittstellenspezifikation des Plugin--Providers
siehe libhugin Dokumentation.

Postprocessing-- und Converter--Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Diese haben die Möglichkeiten von den folgenden Oberklassen abzuleiten:

**IPostProcesssing**: Plugins die als Postprocessing--Plugins fungieren.

``process()``: Diese Methode bekommt ein Liste mit Result--Objekten übergeben und
manipuliert dieses nach bestimmten Kriterien oder gibt eine neue Liste mit
,,Result--Objekten'' zurück.

**IPostProcesssing**: Plugins die als OutputConverter--Plugins fungieren.

``convert()``: Diese Methode bekommt ein ,,Result--Objekt'' übergeben und gibt
die Stringrepräsentation von diesem in einem spezifischen Format wieder.


Libhugin analyze
----------------

.. _fig-klassenuebersicht-analyze

.. figure:: fig/klassenuebersicht-analyze-svg.pdf
    :alt: Libhugin analyze Klassenübersicht und Interaktion.
    :width: 100%
    :align: center

    Libhugin analyze Klassenübersicht und Interaktion.



Session
~~~~~~~

Diese Klasse bildet den Grundstein für libhugin analyze. Sie stellt analog zur
libhugin harvest Session die API bereit.

``add(metadata_file, helper)``: Diese Methode dient zum *importieren* externer
Metadaten. Sie erwartet eine Datei mit Metadaten und als Callback--Funktion eine
*Helferfunktion* welche weiss wie die Metadaten zu extrahieren sind.

``analyze_raw(plugin, attr, data)``: Wrapper Methode, welche es erlaubt die
Analyzerplugins auf *externen* Daten auszuführen.

``analyzer_plugins(pluginname=None)``: Liefert eine Liste mit den vorhandenen
Analyzer--Plugins zurück. Bei Angabe eines bestimmten Pluginnamen, wird dieses
Plugin direkt zurückgeliefert.

``modifier_plugins(pluginname=None)``: Analog zu
``analyzer_plugins(pluginname=None)``.

``comperator_plugins(pluginname=None)``: Analog zu
``analyzer_plugins(pluginname=None)``.

Folgende weitere Methoden erlauben es die Plugins vom Analyzer auf *externen*
Daten auszuführen:

``modify_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``compare_raw(plugin, attr, data)``: Analog zu ``analyze_raw(plugin, attr, data)``.

``get_database()``: Liefert die interne Datenbank (Python Dictionary) zurück.

Für die interne Datenbank der Session:

``databse_open(databasename)``: Lädt die angegebene Datenbank.
``databse_close()``: Schließt und schreibt die aktuelle Datenbank persistent auf
die Festplatte.

**Helferfunktion**

Die Helferfunktion hat folgende Schnittstelle:

    ``helper_func(metadata, attr_mask)``

Der ``attr_mask`` Parameter gibt die Abbildungen der Attribute zwischen der
*externen* und *internen* Datenbank an.

Wir nehmen an unsere Metadaten sind im *Json--Format* gespeichert, bei einlesen
der *Json--Datei* wird diese zu einer Hashmap konvertiert die wie folgt aussieht.

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
        # folgenden zwei Attribute analog hierzu

        'Erscheinungsjahr' = 'year',
        'Inhaltsbeschreibung': 'plot'
    }

   def helper(metadata, attr_mask):
       internal_repr = {}

       for metadata_key, internal_db_key in attr_mask.items():
           internal_repr[internal_db_key] = metadata[metadata_key]

       return internal_repr


Movie
~~~~~

Die Movie Klasse repräsentiert ein Metadatenobjekt welches in der internen
Datenbank zur Analyze gespeichert wird. Es enthält folgende Attribute:

    * ,,key'', über den die Metadaten eindeutig zugeordnet werden können
    * Pfad zur Metadatendatei
    * Hashmap mit den Metadaten
    * Hashmap mit Analyzer--Analysedaten
    * Hashmap mit Comperator--Analysedaten


libhugin analyze Plugininterface
--------------------------------

Libhugin analyze bietet für jeden Plugintyp eine bestimmte Schnittstellen an,
die vom jeweiligen Plugintyp implementiert werden müssen.

.. _fig-analyze-plulgin-interface

.. figure:: fig/analyze-plugin-interface.pdf
    :alt: libhugin analyzeplugins interface
    :width: 100%
    :align: center

    libhugin analyze plugins interface


Library Dateistruktur
=====================

Die folgende Auflistung zeigt die die Ordnerstruktur des Projektes.
Normalerweise enthält unter Python jeder Ordner eine *__init__.py--Datei* welche
diesen Ordner dann als ,,Modul'' erscheinen lässt. Diese wurden wegen der
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
