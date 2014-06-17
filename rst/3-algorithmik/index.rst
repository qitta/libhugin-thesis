.. _tech_grundlagen:

############################
Technische Grundüberlegungen
############################

Bestimmte Teile von *libhugin* arbeiten parallelisiert. Hierzu zählt
der Downloadmechanismus, sowie die Möglichkeit einer asynchronen Suchanfrage.

Auf weiteren Einsatz von Parallelisierung wurde verzichtet, da parallele
Verarbeitung unter Python aufgrund vom *GIL* (global interpreter lock) nur
eingeschränkt möglich ist.

Der *GIL* ist ein Mutex, welcher verhindert, dass mehrere native Threads Python
Bytecode gleichzeitig ausführen können. Die Parallelisierung von Funktionen kann
zu Performanceeinbußen im Vergleich zur Singlethreaded--Ausführung führen,
siehe Abbildung :num:`fig-gil-limitation`.  Zum Testen wurde das Skript im
:ref:`gil-limitation` verwendet, welches als Aufgabe die Dekrementierung einer
Variablen hat.

.. _fig-gil-limitation:

.. figure:: fig/gil_limitation.pdf
    :alt: Limitierung der Geschwindigkeit durch den global interpreter lock bei
          CPU-abhängigen Aufgaben. Hier wird über einer Funktion der Wert
          100.000.000 dekrementiert.
    :width: 100%
    :align: center

    Limitierung der Geschwindigkeit durch den global interpreter lock bei
    CPU-abhängigen Aufgaben. Hier wird über einer Funktion der Wert 100.000.000
    dekrementiert.

Diese Einschränkung gilt jedoch nicht für lange laufende oder blockierende
Operationen wie beispielsweise der Zugriff auf die Festplatte (vgl.
:cite:`hellmann2011python`).

Da der Zugriff auf Onlinequellen je nach Serverauslastung und Internetanbindung
in der Performance stark variiert, wurde das Herunterladen der Metadaten
parallelisiert. Das parallele Herunterladen zeigt deutliche
Geschwindigkeitsvorteile im Vergleich zur seriellen Verarbeitung (siehe
Abbildung :num:`fig-threaded-download`).

Zum Herunterladen wird auf die Python HTTP--Bibliothek *urllib* verzichtet, weil
diese grundlegende HTTP--Standards, wie beispielsweise Kompression, nicht
unterstützt.

Zwei weitere HTTP--Bibliotheken unter Python sind die beiden freien
Implementierungen *urllib3* und *httplib2*, auf welche zurückgegriffen werden
kann. Bei aktivierter Kompression, hier ist im RFC1951-RFC1952 der *deflate*
und *gzip* Algorithmus vorgesehen, wird der Inhalt vor dem Versenden komprimiert
und auf Empfängerseite transparent dekomprimiert. Textdateien lassen sich in
der Regel gut komprimieren. Durch die Kompression müssen weniger Daten
übertragen werden, was sich bei großen Datenmengen und einer geringen Bandbreite
auf die Performance auswirken kann.

Folgende Python--Sitzung zeigt die Standard HTTP--Bibliothek *urllib* der Python
Standardbibliothek. Diese erhält den komprimierten Inhalt, kann diesen
jedoch nicht dekomprimieren, da dieses HTTP--Standardfeature nicht beherrscht
wird:

.. code-block:: python

   >>> from urllib.request import urlopen
   >>> urlopen('http://httpbin.org/gzip').read()
   b'\x1f\x8b\x08\x00\xc0\xa5\x8bS\x02\xff5\x8f\xc1n\x830\x10D\xef\xf9\n\xe4s\xec\[...]'


Im Gegenzug dazu wird der Zugriff über *urllib3*-- und die
*httplib2*--Bibliothek auf die gleiche Ressource gezeigt (gekürzte Version):

.. code-block:: python

   >>> from httplib2 import Http
   >>> Http().request('http://httpbin.org/gzip')
   b'{\n  "gzipped": true,\n  "headers": {\n    "Accept-Encoding": "gzip, deflate"[...]'

   >>> import urllib3
   >>> urllib3.PoolManager(1).request(url='http://httpbin.org/gzip', method='GET').data
   b'{\n  "gzipped": true,\n  "headers": {\n    "Accept-Encoding": "identity",\n [...]'


Aufgrund der genannten Eigenschaften und der vergleichsweise guten Performance
(siehe Abbildung :num:`fig-threaded-download`) wurde für *libhugin* die
*httplib2*--Bibliothek gewählt. Da diese jedoch nicht Thread--Safe ist, wird
hier der in der Google Developer API genannte Ansatz (siehe :cite:`gdev`), eine
Instanz pro Thread zu starten, gewählt.

Abbildung :num:`fig-threaded-download` zeigt wie sich das Parallelisieren
mehrerer Downloads auf die Performance auswirkt. Hier wurden die drei genannten
HTTP--Bibliotheken mit dem Script in :ref:`http_benchmark` getestet.  Der
Benchmark wurde mit einer *VDSL* 50Mbit--Leitung durchgeführt.

.. _fig-threaded-download:

.. figure:: fig/threaded_download.pdf
    :alt: Performancevorteil beim Parallelisieren von Downloads.
    :width: 100%
    :align: center

    Performancevorteil beim Parallelisieren von Downloads. Durchschnitt aus drei
    Durchläufen, jeweils mit Zugriff auf 15 verschiedene Webseiten.


#########################
Algorithmik der Filmsuche
#########################

Für die Suche nach Filmmetadaten gibt es unter *libhugin* mehrere Möglichkeiten.
Je nach Metadaten--Provider ist eine Suche nach IMDb--ID und Titel möglich. Die
IMDb--ID ist eine von IMDb.com festgelegte einzigartige ID für einen Film.

Folgende Python--Shell Sitzung zeigt wie eine Metadaten Suchanfrage
funktioniert:

.. code-block:: python

    >>> from hugin.harvest.session import Session
    >>> s = Session()
    >>> q = s.create_query(title='The Matrix')
    >>> r = s.submit(q)
    >>> print(r)
    [<tmdbmovie <picture, movie> : The Matrix (1999)>,
     <ofdbmovie <movie> : Matrix (1999)>,
     <filmstartsmovie <movie> : Matrix (1999)>]

Beim Erstellen der Sitzung können *libhugin* Konfigurationsparameter übergeben
werden, wie beispielsweise:

    * Cache Pfad, Pfad zum lokalen HTTP--Anfragen Zwischenspeicher.
    * Anzahl paralleler Downloads per Thread

Anschließend muss eine Suchanfrage erstellt werden. Dazu gibt es die
Möglichkeit, die Methode ``create_query()`` zur Hilfe zu nehmen. Hier hat der
Benutzer eine Vielzahl von Möglichkeiten, seine Suchanfrage zu konfigurieren.

Der letzte Schritt ist das Absenden der Suchanfrage. Hier gibt es die
Möglichkeit einer *synchronen* (``submit()``--Methode) oder einer *asynchronen*
Anfrage (``submit_async()``--Methode). Der Hauptunterschied ist, dass die
*asynchrone* Anfrage im Gegensatz zu der *synchronen* nicht blockiert. Der
Aufrufer der Methode kann also in der Zwischenzeit andere Aufgaben erledigen.

Siehe :cite:`cpiechula` und *libhugin* API :cite:`rtfd` für eine vollständige
Liste der Konfigurationsparameter der Session und der Query.

.. _standardsuche:

Standardsuche
=============

