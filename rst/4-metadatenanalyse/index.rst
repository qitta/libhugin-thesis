################
Libhugin Analyse
################

Der *libhugin-harvest* Prototyp der für die Beschaffung der Metadaten verwendet
wird hat die Folgenden Movie--Provider implementiert:

.. figtable::
    :label: fig-provider
    :caption: Überblick implementierter Onlinequellen als Provider.
    :alt: Überblick implementierter Onlinequellen als Provider.

    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    |                  | **tmdb**      | **ofdb**      | **omdb**          | **videobuster** | **filmstarts**  |
    +==================+===============+===============+===================+=================+=================+
    | **Zugriffsart**  | API           | API           | API               | Webzugriff      | Webzugriff      |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    | **Sprache**      | multilingual  | deutsch       | englisch          | deutsch         | deutsch         |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+
    | **Plattformtyp** | Filmdatenbank | Filmdatenbank | Metadatenanbieter | Verleihdienst   | Allg. Plattform |
    +------------------+---------------+---------------+-------------------+-----------------+-----------------+

Desweiteren wurden noch Person--Provider für TMDb und OFDb implementiert.

Timeoutverhalten
================

Während der Entwicklung ist bei der Erhebung der Daten ist aufgefallen, dass der
OFDb--Provider kaum Metadaten findet. Nach kurzer Recherche war zu beobachten,
dass hier der Zugriff über die API sehr oft einen Timeout mit der Fehlermeldung
``,,Fehler oder Timeout bei OFDB Anfrage"`` liefert.

Eine genauere Analyse des Timeout--Verhaltens der Provider zeigt, dass die API
vom OFDb--Provider sehr instabil ist, hierzu wurden Metadaten für 100 Filme je
Provider gezogen. Tabelle :num:`fig-timeout` zeigt wie oft es zu Fehlern pro
Provider gekommen ist. Der Test wurde hier, um gegebenenfalls Server oder
Leitungsprobleme  auszuschließen, an fünf verschiedenen Tagen durchgeführt. Für
den Test wurde das Script aus :ref:`timeout`.


.. figtable::
    :label: fig-timeout
    :caption: Anzahl der ,,retries" beim Herunterladen von metadaten für jeweils 100 filme
    :alt: Anzahl der ,,retries" beim Herunterladen von metadaten für jeweils 100 filme

    +-----------+----------+--------------+----------+-----------------+----------------+
    |           | **tmdb** | **ofdb**     | **omdb** | **videobuster** | **filmstarts** |
    +===========+==========+==============+==========+=================+================+
    | **Tag 1** | (0/0/0)  | (0/31,87/60) | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-----------+----------+--------------+----------+-----------------+----------------+
    | **Tag 2** | (0/0/0)  | (0/0.87/6)   | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-----------+----------+--------------+----------+-----------------+----------------+
    | **Tag 3** | (0/0/0)  | (0/1.23/13)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-----------+----------+--------------+----------+-----------------+----------------+
    | **Tag 4** | (0/0/0)  | (0/1.23/13)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-----------+----------+--------------+----------+-----------------+----------------+
    | **Tag 5** | (0/0/0)  | (0/1.23/13)  | (0/0/0)  | (0/0/0)         | (0/0/0)        |
    +-----------+----------+--------------+----------+-----------------+----------------+

Der OFDb--Provider verteilt die Anfragen über ein Gateway, siehe :cite:`ofdbgw`.
Während der Entwicklung hat sich gezeigt, dass Anfragen über das ofdbgw zu
falschen oder unvollständigen Ergebnisse führten. Ein Testen der einzelnen
Mirror ergab, dass ``http://ofdbgw.geeksphere.de`` als einziger Mirror die
erwarteten Ergebnisse lieferte. Dieser wurde somit im Prototypen direkt als
einziger Mirror aktiviert.

Antwortzeiten Onlinequellen
===========================

Abbildung :num:`fig-sourceresponse` zeigt die Antwortzeiten der jeweiligen
Plattformen/Metadatenanbieter.

Hier wurde mit dem Script im :ref:`source-response` die Zeit beim Zugriff
auf die implementierten Online--Plattformen gemessen. Für die Messung wurden die
in  :ref:`source-response` verwendeten Parameter verwendet. Die Anzahl der
Durchläufe war 10.

