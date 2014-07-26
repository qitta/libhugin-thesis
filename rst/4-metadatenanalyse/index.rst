#####################
Analyse von Libhugin
#####################

Der *libhugin-harvest* Prototyp, der für die Beschaffung der Metadaten verwendet
wird, hat aktuell die fünf Movie--Provider implementiert, siehe Abbildung
:num:`fig-provider`.

.. figtable::
    :label: fig-provider
    :caption: Überblick implementierter Onlinequellen als Provider.
    :alt: Überblick implementierter Onlinequellen als Provider.

    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    |                  | **TMDb**      | **OFDb**      | **OMDb**          | **Videobuster** | **Filmstarts**  |
    +==================+===============+===============+===================+=================+=================+
    | **Zugriffsart**  | API           | API           | API               | Scraping        | Scraping        |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    | **Sprache**      | multilingual  | deutsch       | englisch          | deutsch         | deutsch         |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    | **Plattformtyp** | Filmdatenbank | Filmdatenbank | Metadatenanbieter | Verleihdienst   | Allg. Plattform |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+

Des Weiteren wurden Personen--Provider für TMDb und OFDb implementiert.

.. _timeoutverhalten:

Timeoutverhalten
================

Bereits während der Entwicklung ist bei der Erhebung der Daten aufgefallen,
dass der OFDb--Provider kaum Metadaten findet. Nach kurzer Recherche war zu
beobachten, dass hier der Zugriff über die API sehr oft einen Timeout mit der
Fehlermeldung ``,,Fehler oder Timeout bei OFDB Anfrage"`` liefert.

Eine genauere Analyse des Timeout--Verhaltens der Provider zeigt, dass die API
vom OFDb--Provider sehr instabil ist. Hierzu wurden Metadaten für 100 Filme je
Provider gezogen. Abbildung :num:`fig-timeout` zeigt wie oft es zu Fehlern pro
Provider gekommen ist. Der Test wurde, um gegebenenfalls Server- oder
Leitungsprobleme  auszuschließen, an fünf verschiedenen Tagen durchgeführt. Für
den Test wurde das Skript aus :ref:`timeout` verwendet.


.. figtable::
    :label: fig-timeout
    :caption: Anzahl der ,,retries" beim Herunterladen von Metadaten für jeweils 100 Filme.
    :alt: Anzahl der ,,retries" beim Herunterladen von Metadaten für jeweils 100 Filme.

    +-------------------------+----------+--------------+----------+-----------------+----------------+
    |                         | **TMDb** | **OFDb**     | **OMDb** | **Videobuster** | **Filmstarts** |
    +=========================+==========+==============+==========+=================+================+
    | **Tag 1 (min/avg/max)** | (0/0/0)  | (0/31,87/60) | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-------------------------+----------+--------------+----------+-----------------+----------------+
    | **Tag 2 (min/avg/max)** | (0/0/0)  | (0/0.87/6)   | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-------------------------+----------+--------------+----------+-----------------+----------------+
    | **Tag 3 (min/avg/max)** | (0/0/0)  | (0/1.23/13)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-------------------------+----------+--------------+----------+-----------------+----------------+
    | **Tag 4 (min/avg/max)** | (0/0/0)  | (0/4.61/55)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-------------------------+----------+--------------+----------+-----------------+----------------+
    | **Tag 5 (min/avg/max)** | (0/0/0)  | (0/3.56/55)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-------------------------+----------+--------------+----------+-----------------+----------------+

Der OFDb--Provider verteilt die Anfragen über einen Lastverteiler, siehe
:cite:`ofdbgw`.  Während der Entwicklung hat eine Stichprobe mit 10 Filmen
gezeigt, dass Anfragen über den Lastverteiler zu unvollständigen Ergebnissen führten.
Hier wurden die Filme ohne Inhaltsbeschreibung zurückgeliefert.

Ein Testen der einzelnen Server ergab, dass ``http://ofdbgw.geeksphere.de`` als
einziger Mirror die erwarteten Ergebnisse lieferte. Dieser wurde somit im
Prototypen direkt als einziger Server aktiviert. Weitere Analysen der Metadaten
sollen Aufschluß darüber geben, ob das Problem weiterhin auftritt.


Antwortzeiten der Onlinequellen
===============================

Abbildung :num:`fig-sourceresponse` zeigt die Antwortzeiten der jeweiligen
Plattformen/Metadatenanbieter, die *libhugin* als Provider implementiert hat.
Hierbei wurde jeweils die ,,Suchseite" des jeweiligen Anbieters angefordert.