Bei der Suchanfrage über den Filmtitel wird von den Onlinequellen in der Regel
eine Liste mit mehreren Möglichkeiten geliefert. Das Provider--Plugin muss
anschließend die Filmtitel mit der größten Übereinstimmung herausfinden. Für die
Ähnlichkeit bei der Suche nach übereinstimmenden Zeichenketten, wurde ein
Ähnlichkeitsmaß definiert, welches eine Spanne von 0.0 (keine Ähnlichkeit) bis
1.0 (volle Übereinstimmung) aufweist.

Der Vergleich der Zeichenketten sollte möglichst fehlertolerant sein und
Zeichenketten mit der höchsten Übereinstimmung liefern.

Ein simpler Vergleich wie beispielsweise

.. code-block:: python

    >>> "The Matrix" == "The Matrix"
    True
    >>> "The Matrix" == "The matrix"
    False


funktioniert nur bei exakt den gleichen Zeichenketten. Des Weiteren ist so auch
die Umsetzung einer Werte--Spanne nicht möglich. Für den Vergleich von
Zeichenketten bietet die Python Standard--Bibliothek das *difflib*--Modul. Das
Modul erlaubt es, zwei Sequenzen zu vergleichen. Es arbeitet mit dem
Ratcliff--Obershelp--Algorithmus und hat eine Komplexität von :math:`O(n^{3})`
im *worst case* und eine erwartete Komplexität von :math:`O(n^{2})`. Der
Algorithmus basiert auf der Idee, die Anzahl der Sequenzen mit
übereinstimmenden Zeichen multipliziert mit zwei, durch
die Summe der Länge der beiden Zeichenketten zu teilen (vgl :cite:`ratcliffpattern`).

Ein weiteres Maß für die Ähnlichkeit von Zeichenketten ist die Hamming--Distanz.
Diese Distanz arbeitet nach der Idee, die ,,Ersetzungen" zu zählen. Der
Algorithmus hat jedoch die Einschränkung, dass er sich nur auf gleich lange
Zeichenketten anwenden lässt (vgl. :cite:`navarro2001guided`,
:cite:`ranka2009ic3`).

Ein weiterer Algorithmus, der für Zeichenkettenvergleiche eingesetzt wird, ist
der Levenshtein--Algorithmus (auch Levenshtein--Distanz genannt). Der
Algorithmus hat eine Laufzeitkomplexität von :math:`O(nm)`. Die
Levenshtein--Distanz basiert auf der Idee, die minimalen Editiervorgänge
(Einfügen, Löschen, Ersetzen), um von einer Zeichenkette auf eine andere zu
kommen (vgl :cite:`atallah2010algorithms`, :cite:`navarro2001guided`,
:cite:`ranka2009ic3`), zu zählen. Die normalisierte Levenshtein--Distanz bewegt sich
zwischen 0.0 (Übereinstimmung) und 1.0 (keine Ähnlichkeit).

Eine Erweiterung der Levenshtein--Distanz ist die Damerau--Levenshtein--Distanz.
Diese wurde um die Funktionalität erweitert, vertauschte Zeichen zu erkennen.
Um die Zeichenkette *,,The Matrix"* nach *,,Teh Matrix"* zu überführen, sind bei
der Levenshtein--Distanz zwei Operationen nötig, die
Damerau--Levenshtein--Distanz hingegen benötigt nur eine Operation wie die
folgende *IPython*--Sitzung zeigt:

.. code-block:: python

    >>> from pyxdameraulevenshtein import damerau_levenshtein_distance
    >>> from distance import levenshtein as levenshtein_distance
    >>> levenshtein_distance("the matrix", "teh matrix")
    >>> 2
    >>> damerau_levenshtein_distance("the matrix", "teh matrix")
    >>> 1

Von der Levenshtein- und Damerau--Levenshtein--Distanz gibt es jeweils eine
normalisierte Variante. Hierbei bewegt sich die Distanz zwischen 0.0 und 1.0.
Dies wird dadurch erreicht, indem die Anzahl der Operationen durch die Länge der
längeren der beiden Zeichenketten geteilt wird.

Da es bei der Filmsuche zu vielen Zeichenkettenvergleichen kommt sollte der
Algorithmus zum Vergleich von Zeichenketten performant sein.

Um die jeweiligen Algorithmen, beziehungsweise die Implementierungen dieser,
bezüglich der Performance zu überprüfen, wurde eine Messung mit den folgenden
unter Python verfügbaren Implementierungen durchgeführt:

    * difflib, Modul aus der Python--Standardbibliothek  (Ratcliff-Obershelp)
    * pyxDamerauLevenshtein, auf C basierte Implementierung von Damerau--Levenshtein
    * distance, externes Modul mit Levenshtein--Implementierung in C

.. _fig-stringcompare:

.. figure:: fig/algo_compare.pdf
    :alt: String comparsion algorithms.
    :width: 100%
    :align: center

    Performancevergleich der Algorithmen für den Zeichenkettenvergleich in
    Abhängigkeit von der Zeichenkettenlänge. Pro Vergleich 50 Durchläufe. Die
    Länge der jeweils verglichenen Zeichenketten, ist die Basis--Zeichenkette,
    mit dem Faktor multipliziert.

Abbildung :num:`fig-stringcompare` zeigt, dass die Laufzeit--Komplexität bei
allen drei Algorithmen ähnlich ist. Des Weiteren zeigt die Abbildung, dass die
beiden Implementierungen *distance* (C) und *pyxDamerauLevenshtein* (C) sehr
performant im Vergleich zur *difflib* (Python) Implementierung arbeiten.
Aufgrund der Tatsache, dass der Damerau--Levenshtein--Algorithmus vertauschte
Zeichen ,,erkennen" kann und gleichzeitig performant implementiert ist, wurde er
für den Einsatz in der Bibliothek gewählt.

Der Benchmark wurde mit dem Skript aus :ref:`string_comparsion_algorithms`
durchgeführt.

Je nach verwendeten Algorithmus variiert das Ergebnis leicht. Das liegt daran,
dass die Algorithmen eine unterschiedliche Idee verfolgen.

Folgende interaktive *IPython*--Sitzung zeigt das Ergebnisverhalten von *difflib*
und *pyxDamerauLevenshtein*. Da das Ähnlichkeitsmaß bei der zu letzt genannten
Implementierung eine ,,Distanz" ist, wird das Ergebnis zu einem Ähnlichkeitsmaß
modifiziert (durch das Abziehen von eins), um das Verhalten besser
vergleichen zu können.

.. code-block:: python

    >>> difflib.SequenceMatcher(None, "Katze", "Fratze").ratio()
    0.7272727272727273
    >>> 1 - normalized_damerau_levenshtein_distance("Katze", "Fratze")
    0.6666666666666667

Weitere Werte, um die unterschiedliche Wertung der beiden Algorithmen zu
demonstrieren, finden sich in der Tabelle :num:`fig-comparsion-diff-1` und
:num:`fig-comparsion-diff-2`. Die Werte wurden mit dem Script in
:ref:`comparsion-rating` ermittelt.

.. figtable::
    :label: fig-comparsion-diff-1
    :caption: Ähnlichkeitswerte ermittelt mit Damerau-Levenshtein.
    :alt: Ähnlichkeitswerte Damerau-Levenshtein.

    +---------------+----------------+----------------+-----------------+---------------+
    |               | **Superman**   | **Batman**     | **Iron-Man**    | **Spiderman** |
    +===============+================+================+=================+===============+
    | **Superman**  | 1.0            | 0.38           | 0.25            | 0.67          |
    +---------------+----------------+----------------+-----------------+---------------+
    | **Batman**    | :math:`\times` | 1.0            | 0.25            | 0.33          |
    +---------------+----------------+----------------+-----------------+---------------+
    | **Iron-Man**  | :math:`\times` | :math:`\times` | 1.0             | 0.22          |
    +---------------+----------------+----------------+-----------------+---------------+
    | **Spiderman** | :math:`\times` | :math:`\times` |  :math:`\times` | 1.0           |
    +---------------+----------------+----------------+-----------------+---------------+