.. _fig-sourceresponse:

.. figure:: fig/source_response_time.pdf
    :alt: Antwortzeiten der vom libhugin Prototypen verwendeten Onlineplattformen im Überblick.
    :width: 100%
    :align: center

    Antwortzeiten der vom libhugin Prototypen verwendeten Onlineplattformen im Überblick. Min (grün), Avg (geld), Max (rot).


Der Zugriff in Abbildung :num:`fig-sourceresponse` zeigt hier den
direkten Zugriff über die HTTP--Bibliothek. Bei *libhugin--harvest* besteht die
Suche nach Metadaten in der Regal aus Mehreren Zugriffen. Zusätzlich kommt hier
noch der Aufwand für das Extrahieren der Metadaten aus den jeweiligen
HTTP--Response Objekten hinzu.


.. figtable::
    :label: num-downloads
    :caption: Anzahl der ,,retries" beim Herunterladen von metadaten für jeweils 100 filme
    :alt: Anzahl der ,,retries" beim Herunterladen von metadaten für jeweils 100 filme

    +---------------------+----------+----------+----------+-----------------+----------------+
    |                     | **tmdb** | **ofdb** | **omdb** | **videobuster** | **filmstarts** |
    +=====================+==========+==========+==========+=================+================+
    | **Anzahl Zugriffe** | 2        | 2        | 2        | 2               | 3              |
    +---------------------+----------+----------+----------+-----------------+----------------+

Bei der Suche nach Metadaten für einen Film haben die Provider jeweils einen
Zugriff für die Suchanfrage und einen weiteren Zugriff für den jeweiligen Film.
Der Filmstarts Provider benötigt bei Zugriff auf den jeweiligen Film zwei
Suchanfragen (siehe :num:`num-downloads`), da auf dieser Plattform die
Schauspieler--Informationen zum Film auf einer separaten Teil--Seite zu finden
sind. Folgende Auflistung zeigt die Angesprochenen Seiten des
Filmstarts--Providers:

Suchanfrage nach Metadaten für Film *,,The Matrix"*:

    1. ``http://www.filmstarts.de/suche/?q=the+matrix``

Zugriff auf Seiten mit Metadaten zum Film *,,The Matrix"*:

    1. ``http://www.filmstarts.de/kritiken/35616-Matrix.html``
    2. ``http://www.filmstarts.de/kritiken/35616-Matrix/castcrew.html``


Antwortzeiten libhugin--Provider
================================

Abbildung  :num:`fig-hugindownload` zeigt die Geschwindigkeit den Zugriff auf
Metadaten über die *libhugin--harvest* Bibliothek. Auffällig ist hier die
fast doppelt so lange Zeit bei den Providern ohne API.

.. _fig-hugindownload:

.. figure:: fig/libhugin_download_time.pdf
    :alt: Downloadzeiten pro Provider mit libhugin-harvest.
    :width: 100%
    :align: center

    Downloadzeiten pro Provider mit libhugin-harvest.

Eine zweite Auswertung mit den gleichen Daten und aktiviertem Festplatten--Cache
(Metadaten werden von der Festplatte geladen, es findet kein Webzugriff statt)
zeigt, dass die Provider mit API im Gegensatz zu den Providern ohne API die
Metadaten in sehr kurzer Zeit verarbeiten.

.. _fig-hugindownload-cache:

.. figure:: fig/libhugin_download_time_cache.pdf
    :alt: Downloadzeiten pro Provider mit libhugin-harvest mit aktiviertem Cache.
    :width: 100%
    :align: center

    Downloadzeiten pro Provider mit libhugin-harvest mit aktiviertem Cache.

Die auffällige Antwortzeit mit aktiviertem Festplatten--Cache (Abbildung
:num:`fig-hugindownload-cache`) lässt vermuten, dass das extrahieren der
Metadaten mittels der ``Beautiful-Soup``--Bibliothek aufwendig ist.

Skalierung der Downloadgeschwindigkeit
=======================================