Die Zeit wurde mit dem Skript im :ref:`source_response` gemessen.  Für die
Messung wurden die in  :ref:`source_response` verwendeten Parameter angewandt.
Es wurde jeweils der Durchschnitt von 10 einzeln angeforderten Filmen genommen.

.. _fig-sourceresponse:

.. figure:: fig/source_response_time.pdf
    :alt: Antwortzeiten der vom libhugin Prototypen verwendeten Onlineplattformen im Überblick.
    :width: 100%
    :align: center

    Antwortzeiten der vom libhugin Prototypen verwendeten Onlineplattformen im
    Überblick. Minimum (grün), Durchschnitt (gelb), Maximum (rot). Das jeweilige
    Balkenende repräsentiert den exakten Wert.

Der Zugriff in Abbildung :num:`fig-sourceresponse` zeigt hier den
direkten Zugriff über die HTTP--Bibliothek. Bei *libhugin--harvest* besteht die
Standardsuche (über Titel) nach Metadaten in der Regel aus mehreren Zugriffen
(siehe Abbildung :num:`num-downloads`). Zusätzlich kommt hier noch der Aufwand für
das Extrahieren der Metadaten aus den jeweiligen HTTP--Response Objekten hinzu.

Bei der Suche nach Metadaten für einen Film haben die Provider jeweils einen
Zugriff für die Suchanfrage und einen weiteren Zugriff für den jeweiligen Film.

.. figtable::
    :label: num-downloads
    :caption: Anzahl der Zugriffe bei der Standardsuche.
    :alt: Anzahl der Zugriffe bei der Standardsuche.

    +-------------------------+----------+----------+----------+-----------------+----------------+
    |                         | **TMDb** | **OFDb** | **OMDb** | **Videobuster** | **Filmstarts** |
    +=========================+==========+==========+==========+=================+================+
    | **Anzahl der Zugriffe** | 2        | 2        | 2        | 2               | 3              |
    +-------------------------+----------+----------+----------+-----------------+----------------+

Der Filmstarts Provider benötigt bei Zugriff auf den jeweiligen Film zwei
Suchanfragen (siehe :num:`num-downloads`), da auf dieser Plattform die
Schauspieler--Informationen zum Film auf einer separaten Seite zu finden sind.

Folgende Auflistung zeigt die angesprochenen Seiten des Filmstarts--Providers:

Suchanfrage nach Metadaten für Film *,,The Matrix"*:

    1. ``http://www.filmstarts.de/suche/?q=the+matrix``

Zugriff auf Seiten mit Metadaten zum Film *,,The Matrix"*:

    1. ``http://www.filmstarts.de/kritiken/35616-Matrix.html``
    2. ``http://www.filmstarts.de/kritiken/35616-Matrix/castcrew.html``


.. _antwortzeiten:

Antwortzeiten der Libhugin--Provider
====================================

Abbildung  :num:`fig-hugindownload` zeigt die Geschwindigkeit beim Zugriff auf
Metadaten über die *libhugin--harvest*--Bibliothek. Hier wurde
*libhugin--harvest* so konfiguriert, dass pro Provider einzeln jeweils 10 Filme
heruntergeladen werden. Das Ergebnis ist jeweils der Durchschnitt aus 10
Durchläufen. Das Skript in :ref:`libhugin_source_response` wurde für diesen
Benchmark verwendet.

Auffällig ist hier die fast doppelt so lange Zeit bei den Providern ohne API.

.. _fig-hugindownload:

.. figure:: fig/libhugin_download_time.pdf
    :alt: Downloadgeschwindigkeit der Metadaten für einen Film mit libhugin-harvest.
    :width: 100%
    :align: center

    Downloadgeschwindigkeit der Metadaten für einen Film pro Provider mit
    libhugin-harvest. Durchschnitt aus 10 verschiedenen Filmen.

Eine zweite Auswertung mit den gleichen Daten und aktivierten Festplatten--Cache
(Metadaten werden von der Festplatte geladen, es findet kein Webzugriff statt)
zeigt, dass die Provider mit API im Gegensatz zu den Providern ohne API die
Metadaten in sehr kurzer Zeit verarbeiten.

.. _fig-hugindownload-cache:

.. figure:: fig/libhugin_download_time_cache.pdf
    :alt: Abfragegeschwindigkeit der Metadaten für einen Film mit libhugin-harvest und aktiviertem Cache.
    :width: 100%
    :align: center

    Abfragegeschwindigkeit der Metadaten für einen Film pro Provider mit
    libhugin-harvest mit aktiviertem Cache. Durchschnitt aus 10 verschiedenen
    Filmen.