.. figtable::
    :label: fig-comparsion-diff-2
    :caption: Ähnlichkeitswerte ermittelt mit Ratcliff-Obershelp.
    :alt: Ähnlichkeitswerte ermittelt mit Ratcliff-Obershelp.

    +---------------+----------------+----------------+----------------+---------------+
    |               | **Superman**   | **Batman**     | **Iron-Man**   | **Spiderman** |
    +===============+================+================+================+===============+
    | **Superman**  | 1.0            |  0.43          | 0.38           | 0.82          |
    +---------------+----------------+----------------+----------------+---------------+
    | **Batman**    | :math:`\times` | 1.0            | 0.29           |  0.4          |
    +---------------+----------------+----------------+----------------+---------------+
    | **Iron-Man**  | :math:`\times` | :math:`\times` | 1.0            | 0.35          |
    +---------------+----------------+----------------+----------------+---------------+
    | **Spiderman** | :math:`\times` | :math:`\times` | :math:`\times` | 1.0           |
    +---------------+----------------+----------------+----------------+---------------+


Da der Vergleich von der Groß-- und Kleinschreibung abhängig ist, fällt die
Ähnlichkeit der Titel *,,Sin"* und *,,sin"*, wie folgende *IPython*--Sitzung
zeigt, unterschiedlich aus:

.. code-block:: python

    >>> 1 - normalized_damerau_levenshtein_distance("sin", "Sin")
    0.6666666666666667

Um dieses Problem zu beheben, wird die gesuchte Zeichenkette vor dem Vergleich
normalisiert. Dies geschieht indem alle Zeichen der Zeichenkette in Klein--
beziehungsweise alternativ in Großbuchstaben umgewandelt werden. Folgendes
Beispiel zeigt die Normalisierung mittels der in Python integrierten
``lower()``--Funktion:

.. code-block:: python

    >>> 1 - normalized_damerau_levenshtein_distance("sin".lower(), "Sin".lower())
    1.0

Während der Entwicklung ist aufgefallen, dass der implementierte OFDb--Provider
den Film *,,The East (2013)"* nicht finden konnte. Nach längerer Recherche und
Ausweitung der gewünschten Ergebnisanzahl auf 100 Ergebnisse, wurde
festgestellt, dass der Film auf dem letzten Platz der Suchergebnisse (Platz 48)
zu finden war. Die vorherigen Plätze waren mit Filmtiteln wie ,,The Queen of the
East" oder ,,Horror in the East" besetzt.

Dies lag daran, dass der Film auf dieser Online--Plattform in der Schreibweise
*,,East, The"* gepflegt ist. Dies ist eine valide und nicht unübliche
Schreibweise, um Filme alphabetisch schneller zu finden.

Betrachtet man die Ähnlichkeit der beiden Zeichenketten, so stellt man fest,
dass bei dieser Schreibweise, je nach Algorithmus, eine geringe bis gar keine
Ähnlichkeit vorhanden ist, wie folgende *IPython* Sitzung zeigt:

.. code-block:: python

    >>> import difflib
    >>> from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
    >>> difflib.SequenceMatcher(None, "The East", "East, The").ratio()
    0.47058823529411764
    >>> 1 - normalized_damerau_levenshtein_distance("The East", "East, The")
    0.0

Um dieses Problem zu umgehen, müssen die Filmtitel auf ein bestimmtes Schema
normalisiert werden. Ein möglicher Ansatz wäre, den Artikel zu entfernen. Dies
würde jedoch das Problem mit sich bringen, dass Filme wie *,,Drive (2011)"* und
*"The Drive (1996)"* fälschlicherweise als identisch erkannt werden würden. Ein
weiteres Problem, welches hinzu kommt ist, dass der Artikel--Ansatz
sprachabhängig ist.

Ein anderer Ansatz, der bei *libhugin* gewählt wurde, ist, die
Satztrennungszeichen zu entfernen und die einzelnen Wörter des Titels
alphabetisch zu sortieren.

Anhand des Beispieltitel *,,East, The"* wird folgend das Vorgehen erläutert:

    1. Titel auf Kleinschreibung umwandeln →  ``'east, the'``
    2. Satztrennungszeichen wie ,,,", ,,-" und ,,:" werden entfernt → ``'east the'``
    3. Titel anhand der Leerzeichen aufbrechen und in Liste umwandeln → [``'east'``, ``'the'``]
    4. Liste alphabetisch sortieren und in Zeichenkette zurückwandeln → ``'east the'``
    5. Vergleich mittels Damerau--Levenshtein Algorithmus

Wendet man diesen Ansatz auf ,,The East" und ,,East, The" an, so erhält man in
beiden Fällen die Zeichenkette "east the". Die Umsetzung dieses Algorithmus bei der
Titelsuche löst das Problem beim OFDb--Provider. Der eben genannte Film wird
durch die Normalisierung gefunden und erscheint an der ersten Position.

Diese Vorgehensweise normalisiert ebenso die Personensuche. Hier wird
beispielsweise der Name *,,Emma Stone"* und *,,Stone, Emma"* in beiden Fällen zu
der Zeichenkette ``'emma stone'``.

Die Anpassungen des Algorithmus für den Zeichenkettenvergleich wirken sich nur
wenig auf die Performance aus.  Abbildung :num:`fig-finalstringcompare` zeigt
den Performanceunterschied zum ursprünglichen Algorithmus.

.. _fig-finalstringcompare:

.. figure:: fig/adjusted_algo_compare.pdf
    :alt: Angepasster Algorithmus auf Basis von Damerau-Levenshtein im
          Vergleich zu den ursprünglichen Algorithmen.
    :width: 100%
    :align: center

    Angepasster Algorithmus auf Basis von Damerau-Levenshtein im Vergleich zu
    den ursprünglichen Algorithmen.

Ein weiteres Attribut, das bei der Suche von Filmen angegeben werden kann, ist
das Erscheinungsjahr. Dieses wird verwendet, um Suchergebnisse genauer
einzugrenzen.

Wird der Titel und ein Erscheinungsjahr bei der Suche angegeben, so
kann der ,,richtigere" Film näherungsweise durch das Erscheinungsjahr ermittelt
werden.  Beim simplen Vergleich des Jahres mittels Damerau--Levenshtein
Algorithmus ergibt sich hier jedoch ein neues Problem.

Bei zusätzlicher Anwendung des Damerau--Levenshtein--Algorithmus auf das
Erscheinungsjahr, kann es zu dem Fall kommen, dass das logisch gesehen
,,nähere" Erscheinungsjahr als ,,schlechter" gewertet wird. Das liegt daran,
dass es Fälle gibt, bei denen der logische Jahresunterschied zum Suchstring
geringer sein kann, als der Zeichenkettenunterschied. In diesem Fall würde ein
Film, der den gleichen Titel hat, aber zeitlich gesehen viel weiter vom gesuchten
Film entfernt ist, als ,,besser" bewertet werden.

Folgende *IPython*--Sitzung zeigt die Problematik:

.. code-block:: python

   >>> 1 - normalized_damerau_levenshtein_distance("Drive 2000", "Drive 2011")
   0.8
   >>> 1 - normalized_damerau_levenshtein_distance("Drive 2000", "Drive 1997")
   0.6

Bei separater Betrachtung der Zeichenkette für das Jahr würde die Differenz noch
größer ausfallen, da die beiden Zeichenketten ,,1997" und ,,2000" keine
Ähnlichkeit aufweisen, die Zeichenketten ,,2000" und ,,2011" eine Ähnlichkeit
von 0.5 aufweisen.

Logisch betrachtet ist das Jahr ,,1997" jedoch viel näher an dem gesuchten
Erscheinungsjahr. Was im Beispiel darauf hindeuten würde, dass der Benutzer das
exakte Jahr nicht mehr wusste, jedoch den Zeitraum mit einer Abweichung von drei
Jahren angeben konnte.

Die genannte Problematik äußert sich beispielsweise auch bei Film--Remakes oder
Filmen, die mit einer Ungenauigkeit von :math:`\pm 1` Jahr auf
einer Plattform eingepflegt wurden. Nach Beobachtung des Autors gibt es hier
zwischen den Onlinequellen für den gleichen Film vereinzelt Differenzen beim
Erscheinungsjahr.

Ob dieser Umstand weiterhin präsent ist, beziehungsweise wie oft dieser Fall
vorkommt, zeigt die Auswertung der Stichprobe der Metadaten mehrerer
Onlinequellen (siehe Analyse der Erscheinungsjahrdifferenz :ref:`yeardiff`).

Um das Problem abzumildern wird beim Selektieren der Ergebnisse das Jahr
einzeln betrachtet. Hier wird mittels folgender Funktion die Ähnlichkeit
berechnet:

 .. math::

    year\_similarity(year_a, year_b, max_{years}) = 1 - min \left\{ 1, \frac{\vert year_{a} - year_{b}  \vert}{max_{years}} \right\}

:math:`max_{years}` ist hierbei die maximale Anzahl von Jahren, die betrachtet
werden sollen.

Anschließend wird das Jahr noch zusätzlich gewichtet, da der Titel wichtiger
als das Erscheinungsjahr ist. Durch die Gewichtung soll dies sichergestellt werden.

 .. math::

    similarity(t_a, y_a, t_b, y_b) = \frac{string\_similarity\_ratio(t_a, t_b) \times weight + year\_similarity(y_a, y_b)}{weight + 1}

:math:`t_a, t_b` sind die jeweiligen Titel.

:math:`y_a, y_b` sind die jeweiligen Erscheinungsjahre.

``string_similarity_ratio`` ist die angepasste Damerau--Levenshtein Funktion für den Zeichenkettenvergleich.

:math:`weight` ist hierbei der Gewichtungsfaktor für den Titel. Durch die
Gewichtung des Titels fällt ein falsch gepflegtes Erscheinungsjahr nicht so
stark ins Gewicht wie ein ,,Buchstabendreher" beim Titel. Dies ist ein gewolltes
Verhalten, da das Jahr nur unterstützend beim Filtern der Ergebnismenge
verwendet werden soll.

.. figtable::
    :label: fig-rating
    :caption: Unterschied im Rating bei gewichteter Betrachtung des Titels.
    :alt: Unterschied im Rating bei gewichteter Betrachtung des Titels.

    +------------------+-------------------------------------+------------------------------------+
    | **Titel**        | **Rating mit Gewichtung, weight=3** | **Rating mit Damerau-Levenshtein** |
    +==================+=====================================+====================================+
    | Matrix 1999      | 1.0                                 | 1.0                                |
    +------------------+-------------------------------------+------------------------------------+
    | Matrix 2000      | 0.983                               | 0.636                              |
    +------------------+-------------------------------------+------------------------------------+
    | Matrix 1997      | 0.967                               | 0.909                              |
    +------------------+-------------------------------------+------------------------------------+
    | Matrix 2001      | 0.967                               | 0.636                              |
    +------------------+-------------------------------------+------------------------------------+
    | Matrix, The 1999 | 0.7                                 | 0.538                              |
    +------------------+-------------------------------------+------------------------------------+
    | The Matrix 2013  | 0.467                               | 0.467                              |
    +------------------+-------------------------------------+------------------------------------+
    | The East 1999    | 0.438                               | 0.538                              |
    +------------------+-------------------------------------+------------------------------------+


Abbildung :num:`fig-rating` zeigt das Rating mit einer
Gewichtung von :math:`weight` = 3 für die Zeichenkette ,,Matrix 1999". Das
Skript für die Auswertung findet sich im :ref:`gewichtetes_rating`.


IMDb--ID Suche
==============

Ob die Suche nach der IMDb--ID möglich ist, hängt von der jeweiligen Onlinequelle
ab. Onlinequellen wie TMDb, OFDb oder auch OMDb unterstützen direkt die Suche
über die IMDb--ID. Andere Onlinequellen, wie das Filmstarts- oder das
Videobuster--Portal unterstützen keine Suche über IMDb--ID.

Um trotzdem eine onlinequellenübergreifende Suche über die IMDb--ID zu
ermöglichen, bietet die *libhugin--harvest*--Bibliothek den sogenannten
,,Lookup--Mode".

Hierbei wird intern vor der Metadatensuche ein sogenannter *Lookup*
durchgeführt, um zu der gesuchten IMDb--ID den passenden Filmtitel zu ermitteln.
Dies ist über die Suche auf IMDb.com möglich.  Die Filme auf der Seite sind
jeweils unter der jeweiligen IMDb--ID eingepflegt. Die URL für den Film *,,Only
god forgives (2013)"* mit der IMDb--ID ``tt1602613`` ist wie folgt aufgebaut:

    * http://www.imdb.com/title/tt1602613

Wenn der *Lookup--Mode* aktiviert wird, wird vor der Kommunikation mit den
Provider--Plugins ein *Lookup* über ``http://imdb.com`` getriggert. Hierbei
wird die URL aus der zu suchenden ID zusammengesetzt und eine IMDb Anfrage
gestartet. Anschließend wird auf dem zurückgelieferten HTTP--Response ein
Regulärer Ausdruck ausgeführt, welcher die Zeichenkette bestehend aus
``<Titelname> <(4-stellige Jahreszahl)>``, extrahiert.

Der algorithmische Ansatz sieht unter Python wie folgt aus:

.. code-block:: python

   >>> imdbid = "tt1602613"  # id for only god forgives
   >>> request = requests.get('http://www.imdb.com/title/{}'.format(imdbid))
   >>> title, year = re.search('\>(.+?)\s*\((\d{4})', request.text).groups()
   >>> print(title, year)
   'Only God Forgives 2013'

Nach dem Extrahieren der Attribute Titel und Erscheinungsjahr, wird die Query
mit den Suchparametern, welche an alle Provider--Plugins für die Suche
weitergegeben wird, mit diesen ergänzt. Die Provider--Plugins, die keine IMDb--ID
unterstützen, können so eine Suche über den Titel und das Erscheinungsjahr
durchführen. Für den Benutzer sieht dies nach außen so aus, als würde jeder
Provider eine IMDb--ID Suche unterstützen.

Unschärfesuche
==============

Die Onlinequellen der implementierten Provider, TMDb, IMDb, OFDb, OMDb,
Filmstarts und Videobuster benötigen in der Regel exakte Suchanfragen. Bei einem
Tippfehler wie *,,Unly god forgives"* (Originaltitel: *,,Only god forgives"*),
wird der Film von den genannten Online--Plattformen nicht gefunden.