Abbildung :num:`fig-hugin-search` zeigt das Herunterladen von Metadaten mit
einer Unterschiedlichen Anzahl von Parallelen Downloads. Hier wurden jeweils
separat die API und non--API Provider ausgewertet um genauere Aussagen über die
Effektivität beim parallelen Herunterladen machen zu können. Bei den
API--Provider ist eine signifikante zeitliche Verbesserung mit steigender
Download--Thread Anzahl erkennbar. Hier ist die Zeit von ca. 15 Sekunden auf 4
Sekunden gefallen (siehe auch, :num:`fig-hugin-search-api`).
.. _fig-hugin-search:

.. figure:: fig/libhugin_threaded_search.pdf
    :alt: Suche nach dem Film ,,Sin" mit der Beschränkung auf 20 Ergebnisse.
    :width: 90%
    :align: center

    Suche nach dem Film ,,Sin" mit der Beschränkung auf 20 Ergebnisse.

Die non--API Provider bremsen die Performance aufgrund des aufwendigen
extrahieren mittels ``Beautiful--Soup``--Bibliothek stark aus. Hier ist bewegt
sich die Zeit zwischen 45 -- 60 Sekunden für die Beschaffung von 20 Ergebnissen.
Die theoretischen Annahmen aus Kapitel XY werden mit der Einschränkung auf die
Limitierung der non--API Provider bestätigt.

.. _fig-hugin-search-api:

.. figure:: fig/libhugin_threaded_search_api.pdf
    :alt: Suche nach dem Film ,,Sin" mit der Beschränkung auf 20 Ergebnisse.
    :width: 90%
    :align: center

    Suche nach dem Film ,,Sin" mit der Beschränkung auf 20 Ergebnisse.

Die Auswertung wurde mit dem Script in :ref:`hugin_search_benchmark`.

#################
Metadaten Analyse
#################

Die im Prototypen implementieren Metadatenquellen weisen unterschiedliche
Eigenschaften auf. Für die Entwicklung des Prototypen wurden bestimmte Annahmen
getroffen wie beispielsweise, dass sich die Genreverteilung unterscheidet.

Testdatenbeschaffung
====================

Für die Analyse der Metadaten eine Metadaten--Stichprobe von 2500 Filmen mit
Hilfe der  *libhugin-harvest*--Bibliothek beschafft. Die Zusammenstellung
besteht aus möglichst zufällig gewählten Filmen verschiedener Kategorien. Es ist
Grundsätzlich schwierig eine ,,optimale" Metadaten--Stichprobe auszusuchen, da
die Plattformen unterschiedliche Ziele verfolgen. Des weiteren gibt es keine
Standardisierung beim Filmgenre oder anderen Attributen. Aufgrund dessen sollen
im Anschluß bisherige Annahmen und Vermutungen anhand einer Stichprobe überprüft
werden.

Abbildung :num:`fig-testdata` zeigt die Verteilung der Filme anhand vom
Erscheinungsjahr.

.. figtable::
    :label: fig-testdata
    :caption: Testdaten nach Erscheinungsjahr
    :alt: Testdaten nach Erscheinungsjahr

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

Für die Beschaffung der Metadaten wurden die IMDb--IDs von 2500 in einer Datei
gesammelt. Anschließend wurden über ein IMDb--Lookup--Script
(siehe :ref:`imdblookup_script`) alle deutschsprachigen Titel und
Erscheinungsjahre anhand der IMDb--ID bezogen und 2500 Ordner mit der Struktur

        ``[Filmtitel;Erscheinungsjahr;Imdbid]``

mittels diesem Script angelegt. Anschließend  wurden die Metadaten mit Hilfe von
*libhugin--harvest* über die fünf genannten Provider bezogen. Hierbei wurden die
Metadaten bei den  Providern mit IMDb--ID Unterstützung, über diese bezogen.
Provider die keine IMDb--ID Unterstützung bestitzen, wurden über den über IMDb
,,normalisierten" deutschen Titel mit Erscheinungsjahr bezogen.

Die API basierten Provider haben jeweils 2500 Filme gefunden. Bei den
Provider ohne API wurden ca. 2-3 :math:`\%` nicht  gefunden, siehe
:num:`fig-foundmetadata`.