Die auffällige Antwortzeit mit aktivierten Festplatten--Cache (Abbildung
:num:`fig-hugindownload-cache`) deutet darauf hin, dass das Extrahieren der
Metadaten mittels der ``Beautiful-Soup``--Bibliothek sehr aufwendig ist. Das
Aktivieren eines anderen internen Parsers, hat das Ergebnis verschlechtert.
Der `lxml`--Parser, welcher auch in Abbildung :num:`fig-hugindownload-cache`
verwendet wird, ist hier schneller als mögliche Alternativen (siehe :cite:`bs`).


Skalierung der Downloadgeschwindigkeit
======================================

Abbildung :num:`fig-hugin-search` zeigt das Herunterladen von Metadaten mit
einer unterschiedlichen Anzahl von parallelen Downloads. Hier wurden jeweils
separat die API und non--API Provider ausgewertet, um genauere Aussagen über die
Effizienz beim parallelen Herunterladen machen zu können.

Bei den API--Provider ist eine signifikante zeitliche Verbesserung mit
steigender Download--Thread Anzahl erkennbar. Hier ist die Zeit von ca. 9
Sekunden auf 2 Sekunden gefallen (siehe Abbildung, :num:`fig-hugin-search-api`).

Die non--API Provider bremsen die Performance aufgrund des aufwendigen
Extrahierens mittels ``Beautiful--Soup``--Bibliothek stark aus. Hier bewegt
sich die Zeit zwischen 35 - 42  Sekunden für die Beschaffung von 10
Ergebnissen.


.. _fig-hugin-search:

.. figure:: fig/libhugin_threaded_search.pdf
    :alt: Suche nach dem Film ,,Sin" mit einer unterschiedlichen Anzahl von
          Download-Threads (non-API Provider).
    :width: 100%
    :align: center

    Suche nach dem Film ,,Sin" mit einer unterschiedlichen Anzahl von
    Download-Threads. Die Ergebnisanzahl wurde auf 10 beschränkt. Das
    heisst, jeder Provider zieht maximal 10 Filme.

Die theoretischen Annahmen über die Skalierung der Downloadgeschwindigkeit aus
Kapitel :ref:`tech_grundlagen` werden mit der Einschränkung auf die Limitierung
der non--API Provider bestätigt.

Die Auswertung der Skalierung der Downloadgeschwindigkeit wurde mit dem Skript
:ref:`hugin_search_benchmark` durchgeführt.

.. _fig-hugin-search-api:

.. figure:: fig/libhugin_threaded_search_api.pdf
    :alt: Suche nach dem Film ,,Sin" mit einer unterschiedlichen Anzahl von
          Download-Threads (API Provider).
    :width: 100%
    :align: center

    Suche nach dem Film ,,Sin" mit einer unterschiedlichen Anzahl von
    Download-Threads. Die Ergebnisanzahl wurde auf 10 beschränkt. Das
    heisst, jeder Provider zieht maximal 10 Filme.


#####################
Analyse der Metadaten
#####################

Die im Prototypen implementierten Metadatenquellen weisen unterschiedliche
Eigenschaften auf. Allgemein und auch für die Entwicklung des Prototypen wurden
bestimmte Annahmen getroffen:

    * Starke Unterschiede in der Genre--Verteilung zwischen den Quellen.
    * Starke Unterschiede im Genre--Detailgrad zwischen den Quellen.
    * Erscheinungsjahr--Differenzen bei gleichen Filmen zwischen den verschiedenen Quellen.
    * Unvollständigkeit der Metadaten vieler Filme.
    * Bewertungsverteilung der verschiedenen Quellen variiert stark.

Diese Annahmen sollen folgend anhand einer Stichprobe untersucht werden.

Testdatenbeschaffung
====================

Für die Analyse der Metadaten wurde eine Metadaten--Stichprobe von 2500 Filmen
mit Hilfe der *libhugin-harvest*--Bibliothek beschafft. Die Zusammenstellung
besteht aus möglichst zufällig gewählten Filmen verschiedener Kategorien. Es ist
grundsätzlich schwierig, eine ,,optimale" Metadaten--Stichprobe auszusuchen, da
die Plattformen unterschiedliche Ziele verfolgen.

Abbildung :num:`fig-testdata` zeigt die Verteilung der Filme anhand vom
Erscheinungsjahr.