.. code-block:: python

    >>> from hugin.harvest.session import Session
    >>> s = Session()
    >>> q = s.create_query(title='Unly god forgives', fuzzysearch=False)
    >>> r = s.submit(q)
    >>> print(r)
    []

Diesen Fehler auf Seite von *libhugin* zu beheben ist schwierig. Man müsste eine
große Datenbank an Filmtiteln pflegen und aktuell halten und könnte so mit
Hilfe dieser den Fehler vom Benutzer korrigieren, indem man die ähnlichste aller
Zeichenketten aus der Datenbank nehmen würde. Mit der angepassten
Damerau--Levenshtein--Ähnlichkeit, die *libhugin* zum Zeichenkettenvergleich
anbietet, hätte die falsche Anfrage eine Ähnlichkeit von 0.94.

Eine lokale beziehungsweise zentrale Datenbank aufzubauen wäre möglich, da die
Informationen beziehungsweise Metadaten online auf vielen Plattformen verfügbar
sind. Diese Datenbank aktuell zu halten ist jedoch schwierig, da nicht bekannt
ist auf welchen Plattformen ein Film überhaupt gepflegt ist, beziehungsweise wie
aktuell die gepflegten Informationen sind.

Um dieses Problem trotz der genannten Schwierigkeiten zu lösen, bedient sich
*libhugin* eines anderen Ansatzes. *Libhugin* delegiert die Information, wie es
ein Mensch auch machen würde, an eine Suchmaschine. Im konkreten Fall wird
hierbei ein *Lookup* über die Suchmaschine von Google getriggert.

Über die *,,I'm Feeling Lucky"*--Funktionalität erlaubt es Google über Parameter
die Suchanfrage so zu konfigurieren, dass als Antwort keine Liste mit
Suchergebnissen zurückgeliefert wird, sondern die Seite mit der höchsten
Übereinstimmung zum Suchergebnis. Hierzu muss die Suchanfrage die Option
``btnI=1`` als URL--Queryparameter enthalten. Folgendes Beispiel zeigt die
Suchanfrage zum Wikipedia--Artikel ,,Hauskatze" mit Parameter für die *,,I'm
Feeling Lucky"*--Funktionalität:

    * http://www.google.com/search?hl=de&q=Hauskatze&btnI=1

Gibt man diese URL direkt im Browser ein, so wird direkt der Wikipedia--Artikel
zur Hauskatze [#f1]_ angezeigt.

*Libhugin* bedient sich dieser Funktionalität und führt einen *Lookup* mit den
Parametern *Filmtitel*, *Erscheinungsjahr*, *imdb* und *movie* aus. Anschließend
wird die zurückgegebene URL betrachtet und aus dieser die IMDb--ID extrahiert.

Folgende *IPython*--Sitzung zeigt den Ansatz:

.. code-block:: python


    >>> fmt = 'http://www.google.com/search?hl=de&q={title}+{year}+imdb+movie&btnI=1'
    >>> url = requests.get(fmt.format(title='Drive', year='2011'))).url
    >>> imdbid = re.findall('\/tt\d*/', url)
    >>> imdbid.pop().strip('/')
    'tt0780504'

Hier wurde der Ansatz gewählt, die IMDb--ID aus der URL mit einem Regulären
Ausdruck zu parsen. Dies erspart das Parsen der kompletten HTTP--Response, was
deutlich aufwendiger wäre.

Dies geschieht vor der Kommunikation mit den Provider--Plugins. Anschließend
wird die Suche mit der IMDb--ID normal fortgesetzt. Alternativ wäre hier der
Ansatz über den Filmtitel, wie beim IMDb--ID--zu--Titel--*Lookup* möglich. Diese
Funktionalität lässt sich durch das zusätzliche Aktivieren des
,,IMDb--Lookup"--Mode realisieren.


Normalisierung des Genre
========================

Die Normalisierung der Metadaten aus unterschiedlichen Quellen ist sehr
schwierig, da es bei den Filmmetadaten keinen einheitlichen Standard gibt. Um
fehlerhafte oder fehlende Metadaten über unterschiedliche Quellen zu ergänzen,
müssen die Metadatenattribute, insbesondere das Genre, aufgrund der in Kapitel
:ref:`motivation` gelisteten Problematik, normalisiert werden.

Durch den in Kapitel :ref:`motivation` (siehe Abbildung
:num:`fig-genre-redundanzen`, Abbildung :num:`fig-genre-detail`) genannten
Umstand werden die Genreinformation redundant in der Datenbank der
Abspielsoftware, wie beispielsweise dem XBMC--Media--Center, abgelegt. Es ist
nicht mehr möglich, ein Filmgenre eindeutig zu identifizieren. Es ist somit
weder eine Gruppierung nach diesem Genre noch eine eindeutige Filterung
möglich.

Dieses Problem betrifft grundsätzlich alle Filmmetadaten--Attribute, jedoch
lassen sich andere Attribute wie die Inhaltsbeschreibung problemlos austauschen,
da diese von Natur aus individuell ist und sich somit nicht normalisieren lässt.

Da das Filmgenre, neben der Inhaltsbeschreibung und Filmbewertung, nach Meinung
des Autors, zu den wichtigsten Auswahlkriterien bei Filmen zählt, wurde bei
*libhugin* ein statisches Konzept der Normalisierung umgesetzt.

Die Normalisierung bei *libhugin* bildet hierzu jedes Genre einer Onlinequelle
auf einem globalen Genre ab. Die Normalisierung erfolgt über eine statische
Genre--Tabelle, welche der Autor eines Provider--Plugins bereitstellen muss. Der
Nachteil dieser Variante ist, dass das Genrespektrum der Onlinequelle bekannt
sein muss. Das Provider--Genre wird über einen Index auf einem globalen Genre
abgebildet.

Abbildung :num:`fig-genrenorm` zeigt konzeptuell die Vorgehensweise beim
,,Normalisieren" der Genreinformationen.

.. _fig-genrenorm:

.. figure:: fig/genre_norm.pdf
    :alt: Normalisierung der Genreinformationen anhand statischer Mapping-Tabellen.
    :width: 100%
    :align: center

    Normalisierung der Genreinformationen anhand statischer Mapping-Tabellen.

Wird keine ,,Genremapping--Tabelle" bereitgestellt, so kann das Genre nicht
normalisiert werden. In diesem Fall kann es zu der oben genannten Problematik
kommen. Das Genremapping muss pro Sprache gepflegt werden, der Prototyp besitzt
im aktuellen Zustand eine globale Genre--Tabelle für die deutsche und die
englische Sprache.

Ein weiterer Ansatz bei der Genrenormalisierung war die automatische Erkennung
des Genres anhand der Wortähnlichkeit. Dies erwies sich jedoch als nicht
praxistauglich. Eine automatische Genreerkennung benötigt einen Wortschatz aus
Referenz--Genres, mit welchen das unbekannte Provider--Genre verglichen werden
muss. Bei Genres wie Science--Fiction, Drama oder Thriller funktioniert das
System noch relativ gut. Kommen aber seltene oder unbekannte Genrenamen wie
,,Mondo" oder ,,Suspense" hinzu, kann je nach Referenz--Wortschatz keine
Übereinstimmung mehr erfolgen. Hier wäre noch ein semiautomatischer Ansatz
denkbar, welcher automatisiert Genres erkennt und im Fall eines unbekannten
Genre dieses in eine Liste aus nicht zugeordneten Genres hinzufügt, welche dann
vom Benutzer korrigiert werden können. Dies ist jedoch bei einer
Software--Bibliothek wie sie durch *libhugin* bereitgestellt wird, weniger
praktikabel.

