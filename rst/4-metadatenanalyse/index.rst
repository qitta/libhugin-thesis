################
Metadatenquellen
################

Die im Prototypen implementieren Metadatenquellen weisen unterschiedliche
Eigenschaften auf. Für die Entwicklung des Prototypen wurden bestimmte Annahmen
getroffen wie beispielsweise, dass sich die Genreverteilung unterscheidet.

Für die Analyse der Metadaten eine Metadaten--Stichprobe von 2500 Filmen mit
Hilfe der  *libhugin-harvest*--Bibliothek beschafft. Die Zusammenstellung
besteht aus möglichst zufällig gewählten Filmen verschiedener Kategorien.

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


Der *libhugin-harvest* Prototyp der für die Beschaffung der Metadaten verwendet
wird hat die Folgenden Movie--Provider implementiert:

    * TMDb, multilingual, Online--Filmdatenbank (API)
    * OMDb, englischsprachig, Metadatenanbieter (API)
    * OFDB, deutschsprachig, Online--Filmdatenbank (API)

    * Filmstarts.de, deutschsprachig, Filme--Plattform, (keine API)
    * Videobuster.de, deutschsprachig, Filme Verleihdienst (keine API)

Desweiteren wurden noch Person--Provider für TMDb und OFDb implementiert.

Für die Beschaffung der Metadaten wurden die IMDb--IDs von 2500 in einer Datei
gesammelt. Anschließend wurden über ein IMDb--Lookup--Script
(siehe :ref:`imdblookup_script`) alle deutschsprachigen Titel und
Erscheinungsjahre anhand der IMDb--ID bezogen und 2500 Ordner mit der Struktur
``[Filmtitel;Erscheinungsjahr;Imdbid`` mittels diesem Script angelegt und die
Metadaten mit Hilfe von *libhugin--harvest* über die fünf genannten Provider
bezogen.

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

Bei der Erhebung der Daten ist aufgefallen, dass der OFDb--Provider kaum
Metadaten findet. Nach kurzer Recherche war zu beobachten, dass hier der Zugriff
über die API sehr oft einen Timeout mit der Fehlermeldung ,,Fehler oder Timeout
bei OFDB Anfrage" liefert.

Eine genauere Analyse des Timeout--Verhaltens der Provider zeigt, dass die API
vom OFDb--Provider sehr instabil ist, hierzu wurden Metadaten für 100 Filme je
Provider gezogen. Tabelle :num:`fig-timeout` zeigt wie oft es zu Fehlern pro
Provider gekommen ist. Der Test wurde hier, um gegebenenfalls Server oder
Leitungsprobleme  auszuschließen, an drei verschiedenen Tagen durchgeführt. Für
den Test wurde das Script aus :ref:``


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

Der OFDb--Provider verteilt die Anfragen über ein Gateway, siehe :cite:`ofdbgw`.
Während der Entwicklung hat sich gezeigt, dass Anfragen über das ofdbgw zu
falschen oder unvollständigen Ergebnisse führten. Ein Testen der einzelnen
Mirror ergab, dass ``http://ofdbgw.geeksphere.de`` als einziger Mirror die
erwarteten Ergebnisse lieferte. Dieser wurde somit im Prototypen direkt als
einziger Mirror aktiviert.

Abbildung :num:`fig-sourceresponse` zeigt eine weitere Analyse zeigt die
Rohperformance beim Zugriff auf die jeweiligen Plattformen/Metadatenanbieter.
Hier wurde mit dem Script im :ref:`source-response` die Zeit beim Zugriff
auf die implementierten Online--Plattformen gemessen. Für die Messung wurden die
in  :ref:`source-response` verwendeten Parameter verwendet. Die Anzahl der
Durchläufe war 10.

.. _fig-sourceresponse:

.. figure:: fig/source_response_time.pdf
    :alt: Normalisierung der Genreinformationen anhand statischer Mapping-Tabellen.
    :width: 100%
    :align: center

    Normalisierung der Genreinformationen anhand statischer Mapping-Tabellen.

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
Metadaten mittels der ``Beautiful-Soup``--Bibliothek aufwendig ist. Hier wäre es
ratsam die Bibliothek zu ändern oder alternativ auf ein anderes Verfahren wie
beispielsweise Reguläre Ausdrücke zurück zu greifen.

* Zugriff Threaded.

Um die bezogenen Metadaten weiter zu analysieren wurde der TMDb--Provider als
Referenz genommen.

* Genreverteilung
* Unterschiedliche Metadaten