.. figtable::
    :label: fig-testdata
    :caption: Testdaten nach Erscheinungsjahr.
    :alt: Testdaten nach Erscheinungsjahr.

    +----------------------+------------+----------------------+------------+----------------------+------------+
    | **Erscheinungsjahr** | **Anzahl** | **Erscheinungsjahr** | **Anzahl** | **Erscheinungsjahr** | **Anzahl** |
    +======================+============+======================+============+======================+============+
    | 2013                 | 53         | 2001                 | 76         | 1989                 | 15         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2012                 | 224        | 2000                 | 57         | 1988                 | 13         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2011                 | 253        | 1999                 | 50         | 1987                 | 10         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2010                 | 244        | 1998                 | 55         | 1986                 | 13         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2009                 | 245        | 1997                 | 48         | 1985                 | 12         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2008                 | 226        | 1996                 | 27         | 1984                 | 15         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2007                 | 194        | 1995                 | 40         | 1983                 | 7          |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2006                 | 135        | 1994                 | 23         | 1982                 | 10         |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2005                 | 118        | 1993                 | 18         | 1981                 | 4          |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2004                 | 109        | 1992                 | 19         | 1980                 | 9          |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2003                 | 77         | 1991                 | 12         | 1979                 | 4          |
    +----------------------+------------+----------------------+------------+----------------------+------------+
    | 2002                 | 74         | 1990                 | 11         |                      |            |
    +----------------------+------------+----------------------+------------+----------------------+------------+

Für die Beschaffung der Metadaten wurden die IMDb--IDs von 2500 Filmen in einer
Datei gesammelt. Anschließend wurden über ein IMDb--Lookup--Skript (siehe
:ref:`imdblookup_script`) alle deutschsprachigen Titel und Erscheinungsjahre
anhand der IMDb--ID bezogen. Mit diesen Informationen wurden 2500 Ordner mit der
Struktur ``[Filmtitel;Erscheinungsjahr;Imdbid]`` angelegt, hierzu wurde das
gleiche Skript verwendet.

Anschließend  wurden die Metadaten mit Hilfe von *libhugin--harvest* über die
fünf genannten Provider bezogen. Hierbei wurden die Metadaten bei den Providern
mit IMDb--ID Unterstützung über diese bezogen.  Provider, die keine IMDb--ID
Unterstützung besitzen, wurden über den, über IMDb ,,normalisierten" deutschen
Titel, mit Erscheinungsjahr bezogen. Die Metadaten wurden ebenso mit dem Skript
:ref:`imdblookup_script` bezogen. Ein komprimiertes Archiv mit den Testdaten
findet sich unter :cite:`metadata`.

Die API basierten Provider haben jeweils 2500 Filme gefunden. Bei den
Provider ohne API wurden ca. 2-3 :math:`\%` nicht  gefunden, siehe dazu
Abbildung :num:`fig-foundmetadata`.

.. figtable::
    :label: fig-foundmetadata
    :caption: Überblick Metadatensuche für 2500 Filme.
    :alt: Überblick Metadatensuche für 2500 Filme.

    +----------------------------+---------------------+--------------------+--------------------+-----------------+----------------+
    |                            | **tmdb**            | **ofdb**           | **omdb**           | **videobuster** | **filmstarts** |
    +============================+=====================+====================+====================+=================+================+
    | **gefundene Filme**        | 2500                | 2500               | 2500               | 2444            | 2427           |
    +----------------------------+---------------------+--------------------+--------------------+-----------------+----------------+
    | **Suche über IMDBID**      |  :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\times`  | :math:`\times` |
    +----------------------------+---------------------+--------------------+--------------------+-----------------+----------------+
    | **Onlinezugriff über API** |  :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\times`  | :math:`\times` |
    +----------------------------+---------------------+--------------------+--------------------+-----------------+----------------+


Eine Stichprobe von jeweils fünf nicht gefundenen Filmen von Videobuster und
Filmstarts wurde genauer betrachtet:

**Filmstarts**:

    * ,,Secretary (2002)", wird ohne Titelzusatz gefunden.
    * ,,Reservoir Dogs (1992)", wird ohne Titelzusatz gefunden.
    * ,,Peter & der Wolf (2006)", auf Plattform nicht vorhanden.
    * ,,One Dark Night (1982)", auf Plattform nicht vorhanden.
    * ,,O Brother, Where Art Thou? (2000)", wird ohne Titelzusatz gefunden.

**Videobuster**:

    * ,,Mimic (1997)", wird ohne Titelzusatz gefunden.
    * ,,Miez und Mops (1986)", auf Plattform nicht vorhanden.
    * ,,Like Someone in Love (2012)", auf Plattform nicht vorhanden.
    * ,,The Last House on the Left (2009)", wird wegen Altersverifikation nicht gefunden.
    * ,,Infernal Affairs (2002)", wird ohne Titelzusatz gefunden.

