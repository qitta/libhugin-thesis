#######
Entwurf
#######

*Im folgenden wird der systematische Entwurf der Software dargestellt. Die
verwendetetn Algorithmen, Probleme sowie Möglichgeiten der technischen Umsetzung
werden in der Bachelorarbeit genauer beleuchtet und diskutiert.*

Grundüberlegung
===============

Die Library soll über die Metadatenbeschaffung hinaus Werkzeuge zur
Metadatenanalyse bereitstellen. Um eine saubere Trennung zwischen
Metadatenbeschaffung und Metadatenanalyse zu schaffen, wird die Library in die
zwei Teile *libhugin harvest* und *libhugin analyze* aufgeteilt.

Libhugin Architektur
====================

**libhugin harvest**

Dieser Teil (siehe Abbildung :num:`fig-harvest-arch`) soll für die
Metadatenbeschaffung zuständig sein und Schnittstellen für die folgenden
Pluginarten bereitstellen:

    * Provider--Plugins
    * Postprocessing--Plugins
    * Output--Converter--Plugins

Libhugin harvest besitzt ein zentrales Downloadmodul. Somit bleibt die Kontrolle
über den Download bei der library und die Provider-Plugin--Entwickler müssen
keine Downloadfunktionalität implementieren.


.. _fig-harvest-arch

.. figure:: fig/arch-overview.png
    :alt: Architekturübersich libhugin
    :width: 80%
    :align: center

    Architekturübersicht libhugin.

**libhugin analyze**

Dieser Teil (Abbildung :num:`fig-analyze-arch`) soll für nachträgliche
Metadatenanalyse zuständig sein und Schnittstellen für folgende Pluginarten
bereitstellen.

    * Modifier--Plugins
    * Analyzer--Plugins
    * Comperator--Plugins

Der Analyze Teil der library hat eine interne *Datenbank* die die
,,normalisierten'' Metadaten enthält. Diese Datenbank wird durch den Import
externer Metadaten aufgebaut. Auf diesen ,,arbeiten'' dann die
Modifier--, Analyzer-- und Comperator--Plugins.

Klassenübersicht und Schnittstellen
===================================

Aus der Architektur wurde ein Entwurf abgeleitet, Abbildung X zeigt eine
Klassenübersicht und ihre Schnittstellen.

**Session**

Das ist der Einstiegspunkt für libhugin harvest. Über eine Sitzung konfiguriert
der Benutzer das ,,System'' und hat Zugriff auf die verschiedenen Plugins.

    * ``create_query()``
    * ``submit()``
    * ``submit_async()``

    * ``provider_plugins()``
    * ``postprocessing_plugins()``
    * ``converter_plugins()``

    * ``cancel()``
    * ``clean_up()``


**Queue**

Die Queue kapselt die Parameter der Suchanfrage. Die Queue wird mit den
Parametern der Suchanfrage *instanziiert*, hierbei werden bestimmte Werte
validiert und *Defaultwerte* gesetzt.

**Cache**

Wird intern verwendet um erfolgreiche Ergebnisse von Suchanfragen persistent
zwischenzuspeichern. So können die Daten bei wiederholter Anfrage aus dem Cache
geladen werden. Dies funktioniert schneller und entlastet den Metadatenanbieter.

``open()``: Öffne den übergebenen Cache.
``read()``: Lese Element an Position *key* aus dem Cache.
``write()``: Schreibe Element Value an Position *key* in den Cache.
``close()``: Schließe den Cache.

**Downloadqueue**

Die Downloadqueue ist für den eigentlichen Download der Daten zuständig. Die
Provider--Plugins müssen so keine eigene Downloadqueue implementieren. Durch
eine zentrale Downloadqueue bleibt die Kontrolle über den Download der Daten bei
libhugin selbst und nicht bei den Plugins.

``pop()``: Fügt einen *Job* der *Downloadqueue* hinzu.
``push()``: Holt den nächsten fertigen *Job* aus der *Downloadqueue*.
``running_jobs()``: Gibt die Anzahl der *Jobs* die in Verarbeitung sind.


**GenreNormalize**

GenreNormalize kann von den Provider--Plugins verwendet werden um das Genre zu
normalisieren.

``normalize_genre()``: Normalisiert ein Genre Anhand einer festgelegten
Lookup--Table. Weitere Informationen hierzu in der Bachelorarbeit.

``normalize_genre_list()``: Normalisiert eine Liste aus Genres wie
``normalize_genre()``.


**PluginHandler**

Das Pluginsystem wurde mit Hilfe der Yapsy--Library umgesetzt. Es bietet
folgende Schnittstellen nach außen:

``activate_plugin_by_category(category)``: Aktiviert *Plugins* einer bestimmten
Kategorie. Bei libhugin harvest gibt es die Kategorien  *Provider*,
*Postprocessing* und *Converter*.

``deactivate_plugin_by_category(category)``: Deaktiviert *Plugins* einer bestimmten
Kategorie.

``get_plugins_from_category(category)``: Liefert Plugins einer bestimmten Kategorie
zurück.

``is_activated(category)``: Gibt ``True`` zurück wenn eine Kategorie bereits aktiviert
ist ansonsten ``False``.

Plugininterface
---------------

Das Modul hugin bietet für jeden Plugintyp bestimmte Schnittstellen, die
vom Plugin implementiert werden müssen.

**Provider--Plugins**

Diese Plugins haben die Möglichkeiten von den folgenden Oberklassen abzuleiten:

``IMovieProvider``: Plugins die textuelle Metadaten für Filme beschaffen.
``IMoviePictureProvider``: Plugins die grafische Metadaten für Filme beschaffen.

``IPersonProvider``: Plugins die textuelle Metadaten für Personen beschaffen.
``IPersonPictureProvider``:Plugins die textuelle Metadaten für Personen
beschaffen.

``ITVShowProvider``:Plugins die textuelle Metadaten für Serien beschaffen.
``ITVShowPictureProvider``:Plugins die textuelle Metadaten für Serien
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

**Postprocessing--Plugins**

Die Postprocessing--Plugins haben die Möglichkeiten von den folgenden
Oberklassen abzuleiten:

``IPostProcesssing``.

``process()``: Diese Methode bekommt ein ,,Result--Objekt'' übergeben und
manipuliert dieses nach bestimmten Kriterien oder gibt ein neues
,,Result--Objekt'' zurück.

**OutputConverter--Plulgins**

``convert``: Diese Methode bekommt ein ,,Result--Objekt'' übergeben und gibt
die Stringrepräsentation von diesem in einem spezifischen Format wieder.


Library Dateistruktur
=====================

...