Ein weiteres Problem das hier jedoch hinzukommt ist, dass das Genre an sich
in keiner Form standardisiert ist. Je nach Onlinequelle gibt es
Genrebezeichnungen wie Animationsfilm oder Kinderfilm, welche jedoch im engeren
Sinne nicht zum ,,Filmgenre"--Begriff gezählt werden dürften (siehe
:cite:`wikigenre`). Des Weiteren kommt hinzu, dass im Laufe der Zeit immer
wieder neue Genre entstanden sind.


Suchstrategien
==============

Der Prototyp der *libhugin--harvest*--Bibliothek unterstützt zwei verschiedene
Suchstrategien. Eine *,,deep"*--Strategie und eine *,,flat"*--Strategie. Diese
beiden Strategien sollen dem Benutzer die Kontrolle über die ,,Suchtrefferart"
geben.

Jedes Provider--Plugin hat aktuell eine vergebene Priorität. Diese ist im
Prototypen von *libhugin* manuell vergeben worden. Die Priorität ist ein
Integer--Wert im Bereich 0-100. Je höher die Priorität, desto mehr wird ein
Provider beim abschließenden Filtern der Ergebnisse berücksichtigt.

Die gefundenen Ergebnisse können einerseits nach Provider--Priorität betrachtet
oder aber nach ,,Ergebnisqualität" betrachtet werden. Aus diesem Grund wurde die
*,,deep"*-- und die *,,flat"*--Suchstrategie implementiert.

.. _fig-searchstrategy:

.. figure:: fig/searchstrategy.pdf
    :alt: Suchstrategien. Suche nach dem Film ,,Drive (2011)" mit der Begrenzung der Suchergebnisse auf fünf.
    :width: 80%
    :align: center

    Suchstrategien. Suche nach dem Film ,,Drive (2011)" mit der Begrenzung der Suchergebnisse auf fünf.

Bei der *,,deep"*--Strategie werden die Ergebnisobjekte nach Provider (Priorität)
gruppiert und die Ergebnisse innerhalb jeder Gruppe nach Übereinstimmung mit
der gesuchten Zeichenkette sortiert.

Anschließend werden die Ergebnisse, angefangen beim Provider mit der höchsten
Priorität, zurückgeliefert bis die gewünschte Anzahl an Ergebnissen
zurückgegeben wurde (siehe Abbildung :num:`fig-searchstrategy`).

Das folgende Beispiel zeigt das tatsächliche Ergebnis der im *libhugin*--Prototyp
implementierten ,,deep"--Strategie:

.. code-block:: python

    >>> from hugin.harvest.session import Session
    >>> s = Session()
    >>> q = s.create_query(title="drive", amount=7, strategy='deep')
    >>> s.submit(q)
    [<tmdbmovie <movie, picture> : Drive (2011)>,
     <tmdbmovie <movie, picture> : Drive (1998)>,
     <tmdbmovie <movie, picture> : Drive (2002)>,
     <ofdbmovie <movie> : Drive (2011)>,
     <ofdbmovie <movie> : Drive [Kurzfilm] (2011)>,
     <ofdbmovie <movie> : Drive (1997)>,
     <filmstartsmovie <movie> : Drive (2011)>]

Bei der *,,flat"*--Strategie werden die Provider und Ergebnisse auf die gleiche
Art wie bei der *,,deep"*--Strategie gruppiert und sortiert. Anschließend werden
aber jeweils die Ergebnisse mit der größten Übereinstimmung iterativ, angefangen
beim Provider mit der höchsten Priorität, zurückgeliefert bis die gewünschte
Anzahl erreicht ist.

Das folgende Beispiel zeigt das tatsächliche Ergebnis der im *libhugin*--Prototyp
implementierten ,,flat"--Strategie:

.. code-block:: python

    >>> from hugin.harvest.session import Session
    >>> s = Session()
    >>> q = s.create_query(title="drive", amount=7, strategy='flat')
    >>> s.submit(q)
    [<tmdbmovie <movie, picture> : Drive (2011)>,
     <ofdbmovie <movie> : Drive (2011)>,
     <filmstartsmovie <movie> : Drive (2011)>,
     <omdbmovie <movie> : Drive (2011)>,
     <videobustermovie <movie> : Drive (2011)>,
     <tmdbmovie <movie, picture> : Drive (1998)>,
     <ofdbmovie <movie> : Drive [Kurzfilm] (2011)>]

Abbildung :num:`fig-searchstrategy` visualisiert die Vorgehensweise der beiden
Strategien.


Libhugin harvest Plugins
========================

Die bisher erläuterten Ansätze und Algorithmen werden direkt durch *libhugin*
realisiert oder als Hilfsfunktionen bereitgestellt.

Des Weiteren wurden für den Prototypen Postprocessor--Plugins geschrieben,
welche weitere Probleme der Metadatenbeschaffung angehen. Ob der Benutzer ein
Plugin, beziehungsweise welche Plugins der Benutzer nutzen möchte,
bleibt ihm überlassen.

Durch die einfach gestalteten Schnittstellen (vgl :cite:`cpiechula`) ist es
möglich, *libhugin* um ein eigenes Plugin mit gewünschter
Funktionalität zu erweitern.

**Algorithmik der Postprocessor--Plugins**

Das Postprocessor--Plugin *,,Compose"* ist ein Plugin, welches es dem Benutzer
erlaubt, verschiedene Metadatenquellen zusammenzuführen. Dies ist in
der aktuellen Version auf zwei verschiedene Arten möglich.

1.) Das ,,automatische" Zusammenführen der Daten. Hierbei werden die gefundenen
Suchergebnisse nach IMDb--ID gruppiert. Dies garantiert, dass die Metadaten
nur zwischen gleichen Filmen ausgetauscht werden.

Findet der höchstpriorisierte Provider Metadaten zu einem Film, fehlt jedoch die
Inhaltsbeschreibung, so wird diese, durch den nächst niedriger priorisierten
Provider der eine Inhaltsbeschreibung besitzt, ergänzt. Abbildung :num:`fig-compose`
zeigt die Funktionalität des *Compose*--Plugins. Zuerst wird eine
Ergebnisobjekt--Kopie vom Provider mit der höchsten Priorität erstellt,
anschließend werden fehlende Attribute durch Attribute der anderen
Ergebnisobjekte ergänzt,  soweit diese vorhanden sind. Dabei erfolgt das
Auffüllen der fehlenden Attribute *iterativ*, anfangend beim Provider mit der
nächst niedrigeren Priorität. Dieser Ansatz funktioniert aktuell nur mit
Onlinequellen, die eine IMDb--ID bereitstellen. Eine Erweiterung um Provider, die
keine IMDb--ID bieten wäre möglich, indem hier zusätzliche Attribute
wie beispielsweise der Regisseur herangezogen werden, um gleiche Filme zu
gruppieren.

.. _fig-compose:

.. figure:: fig/compose.pdf
    :alt: Automatisches Ergänzen fehlender Attribute mittels Compose-Plugin mit Genre Zusammenführung.
    :width: 80%
    :align: center

    Automatisches Ergänzen fehlender Attribute mittels Compose-Plugin mit Genre Zusammenführung.

2.) Eine weitere Möglichkeit neben dem automatischen Zusammenführen von Attributen
verschiedener Provider ist die Angabe einer benutzerdefinierten Profilmaske.
Diese Profilmaske ist eine Hash--Tabelle mit den jeweiligen Attributen als
Schlüssel und den gewünschten Providern als Wert. Folgende Python Notation gibt
an, dass der Standardanbieter TMDb sein soll und die Inhaltsbeschreibung immer
vom Provider OFDb befüllt werden soll. Wenn dieser keine Inhaltsbeschreibung
besitzt, soll das Ergebnis des OMDb--Provider genommen werden.