**Anmerkung zum Titelzusatz:** Die über IMDb ,,normalisierten" Titel haben oft
einen Titelzusatz. Beispielsweise der Film ,,Secretary (2002)" wurde über IMDb
auf ,,Secretary -- Womit kann ich dienen? (2002)" normalisiert.

Der Stichprobe nach zu urteilen, gibt es hier bei Videobuster und Filmstarts
Probleme. Bei der Suche nach dem Filmtitel ohne Titelzusatz werden die Titel
gefunden, falls vorhanden.

Die Stichprobe der 10 Filme zeigt, dass die nicht gefundenen Filme durchaus auf
der jeweiligen Plattform gepflegt sein können.

.. raw:: Latex

   \newpage


.. _genreinformationen:

Analyse der Genreinformationen
==============================

Das Genre unterscheidet sich oft bei den gepflegten Plattformen. Das
liegt daran, dass das Genre an sich nicht standardisiert ist und die
Onlineplattformen teils divergente Genre--Bezeichnungen haben.  Die folgenden
Auswertungen sollen den Umstand anhand der gewählten Stichprobe, sowie alle
bisher für die Entwicklung getroffenen Annahmen, bestätigen.

Die Daten in Abbildung :num:`fig-genres` wurden mit dem Skript im :ref:`genre-table`
erhoben und zeigen die Genreverteilung der fünf Provider für die Metadaten der
2500 Filme. Bei Filmstarts beziehen sich die Genreinformationen lediglich nur
auf 2427 Filme, bei Videobuster nur auf 2444 Filme.

.. figtable::
    :label: fig-genres
    :caption: Überblick Unterschiede in der Genreverteilung bei ca. 2500 Filmen.
    :alt: Überblick Unterschiedie in der Genreverteilung bei ca. 2500 Filmen.
    :spec: l|l|l|l|l

    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | **OFDb/2500**        | **OMDb/2500**   | **TMDb/2500**        | **Videobuster/2444** | **Filmstarts/2427** |
    +======================+=================+======================+======================+=====================+
    | Abenteuer: 180       | Action: 650     | Abenteuer: 362       | 18+ Spielf.: 332     | Abenteuer: 202      |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Action: 609          | Adult: 2        | Action: 753          | Abenteuer: 113       | Action: 529         |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Biographie: 60       | Adventure: 331  | Animation: 124       | Action: 395          | Animation: 112      |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Dokumentation: 33    | Animation: 125  | Dokumentarf.: 36     | Animation: 98        | Biografie: 50       |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Drama: 1086          | Biography: 104  | Drama: 1200          | Anime: 24            | Dokumentation: 43   |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Eastern: 4           | Comedy: 722     | Eastern: 2           | Bollywood: 2         | Drama: 801          |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Erotik: 26           | Crime: 575      | Erotik: 6            | Deutscher F.: 127    | Erotik: 22          |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Essayfilm: 1         | Documentary: 33 | Familie: 130         | Dokumentation: 38    | Experimentalf.: 1   |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Experimentalf.: 1    | Drama: 1239     | Fantasy: 182         | Drama: 616           | Familie: 50         |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Fantasy: 193         | Family: 76      | Film Noir: 2         | Fantasy: 180         | Fantasy: 229        |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Grusel: 5            | Fantasy: 169    | Foreign: 152         | Horror: 304          | Gericht: 8          |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Heimatfilm: 1        | History: 48     | Historie: 52         | Kids: 47             | Historie: 46        |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Historienf.: 19      | Horror: 349     | Holiday: 1           | Komödie: 491         | Horror: 313         |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Horror: 352          | Music: 31       | Horror: 387          | Kriegsfilm: 47       | Komödie: 578        |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Kampfsport: 16       | Musical: 12     | Indie: 149           | Krimi: 275           | Kriegsfilm: 37      |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Katastrophen: 8      | Mystery: 264    | Katastrophenf.: 4    | Lovestory: 142       | Krimi: 209          |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Familienfilm: 110    | Romance: 317    | Komödie: 718         | Musik: 31            | Martial Arts: 16    |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Komödie: 727         | Sci-Fi: 258     | Kriegsfilm: 57       | Ratgeber: 1          | Monumentalf.: 3     |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Krieg: 56            | Short: 10       | Krimi: 452           | Science-Fiction: 223 | Musical: 7          |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Krimi: 193           | Sport: 38       | Lovestory: 341       | Serie: 17            | Musik: 28           |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Liebe/Romantik: 257  | Thriller: 650   | Musical: 23          | Softerotik: 1        | Romanze: 216        |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Musikfilm: 30        | War: 37         | Musik: 23            | TV-Film: 10          | Sci-Fi: 235         |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Mystery: 79          | Western: 6      | Mystery: 239         | Thriller: 599        | Spionage: 29        |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Science-Fiction: 271 |                 | Neo-noir: 3          | Western: 15          | Sport: 1            |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Sex: 5               |                 | Road Movie: 3        |                      | Thriller: 671       |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Splatter: 34         |                 | Science Fiction: 337 |                      | Tragikomödie: 127   |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Sportfilm: 31        |                 | Short: 6             |                      | Unbekannt: 25       |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Thriller: 803        |                 | Sport: 15            |                      | Western: 11         |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Tierfilm: 8          |                 | Sport Film: 12       |                      | Kein Genre: 1       |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    | Western: 10          |                 | Suspense: 53         |                      |                     |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    |                      |                 | Thriller: 1000       |                      |                     |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    |                      |                 | Western: 10          |                      |                     |
    +----------------------+-----------------+----------------------+----------------------+---------------------+
    |                      |                 | Kein Genre: 25       |                      |                     |
    +----------------------+-----------------+----------------------+----------------------+---------------------+