.. figtable::
    :label: fig-foundmetadata
    :caption: Überblick Metadatensuche für 2500 Filme
    :alt: Überblick Metadatensuche für 2500 Filme

    +----------------------------+----------+----------+----------+-----------------+----------------+
    |                            | **tmdb** | **ofdb** | **omdb** | **videobuster** | **filmstarts** |
    +============================+==========+==========+==========+=================+================+
    | **gefundene Filme**        | 2500     | 2500     | 2500     | 2444            | 2427           |
    +----------------------------+----------+----------+----------+-----------------+----------------+
    | **Suche über IMDBID**      |  ja      | ja       | ja       | nein            | nein           |
    +----------------------------+----------+----------+----------+-----------------+----------------+
    | **Onlinezugriff über API** |  ja      | ja       | ja       | nein            | nein           |
    +----------------------------+----------+----------+----------+-----------------+----------------+


Eine Stichprobe von jeweils fünf nicht gefundenen Filmen von Videobuster und
Filmstarts genauer betrachtet:

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

Der Stichprobe nach zu urteilen gibt es hier bei Videobuster und Filmstarts
Probleme. Bei der Suche nach dem Filmtitel ohne Titelzusatz so werden die Titel
gefunden, falls vorhanden. Die Stichprobe zeigt auch, dass die nicht gefundenen
Filme durchaus auf der jeweiligen Plattform gepflegt sein können.

Analyse der Suche über den Lookup--Mode
=======================================

here goes text.

Analyse Genreinformationen
==========================

Das Genre unterscheidet sich oft bei den gepflegten Plattformen. Das
liegt daran, dass das Genre an sich nicht standardisiert ist und die
Onlineplattformen teils divergente Genre--Bezeichnungen haben. Die folgenden
Auswertungen sollen den Umstand anhand der gewählten Stichprobe soviel dadurch
alle bisher für die Entwicklung getroffenen Maßnahmen bestätigen.

Die Daten in Tabelle :num:`fig-genres` wurden mit dem Script in
:ref:`genre-table` erhoben und zeigen die Genreverteilung der fünf Provider für
die Metadaten der 2500 Filme. Bei Filmstarts beziehen sich die
Genreinformationen lediglich nur auf 2427 Filme, bei Videobuster nur auf 2444
Filme.

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
korrigiert. Des Weiteren wurden vereinzelt Genres abgekürzt um die Tabelle
darstellen zu können (f./F. :math:`\hat{=}` Film).

Aus Tabelle :num:`fig-genres` ist nur schwer ersichtlich wie sich die
Genreinformationen im Schnitt pro Film verteilen beziehungsweise wie
detailiert die Filme im Schnitt gepflegt sind. Tabelle :num:`fig-genre-detail`
zeigt wie detailiert die Genreverteilung je Provider ist.

.. figtable::
    :label: fig-genres-detail
    :caption: Überblick Unterschiede in der Genreverteilung bei ca. 2500 Filmen.
    :alt: Überblick Unterschiedie in der Genreverteilung bei ca. 2500 Filmen.
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

Analyse Differenz Erscheinungsjahr
==================================

Bei der Entwicklung wurde augrund der persönlichen Erfahrung des Autors die
Algorithmik beim Zeichenkettenvergleich so angepasst damit das Erscheinungsjahr
,,einzeln" betrachet wird. Hier wurde bisher davon ausgegangen, dass es zwischen
den Plattformen beim Erscheinungsjahr immer wieder zu Differenzen von ein bis
zwei Jahren bei unterschiiechen Plattformen gibt.

Die Erhobenen Metadaten wurden dahingehend mit dem Script in XXX analysiert.
Hier werden für die Betrachtung nur die API--Provider hergenommen, da hier die
Daten mit höherer wahrscheintlichkeit Augrund der Suche über die IMDb--ID
korrekt bezogen wurden.

.. figtable::
    :label: fig-yeardiff
    :caption: Überblick der unterschiedlich gepflegten Erscheinungsjahre.
    :alt: Überblick der unterschiedlich gepflegten Erscheinungsjahre.

        +------------------------+------------+----------+----------+
        |   **Jahresdifferenz:** |   **TMDb** | **OFDb** | **OMDb** |
        +------------------------+------------+----------+----------+
        |   **1 jahr**           |            |          |          |
        +------------------------+------------+----------+----------+
        |   **2 jahr**           |            |          |          |
        +------------------------+------------+----------+----------+
        |   **3 jahr**           |            |          |          |
        +------------------------+------------+----------+----------+

Vollständigkeit der Metadaten
=============================

some text goes here.