.. code-block:: python

   profile_mask = {
        'default':['tmdbmovie'],            # Grundkopie von TMDb
        'plot': ['ofdbmovie', 'omdbmovie']  # Plot von ofdb oder omdb
   }

Nach dem Befüllen der fehlenden Attribute wird das Genre zusammengeführt.
Dies passiert indem die normalisierten Genres der verschiedenen
Provider--Ergebnisse zu einer Liste aus Genres zusammengeführt werden.

Um die Postprocessor--Plugins vollständig zu benennen, existiert noch ein
*,,Trim"*--Plugin. Dieses iteriert über alle Attribute eines Ergebnisobjektes
und entfernt dabei mittels der Python ``strip()``--Funktion die führenden und
nachstehenden Leerzeichen.

**Algorithmik der Converter--Plugins**

Auf weitere Algorithmik, welche innerhalb der Converter--Plugins realisiert ist,
wird aufgrund ihrer Einfachheit nicht weiter eingegangen. Hier werden jeweils
nur Formatierungen der Ergebnisobjekte in ein bestimmtes Ausgabeformat wie
beispielsweise XML, durchgeführt.

Libhugin analyze plugins
========================

Der *libhugin--analyze* Teil der Bibliothek ist für das nachträgliche Bearbeiten
von Metadaten gedacht. Insbesondere ist dieser Teil der Bibliothek konzipiert
worden, um automatisiert große Filmsammlungen von mehreren hundert Filmen
möglichst automatisiert mit wenig Aufwand pflegen zu können. Dabei werden die
Daten mittels einer import/export--Funktion, die vom Benutzer bereitgestellt
werden muss, in eine interne Datenbank importiert. Auf diesen Metadaten können
dann Analysen sowie Modifikationen durchgeführt werden. Anschließend werden die
modifizierten Daten mit Hilfe der vom Benutzer bereitgestellten
import/export--Funktion wieder in das Produktivsystem exportiert. Für weitere
Informationen und Anwendungsbeispiele siehe :cite:`cpiechula`.

**Algorithmik der Analyzer--Plugins**

Die Analyzer--Plugins analysieren die Metadaten und schreiben die neu gewonnenen
Informationen in eine dafür vorgesehene Liste. Die folgenden Analyzer--Plugins
wurden im Prototypen implementiert:

**Keywordextract--Plugin**: Plattformen wie TMDb bieten neben den grundlegenden
Metadaten wie Titel, Erscheinungsjahr et cetera auch Zusatzinformationen zu
Filmen an. Ein Attribut, welches beim ,,Stöbern" oder der Auswahl eines Filmes
hilfreich sein kann, sind Schlüsselwörter.

Alternativ zu Providern, die Schlüsselwörter für Filme anbieten, gibt es auch die
Möglichkeit, Schlüsselwörter aus Texten automatisiert zu extrahieren. Hierzu
gibt es verschiedene Algorithmen, jedoch werden hier zur Extraktion der
Schlüsselwörter meistens sprachabhängige Korpora (Wort--Datenbanken) benötigt
(vgl. :cite:`steinautomatische`).

Ein weiterer Algorithmus, der ohne Korpus auskommt und dabei ähnlich gute
Ergebnisse wie die korporabasierten Algorithmen liefert, ist der
RAKE--Algorithmus (Rapid Automatic Keyword Extraction), vgl.
:cite:`rose2010automatic`, :cite:`berry2010text`.

Hier wurde eine bereits existierende Implementierung in Kooperation mit dem
Kommilitonen, Christopher Pahl, reimplementiert. Herr Pahl verwendet den
Algorithmus zur Extraktion von Schlüsselwörtern aus Liedtexten, vgl.
:cite:`bacpahl`.  Der Algorithmus wurde um das automatische Laden einer
*Stoppwortliste* und einen *Stemmer* erweitert.