Beim TMDb und Videobuster Provider war das Genre Komödie auf jeweils drei Genre
aufgrund eines fehlerhaften Encoding verteilt. Dieser Umstand wurde per Hand
korrigiert. Des Weiteren wurden vereinzelt Genres abgekürzt, um die Tabelle
darstellen zu können (f./F. :math:`\hat{=}` Film).

Aus Abbildung :num:`fig-genres` ist nur schwer ersichtlich wie sich die
Genreinformationen im Schnitt pro Film verteilen, beziehungsweise wie
detailliert die Filme im Schnitt gepflegt sind. Abbildung
:num:`fig-genre-avg` zeigt wie detailliert die Genreverteilung im Schnitt
pro Film ist.

.. figtable::
    :label: fig-genre-avg
    :caption: Anzahl der vergebenen Genres pro Film.
    :alt: Anzahl der vergebenen Genres pro Film.
    :spec: c|l|l|l|l|l

    +----------------------+----------+----------+----------+-----------------+----------------+
    |  **Genres pro Film** | **OFDb** | **OMDb** | **TMDb** | **Videobuster** | **Filmstarts** |
    +======================+==========+==========+==========+=================+================+
    | **0**                | 0        | 0        | 25       | 0               | 1              |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **1**                | 701      | 372      | 398      | 976             | 913            |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **2**                | 1029     | 713      | 666      | 1259            | 926            |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **3**                | 639      | 1412     | 783      | 202             | 522            |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **4**                | 123      | 3        | 435      | 7               | 57             |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **5**                | 8        | 0        | 153      | 0               | 8              |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **6**                | 0        | 0        | 30       | 0               | 0              |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **7**                | 0        | 0        | 10       | 0               | 0              |
    +----------------------+----------+----------+----------+-----------------+----------------+
    | **Durchschnittlich** | **2,08** | **2,42** | **2,73** | **1,69**        | **1,89**       |
    +----------------------+----------+----------+----------+-----------------+----------------+

Die Auswertung bestätigt die bisherigen Annahmen. Die Genreinformationen sind
hier sehr divergent (siehe Abbildung :num:`fig-genres`) gepflegt und
unterscheiden sich auch im Detailgrad  (siehe Abbildung :num:`fig-genre-avg`).

.. _yeardiff:

Analyse der Erscheinungsjahrdifferenz
=====================================

Bei der Entwicklung wurde aufgrund der persönlichen Erfahrung des Autors die
Algorithmik beim Zeichenkettenvergleich so angepasst, damit das Erscheinungsjahr
,,einzeln" betrachtet wird. Hier wurde bisher davon ausgegangen, dass es zwischen
den Plattformen beim Erscheinungsjahr immer wieder zu Differenzen von ein bis
zwei Jahren kommen kann.

Die erhobenen Metadaten wurden dahingehend mit dem Skript im :ref:`code_yeardiff`
analysiert.  Hier werden für die Betrachtung die API--Provider und die
non--API--Provider hergenommen. Bei den API--Providern wird die Gleichheit des
Films anhand der IMDb--ID definiert. Bei den non--API--Provider--Daten, die keine
IMDb--ID besitzen, wird eine Titelübereinstimmung von 90% gefordert.
Filme, die diese Eigenschaft erfüllen, fließen in die
Erscheinungsjahrdifferenz--Auswertung ein (siehe Abbildung :num:`fig-yeardiff`).
Als Bezugsreferenz wurde hier der TMDb Provider genommen.