*Stoppwörter* sind Wörter, die sehr häufig auftreten und somit keine Relevanz
für die Erfassung des Dokumentinhalts besitzen.  Libhugin verwendet hier die
Stoppwortlisten verschiedener Sprachen von der Université de Neuchâtel [#f2]_.

*Stemming* ist ein Verfahren im Information Retrieval, bei dem die Wörter auf
ihren gemeinsamen Wortstamm zurückgeführt werden.

Im Anschluß die Funktionsweise des RAKE--Algorithmus, analog zu :cite:`bacpahl`:

1. Aufteilung des Eingabetextes in Sätze anhand von Interpunktionsregeln.
2. Extrahieren von *Phrasen* aus den jeweiligen Sätzen. Eine *Phrase* ist eine Sequenz aus nicht Stoppwörtern.
3. Berechnung eines *Scores* für jedes Wort einer *Phrase* aus dem *Degree* und
   der *Frequency* eines Wortes. :math:`P`  entspricht der Menge aller Phrasen,
   :math:`\vert p\vert` ist die Anzahl der Wörter einer Phrase.

   .. math::

      degree(word) = \sum_{p \in P} \left\{\begin{array}{cl} \vert p\vert, & \mbox{falls } word \in p\\ 0, & \mbox{sonst} \end{array}\right.

   .. math::

      frequency(word) = \sum_{p \in P} \left\{\begin{array}{cl} 1, & \mbox{falls } word \in p\\ 0, & \mbox{sonst} \end{array}\right.


4. Berechnung des *Scores* für jede Phrase. Dieser definiert sich durch die
   Summe aller Wörter--*Scores* innerhalb einer Phrase.

   .. math::

      score(word) = \frac{degree(word)}{frequency(word)}


Im Gegensatz zur Extraktion von Schlüsselwörtern aus Liedtexten werden bei der
Extraktion aus der Film--Inhaltsbeschreibung die Sätzen nur anhand von
Interpunktionsregeln getrennt, Zeilenumbrüche zählen hier nicht als Trennzeichen.

Folgende Inhaltsbeschreibung findet sich für den Film :math:`\pi` (1998) auf
TMDb:

    *Mathematikgenie Max Cohen steht kurz vor der Entschlüsselung eines numerischen
    Systems, das die Struktur von Zufall und Chaos aufdecken könnte. Mit diesem Code
    ließen sich nicht nur die Abläufe des Universums erklären, sondern auch
    Börsenbewegungen voraussagen. Bald sieht sich Max durch skrupellose
    Wall-Street-Haie verfolgt, aber auch eine religiöse Sekte und der Geheimdienst
    sind ihm auf den Fersen. Seine mentale Gesundheit leidet, er schlingert mehr und
    mehr in den Wahnsinn. Als es ihm gelingt, den 216-stelligen Code zu knacken,
    macht er eine Entdeckung, für die alle bereit sind, ihn zu töten...*

Abbildung :num:`fig-keywords` zeigt die relevanten (*Score* > 1.0)
Schlüsselwörter, die aus dem oben genannten Text, mittels RAKE--Algorithmus,
extrahiert wurden.

.. figtable::
    :label: fig-keywords
    :caption: Extrahierte Schlüsselwörter aus der Inhaltsbeschreibung des Films Pi (1998).
    :alt: Extrahierte Schlüsselwörter aus der Inhaltsbeschreibung des Films Pi (1998).

    +-----------+----------------------------------------------+
    | **Score** | **Schlüsselwörter**                          |
    +===========+==============================================+
    | 14.500    | ('mathematikgenie', 'max', 'cohen', 'steht') |
    +-----------+----------------------------------------------+
    | 9.000     | ('mentale', 'gesundheit', 'leidet')          |
    +-----------+----------------------------------------------+
    | 4.000     | ('code', 'ließen')                           |
    +-----------+----------------------------------------------+
    | 4.000     | ('börsenbewegungen', 'voraussagen')          |
    +-----------+----------------------------------------------+
    | 4.000     | ('chaos', 'aufdecken')                       |
    +-----------+----------------------------------------------+
    | 4.000     | ('numerischen', 'systems')                   |
    +-----------+----------------------------------------------+
    | 4.000     | ('haie', 'verfolgt')                         |
    +-----------+----------------------------------------------+
    | 4.000     | ('universums', 'erklären')                   |
    +-----------+----------------------------------------------+
    | 4.000     | ('stelligen', 'code')                        |
    +-----------+----------------------------------------------+
    | 4.000     | ('religiöse', 'sekte')                       |
    +-----------+----------------------------------------------+
    | 4.000     | ('skrupellose', 'wall')                      |
    +-----------+----------------------------------------------+
    | 2.500     | ('max')                                      |
    +-----------+----------------------------------------------+

Im Vergleich zu den automatisch extrahierten Schlüsselwörtern sind auf der TMDb
Plattform folgende Schlüsselwörter gepflegt:

        *hacker, mathematician, helix, headache, chaos theory, migraine, torah, börse,
        mathematics, insanity, genius*

**FiletypeAnalyze--Plugin:** Dieses Plugin dient dazu, Datei--Metadaten aus
Filmdateien zu extrahieren. Da dies, aufgrund der Vielzahl von Containern und
Codecs, ein nicht triviales Problem ist, implementiert der *libhugin--analyze*
Prototyp diese Funktionalität mit Hilfe des Tools ``hachoir-metadata``. Dieses
Tool basiert auf der ,,Hachoir"--Bibliothek welche die Extraktion verschiedener
Metadaten aus Multimedia--Dateien unterstützt. Das *FiletypeAnalyze*--Plugin
führt das ``Hachoir-metadata``--Kommandozeilen Tool aus, welches folgenden
Output liefert:

.. code-block:: bash

    hachoir-metadata --raw Sintel.2010.1080p.mkv
    Common:
    - duration: 0:14:48.032000
    - creation_date: 2011-04-25 12:57:46
    - producer: mkvmerge v4.0.0 ('The Stars were mine') built on Jun 17 2010 18:47:20
    - producer: libebml v1.0.0 + libmatroska v1.0.0
    - mime_type: video/x-matroska
    - endian: Big endian
    video[1]:
    - width: 1920
    - height: 818
    - compression: V_MPEG4/ISO/AVC
    audio[1]:
    - title: AC3 5.1 @ 640 Kbps
    - nb_channel: 6
    - sample_rate: 48000.0
    - compression: A_AC3
    subtitle[1]:
    - language: German
    - compression: S_TEXT/UTF8

Diese Ausgabe wird vom Plugin betrachtet und die relevanten Informationen wie
Auflösung, Laufzeit, et cetera extrahiert. Die Extraktion ist relativ
einfach, da die ``hachoir--metadata``--Ausgabe ein valides *Json*--Dokument ist,
welches direkt in eine Python Hash--Tabelle umgewandelt werden kann. *Json* ist
ein schlankes Dateiaustauschformat, ähnlich wie *XML*.

**LangIdentify--Plugin:** Dieses Plugin erkennt die Sprache des übergebenen Textes.
Es ist für die Analyse der Sprache der Inhaltsbeschreibung gedacht. Mittels dem
Plugin können große Filmsammlungen effizient analysiert werden und nicht
vorhandene oder in einer unerwünschten Sprache gepflegte Inhaltsbeschreibungen
in wenigen Sekunden identifiziert werden. Das Plugin verwendet die
Python--Bibliothek ``guess_language-spirit``, welche die Sprache anhand von
Sprachstatistiken erkennt. Die zusätzliche optionale Bibliothek ``pyEnchant``
kann von ``guess_language-spirit`` verwendet werden, um Texte mit weniger als 20
Zeichen zu erkennen. ``Enchant`` ist eine Bibliothek, welche auf verschiedene
Sprachbibliotheken zugreifen kann.

Die folgende *IPython*--Sitzung zeigt die Funktionalität der Bibliothek:

.. code-block:: python

    >>> from guess_language import guess_language
    >>> guess_language("Der Elfenkauz ist die einzige Art der Eulengattung der Elfenkäuze.")
    'de'

**Algorithmik der Modifier--Plugins**

Die Modifier--Plugins modifizieren die Metadaten direkt. Hier wurde ein Plugin
zum bereinigen von Inhaltsangaben entwickelt, welches mittels Regulärer
Ausdrücke (vgl. :cite:`friedl2009regulare`) unerwünschte, in Klammern stehende
Inhalte, entfernt.

Die folgende *IPython*--Sitzung zeigt den Algorithmus im Einsatz:

.. code-block:: python

    >>> import re
    >>> text  = "Die Elfenkäuzin (Micrathene Whitneyi) ist die einzige ihrer Gattung."
    >>> re.sub('\s+\(.*?\)(\s*)', '\g<1>', text)
    'Die Elfenkäuzin ist die einzige ihrer Gattung.'


Je nach Metadatenquelle finden sich hinter den jeweiligen Rollennamen, die Namen
der Schauspieler in Klammern.  Der Einsatz dieses Plugins soll eine
einheitlichere Basis für weitere Untersuchungen der Inhaltsbeschreibung zwischen
allen Metadatenquellen ermöglichen.

**Algorithmik der Comparator--Plugins**

Des Weiteren gibt es noch die experimentellen Comparator--Plugins, welche für den
Vergleich von Metadaten untereinander gedacht sind. Dieser Teil ist im
Prototypen noch nicht endgültig ausgebaut. Ziel ist es, hier über verschiedene
Data--Mining--Algorithmen neue Erkenntnisse durch den Vergleich von Metadaten
untereinander zu gewinnen, um beispielsweise Empfehlungen für ähnliche Filme
aussprechen zu können.

Aktuell gibt es ein ``KeywordCompare``--Plugin welches die Schlüsselwörter
verschiedener Filme vergleicht, um eine Ähnlichkeit zu ermitteln.
Der Ansatz, über Schlüsselwörter ähnliche Filme zu finden, hat bisher keine
nennenswerten Erkenntnisse liefern können.

Das Comparator--Plugin ``GenreCompare`` versucht anhand vom Genre, Ähnlichkeiten
zwischen Filmen zu ermitteln. Die bisherigen Ergebnisse sind je nach
verwendeter Metadatenquelle unterschiedlich gut. Je feingranularer das Genre bei
einem Anbieter gepflegt ist, umso *,,ähnlicher"* ist die Grund--Thematik. Ein
Film, der als Genre nur ,,Drama" gepflegt hat, kann zusätzlich in die Richtung
Horror, Erotik, Thriller oder eine weitere nicht spezifizierte Richtung von der
Handlung gehen.

Zusammenfassend kann gesagt werden, dass sich der Vergleich über das Genre zum
aktuellen Zeitpunkt im Prototypen nur für die Eingrenzung der Filmauswahl auf
ein bestimmtes Genre--Schema eignet.

.. rubric:: Footnotes

.. [#f1] http://de.wikipedia.org/wiki/Hauskatze
.. [#f2] http://members.unine.ch/jacques.savoy/clef/index.html