.. figtable::
    :label: fig-yeardiff
    :caption: Überblick der unterschiedlich gepflegten Erscheinungsjahre gleicher Filme.
    :alt: Überblick der unterschiedlich gepflegten Erscheinungsjahre gleicher Filme.

        +--------------------------------+------------+----------+----------------+-----------------+
        |   **Jahresdifferenz zu TMDb:** |   **OFDb** | **OMDb** | **Filmstarts** | **Videobuster** |
        +================================+============+==========+================+=================+
        |   **0 Jahre**                  | 2378       | 2403     | 1844           | 1792            |
        +--------------------------------+------------+----------+----------------+-----------------+
        |   **1 Jahre**                  | 109        | 87       | 198            | 118             |
        +--------------------------------+------------+----------+----------------+-----------------+
        |   **2 Jahre**                  | 8          | 5        | 13             | 8               |
        +--------------------------------+------------+----------+----------------+-----------------+
        |   **3 Jahre**                  | 2          | 2        | 3              | 3               |
        +--------------------------------+------------+----------+----------------+-----------------+
        |   **> 3 Jahre**                | 0          | 0        | 42             | 36              |
        +--------------------------------+------------+----------+----------------+-----------------+

Die Videobuster und Filmstarts Ergebnisse wurden zusätzlich manuell auf die
Übereinstimmung des Regisseurs überprüft. Hier wurde eine Übereinstimmung des
Namens von 95% gefordert. Dieser stimmt in insgesamt 317 von 343 (1 - 3 Jahre)
Fällen überein. In den restlichen 26 Fällen, war in 13 Fällen ein Vergleich
nicht möglich, in weiteren 13 war der Film unterschiedlich.

Die restlichen, insgesamt 78 Filme, die bei der Jahresdifferenz
:math:`\textgreater` 3 gelistet sind, wurden manuell auf Regisseur
Übereinstimmung untersucht. Hier gab es nur eine einzige Übereinstimmung, die
restlichen 77 Filme waren ,,Remakes", Filme mit zufälligerweise gleichem Titel
oder Filme ohne gelisteten Regisseur.


.. _unvoll:

Unvollständigkeit der Metadaten
===============================

Abbildung :num:`fig-completeness` zeigt die Anzahl der nicht gepflegten Attribute
je Provider. Die Menge bezieht sich hier auf die, pro Provider, jeweils gefundene
Anzahl der Metadaten (siehe Abbildung :num:`fig-foundmetadata`). Die mit
:math:`\times` markierten Felder deuten darauf hin, dass das Attribut vom
Provider nicht ausgefüllt wird.

Auffällig in Abbildung :num:`fig-completeness` ist, dass der OFDb--Provider das
Attribut ,,plot" 2353 mal nicht gefunden hat. Die manuelle Überprüfung dieses
Wertes bestätigt, dass es hier bei dem verwendeten API--Mirror, wie bereits
erwähnt in Kapitel :ref:`timeoutverhalten` Timeoutverhalten, entgegen der
vorherigen Annahme, weiterhin zu Problemen kommt. Die Daten wurden mit dem
Skript :ref:`completness` analysiert.


.. figtable::
    :label: fig-completeness
    :caption: Überblick fehlende Metadaten
    :alt: Überblick fehlende Metadaten

    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **Attribute**          | **OFDb**       | **OMDb**       | **TMDb**       | **Videobuster** | **Filmstarts**  |
    +========================+================+================+================+=================+=================+
    | **title**              | 0              | 0              | 0              | 0               | 0               |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **original_title**     | 0              | 0              | 0              | 0               |  :math:`\times` |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **plot**               | 2353           | 57             | 81             | 5               | 151             |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **runtime**            | :math:`\times` | 30             | :math:`\times` | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **imdbid**             | 0              | 0              | 0              | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **vote_count**         | 5              | 0              | 101            | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **rating**             | 0              | 0              | 482            | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **alternative_titles** | :math:`\times` | :math:`\times` | 315            | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **directors**          | 0              | 4              | 19             | 8               | 109             |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **writers**            | 2404           | 12             | 1818           | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **year**               | 0              | 1              | 2              | 0               | 5               |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **poster**             | 0              | 82             | 707            | 0               | 1               |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **fanart**             | :math:`\times` | :math:`\times` | 2465           | :math:`\times`  | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **countries**          | 0              | :math:`\times` | 104            | 0               | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **genre**              | 0              | 0              | 25             | 0               | 1               |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **studios**            | :math:`\times` | :math:`\times` | 434            | 0               | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **actors**             | 132            | 6              | 23             | 137             | 442             |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **keywords**           | :math:`\times` | :math:`\times` | 444            | 129             | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+
    | **tagline**            | :math:`\times` | :math:`\times` | 1833           | 1138            | :math:`\times`  |
    +------------------------+----------------+----------------+----------------+-----------------+-----------------+

Die Abbildung :num:`fig-completeness` zeigt, dass je nach Onlinequelle die
Vollständigkeit der Metadaten nicht gewährleistet werden kann. Es zeigt ebenso,
dass Plattformen, wie Videobuster das Attribut ,,Poster/Cover" vollständig
gepflegt haben. Bei diesem Anbieter handelt es sich um eine
Videoverleihplattform, welche anscheinend darauf Wert legt, dass jeder
ausleihbare Film auch ein digitales Cover besitzt.

.. raw:: Latex

   \newpage


.. _ratingkapitel:

Ratingverteilung der Stichprobe
===============================

Folgend finden sich eine Rating--Auswertung zu den drei API--basierten Providern.
Die non--API--basierten Provider befüllen in der aktuellen Version das Attribut
Rating nicht.

Die Analyse soll darüber Auskunft geben, ob es bei den Plattformen in der Bewertung
signifikante Unterschiede gibt. Bei allen drei Anbietern bewegt sich das Rating
auf einer Skala von 0 -- 10.

Abbildung :num:`rating` zeigt, dass das Rating der Stichprobe bei allen drei
Providern sich im Schnitt bei ca 6,5 von 10 bewegt.

.. figtable::
    :label: rating
    :caption: Ratingverteilung der Stichprobe.
    :alt: Ratingverteilung der Stichprobe.

    +----------------------------------------------+----------+----------+----------+
    |                                              | **OMDb** | **TMDb** | **OFDb** |
    +==============================================+==========+==========+==========+
    | **Minimales Rating in der Stichprobe**       | 1.9      | 0.2      | 0        |
    +----------------------------------------------+----------+----------+----------+
    | **Durchschnittliches Rating der Stichprobe** | 6.57     | 6.36     | 6.46     |
    +----------------------------------------------+----------+----------+----------+
    | **Maximales Rating der Stichprobe**          | 10.0     | 10.0     | 9.0      |
    +----------------------------------------------+----------+----------+----------+


.. raw:: Latex

   \newpage

Die Abbildung :num:`fig-rating` zeigt weiterhin die Verteilung des
Movie--Ratings der drei API--Provider.  Hier zeigt sich, dass das Rating in der
Stichprobe bei allen drei Anbietern sehr ähnlich ausfällt.

.. _fig-rating:

.. figure:: fig/rating.pdf
    :alt: Verteilung vom Movie-Rating der Stichprobe von 2500 Filmen der drei
          Anbieter TMDb, OMDb und OFDb.
    :width: 90%
    :align: center

    Verteilung vom Movie-Rating der Stichprobe von 2500 Filmen der drei Anbieter
    TMDb, OMDb und OFDb.


Die vorliegenden Daten wurden mit dem Skript in :ref:`rating` analysiert.

######
Trivia
######

Testumgebung
============

Die Bibliothek wurde in der Python--Version 3.4 getestet. Die Skripte im Anhang
wurden für die jeweiligen Auswertungen verwendet. Für das Einlesen der Metadaten
verwenden manche Skripte die Funktion analyze_folder. Diese Funktion wurde in
die ``utils.py``--Datei ausgelagert (siehe :ref:`utils`).

Bei zeitabhängigen Messungen wurde darauf geachtet, dass immer der
Durchschnitt aus mehreren Durchläufen genommen wurde, um statistische Ausreißer
zu unterdrücken.

Als Testumgebung wurde das folgende System verwendet:

    * OS: Arch Linux, 3.14.6-1-ARCH x86_64 (64 bit)
    * CPU: Intel Core 2 Quad Q6600  @ 2.40GHz
    * RAM: 4 GB DDR2 RAM
    * HDD: Hitachi 120GB, 5400 upm

Als Internetanbindung wurde eine VDSL 50 Mbit Leitung der Telekom verwendet.
Diese hat laut Internet--Messverfahren eine tatsächliche Geschwindigkeit von
47,9 Mbit/s (downstream) und 7,7 Mbit/s (upstream).

Statistiken und Plots
=====================

Für das Analysieren der Metadaten wurden eigene Skripte geschrieben. Diese sind
an jeweiliger Stelle genannt und befinden sich im Anhang. Für das Erstellen der
Grafiken/Plots wurde die Python Matplotlib--Bibliothek verwendet (siehe
:cite:`matplotlib`).
