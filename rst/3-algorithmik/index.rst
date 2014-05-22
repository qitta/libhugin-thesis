###########
Algorithmik
###########


Filmsuche Algorithmik
=====================

Bei der Suchanfrage über den Filmtitel wird von den Onlinequellen in der Regel
eine Liste mit mehreren Möglichkeiten geliefert. Das Provider--Plugin muss
anschließend die Filmtitel mit der größten Übereinstimmung herausfinden. Für die
Ähnlichkeit bei der Suche nach übereinstimmenden Zeichenketten, wurde ein
Ähnlichkeitsmaß definiert welches von 0.0 (keine Ähnlichkeit) bis 1.0
(Übereinstimmung) geht.

Der Vergleich der Zeichenketten sollte möglichst fehlertolerant sein und
Zeichenketten mit der höhten Übereinstimmung liefern.

Der simple Vergleich

::

    "The Matrix" ==  "The Matrix"

würde hier nur bei exakt den gleichen Zeichenketten funktionieren. Für den
Vergleich von Zeichenketten bietet die Python Standard--Bibliothek das
*difflib*--Modul. Das Modul erlaubt es zwei Sequenzen zu vergleichen. Es
arbeitet mit dem Ratcliff--Obershelp--Algorithmus und hat eine Komplexität von
:math:`O(n^{3})` im *worst case* und eine erwartete Komplexität von
:math:`O(n^{2})`. Der Algorithmus basiert auf der Idee, die Sequenzen der
übereinstimmenden Zeichen zu und durch die Anzahl alle Zeichen der beiden
Strings zu teilen.

Ein weiterer Algorithmus der für Zeichenkettenvergleiche eingesetzt wird ist der
Levenshtein--Algorithmus (Levenshtein--Distanz). Der Algorithmus hat eine
Laufzeit von :math:`O(nm)`. Die Levenshtein--Distanz basiert auf der Idee, der
minimalen Editiervorgänge (Einfügen, Löschen, Ersetzen) um von einer
Zeichenkette auf eine andere zu kommen (vgl :cite:`atallah2010algorithms`). Die
normalisierte Levenshtein--Distanz bewegt sich zwischen 0.0 (Übereinstimmung)
und 1.0 (keine Ähnlichkeit).

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


Da es bei der Filmsuche zu vielen Zeichenkettenvergleichen kommt, und auch nicht
abgesehen werden kann um beispielsweise welche Data--Mining--Plugins *libhugin*
in Zukunft erweitert wird, sollte der Algorithmus, zum Vergleich von
Zeichenketten, eine gute Laufzeit bieten.

Da der Raspberry Pi als Zielplattform nicht ausgeschlossen ist, sollte die
Implementierung des Algorithmus zum Vergleich von Zeichenketten möglichst
performant sein.

Um die jeweiligen Algorithmen, beziehungsweise die Implementierungen dieser,
bezüglich der Performance, zu überprüfen wurde eine Messung mit den folgenden
unter Python verfügbaren Implementierungen durchgeführt:

    * difflib, Modul aus der Python--Standard--Bibliothek  (Ratcliff-Obershelp)
    * pyxDamerauLevenshtein, auf Cython basierte der Damerau--Levenshtein--Implementierung
    * distance, externes Modul mit Levenshtein--Implementierung in Python und C

.. _fig-stringcompare:

.. figure:: fig/algo_compare.pdf
    :alt: String comparsion algorithms.
    :width: 100%
    :align: center

    String comparsion algorithms performance anlysis.

Je nach Algorithmus variiert das Ergebnis leicht, das liegt daran dass die
Algorithmen eine unterschiedliche Idee verfolgen.

Folgende interaktive Python--Sitzung zeigt das Ergebnisverhalten von difflib und
pyxDamerauLevenshtein, da das Ähnlichkeitsmaß beim der zu letzt genannten
Implementierung umgekehrt ist, wird das Ergebnis von der eins abgezogen um das
Verhalten zu vergleichen:

.. code-block:: python

    >>> difflib.SequenceMatcher(None, "Katze", "Fratze").ratio()
    0.7272727272727273
    >>> 1 - normalized_damerau_levenshtein_distance("Katze", "Fratze")
    0.6666666666666667

Weitere Werte für die um die unterschiedliche Wertung der beiden Algorithmen zu
zeigen finden sich in der Tabelle (siehe Abbildung).

Da der Vergleich case sensitive ist fällt die Ähnlichkeit der Titel *,,Sin"*
und *,,sin"*, wie folgende Python Sitzung zeigt, unterschiedlich aus:

.. code-block:: python

    >>> 1 - normalized_damerau_levenshtein_distance("sin", "Sin")
    0.6666666666666667

Um dieses Problem zu beheben wird die gesuchte Zeichenkette vor dem Vergleich
normalisiert. Dies geschieht indem alle Zeichen der Zeichenkette in Klein--
beziehungsweise alternative in Großbuchstaben umgewandelt werden. Folgendes
Beispiel zeigt die Normalisierung mittels der in Python integrierten
``lower()``--Funktion:

.. code-block:: python

    >>> 1 - normalized_damerau_levenshtein_distance("sin".lower(), "Sin".lower())
    1.0

Während der Entwicklung ist aufgefallen, dass der implementierte OFDb--Provider
den Film *,,The East (2013)"* nicht finden konnte. Nach längerer Recherche und
Ausweitung der gewünschten Ergebnisanzahl auf 100, wurde festgestellt, dass der
Film auf dem letzten Platz der Suchergebnisse (Platz 48) zu finden war.

Dies liegt daran liegt, dass der Film auf dieser Online--Plattform mit der
Schreibweise *,,East, The"* gepflegt ist. Dies ist eine valide und nicht
unübliche Schreibweise um Filme alphabetisch schneller zu finden.

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

Um dieses Problem zu Umgehen, müssen die Filmtitel auf ein bestimmtes Schema
normalisiert werden. Um dieses Problem zu beheben wäre ein möglicher Ansatz den
Artikel zu entfernen. Dies würde jedoch das Problem mit sich bringen, dass Filme
wie *,,Drive (2011)"* und *"The Drive (1996)"* fälschlicherweise als identisch
erkannt werden würden. Ein weiteres Problem, welches hinzu kommt ist, dass der
Artikel--Ansatz sprachabhängig ist.

Ein anderer Ansatz ist, Satztrennungszeichen zu entfernen und die einzelnen
Wörter des Titels alphabetisch zu sortieren.

Aus *,,East, The"* und *,,The East"* wird nach der Normalisierung also *,,east
the"*. Der Vergleich der Zeichenkette würde eine Ähnlichkeit von 1.0 liefern.

Anhand des Beispieltitel *,,East, The"* wird wie folgt die Normalisierung
erläutert:

    1. Titel auf Kleinschreibung runter brechen →  ``'east, the'``
    2. Satztrennungszeichen wie ,,,", ,,-" und ,,:" werden entfernt → ``'east the'``
    3. Titel anhand der Leerzeichen aufbrechen und in Liste umwandeln → [``'east'``, ``'the'``]
    4. Liste alphabetisch sortieren und in Zeichenkette umwandeln → ``'east the'``

Wendet man diesen Ansatz auf ,,The East" und ,,East, The" an so erhält man in
beiden Fällen die Zeichenkette "east the". Die Umsetzung des Algorithmus bei der
Titelsuche löst das Problem beim OFDb--Provider. Der eben genannte Film wird
durch die Normalisierung gefunden und erscheint an der ersten Position.

Diese Vorgehensweise Normalisiert ebenso die Personensuche. Hier wird
beispielsweise der Name *,,Emma Stone"* und *,,Stone, Emma"* in beiden Fällen zu
der Zeichenkette ``'emma stone'``.

Die Anpassungen beim Zeichenkettenvergleich wirken sich auf die Performance aus.
Abbildung :num:`fig-finalstringcompare` zeigt den Performanceunterschied zum
ursprünglichen Algorithmus.

.. _fig-finalstringcompare:

.. figure:: fig/adjusted_algo_compare.pdf
    :alt: String comparsion algorithms.
    :width: 100%
    :align: center

    Angepasster Damerau-Levenshtein Algorithmus

.. raw:: Latex

   \newpage

IMDb--ID Suche
==============

Ob die Suche nach der IMDb--ID möglich ist hängt von der jeweiligen Onlinequelle
ab. Onlinequellen wie TMDb, OFDb oder auch OMDb unterstützen direkt die Suche
über die IMDB--ID. Andere Onlinequellen wie das filmstarts-- oder
Videobuster--Portal unterstützen keine Suche über IMDb--ID. Es ist prinzipiell
nur eine Suche über IMDb--ID möglich wenn diese von der jeweiligen Onlinequelle
direkt angeboten wird.

Um dieses Problem abzumildern und eine onlinequellenübergreifende Möglichkeit
über die IMDb--ID zu ermöglichen bietet die *libhugin--harvest*--Bibliothek die
Möglichkeit den sogenannten ,,Lookup--Mode" zu aktivieren.

Hierbei wird intern vor der Metadatensuche ein sogenannter *Lookup* durchgeführt
um zu der gesuchten IMDB--ID den passenden Filmtitel zu ermitteln. Prinzipiell
gibt es hier die Möglichkeit über eine Suche auf *IMDb.com* den Entsprechenden
Titel zu ermitteln. Die Filme auf der Seite sind jeweils unter der jeweiligen
IMDb--ID eingepflegt. Eine URL für den Film mit der IMDb--ID ``tt1602613`` für
den Film *,,Only god forgives (2013)"* ist wie folgt aufgebaut:

    * http://www.imdb.com/title/tt1602613

Wenn also der *Lookup--Mode* aktiviert wird, wird vor dem eigentlichen
Herunterladen über die Provider ein *Loockup* über ``http://imdb.com``
getriggert. Hierbei wird die URL aus der zu suchenden ID zusammengesetzt und
ein IMDb Anfrage darüber gestartet. Anschließend wird auf den zurückgelieferten
Inhalt ein Regulärer Ausdruck ausgeführt, welcher die Zeichenketten bestehend
aus "<Titelname> <(4-stellige Jahreszahl)>", extrahiert.

Der algorithmische Ansatz schaut unter Python wie folgt aus:

.. code-block:: python

   >>> imdbid = "tt1602613"  # id for only god forgives
   >>> request = requests.get('http://www.imdb.com/title/{}'.format(imdbid))
   >>> title, year = re.search('\>(.+?)\s*\((\d{4})', request.text).groups()
   >>> print(title, year)
   'Only God Forgives 2013'


Unschärfesuche
==============

Die Onlinequellen der implementierten Provider, TMDb, IMDb, OFDb, OMDb,
Filmstarts und Videobuster benötigen exakte Suchanfragen. Bei einem Tippfehler
wie *,,Only good forgives"* (Originaltitel: Only god forgives), wird der Film
von den genannten Online--Plattformen nicht gefunden. Diesen Fehler clientseitig
zu beheben ist schwierig, man müsste eine große Datenbank an Filmtitel pflegen
und aktuell halten, und könnte so mit Hilfe dieser den Fehler vom Benutzer
korrigieren indem alternativ die ähnlichste Zeichenkette aus der Datenbank
nehmen würde. Mit der normalisierten Damerau--Levenshtein Ähnlichkeit die
*libhugin* zum Zeichenkettenvergleich anbietet hätte die falsche Anfrage eine
Ähnlichkeit von 0.94.

Eine lokale beziehungsweise zentrale Datenbank aufzubauen wäre möglich, da die
Informationen beziehungsweise Metadaten Online auf vielen Plattformen verfügbar
sind. Diese Datenbank aktuell zu halten ist jedoch schwierig, da nicht bekannt
ist auf welchen Plattformen ein Film überhaupt gepflegt ist beziehungsweise wie
aktuell die gepflegten Informationen sind.

Um dieses Problem trotz der genannten Schwierigkeiten zu lösen bedient sich
*libhugin* eines anderen Ansatzes. *Libhugin* delegiert die Information, wie es
ein Mensch auch machen würde, an eine Suchmaschine. In konkreten Fall wird ein
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
Parametern *Filmtitel*, *Erscheinungsjahr*, *imdb* und *movie*. Anschließend
wird die zurückgegebene URL betrachtet, und aus dieser die IMDb--ID extrahiert.

Folgende *IPython*--Sitzung zeigt den Ansatz:

.. code-block:: python


    >>> fmt = 'http://www.google.com/search?hl=de&q={title}+{year}+imdb+movie&btnI=1'
    >>> url = requests.get(fmt.format(title='Drive', year='2011'))).url
    >>> imdbid = re.findall('\/tt\d*/', url)
    >>> imdbid.pop().strip('/')
    'tt0780504'

Hier wurde der Ansatz gewählt die IMDb--ID aus der URL mit einem Regulärem
Ausdruck zu parsen. Dies erspart das parsen des kompletten Dokuments.
Anschließen wird die Suche mit der IMDb--ID normal fortgesetzt. Alternativ wäre
hier der Ansatz über dem Filmtitel, wie beim IMDb--ID zu Titel *Lookup* möglich.


Asynchrone Ausführung
=====================

Bestimmte Teile von *libhugin* wurden multithreaded entwickelt. Hierzu zählen
die Downloadqueue so wie die Möglichkeit die Suchanfrage asynchron
loszuschicken.

Auf den exzessiven Einsatz von Multithreading wurde verzichtet, da
parallele Verarbeitung unter Python aufgrund vom *GIL* (Global Inetpreter Lock)
nur eingeschränkt möglich ist. Der *GIL* ist ein Mutex, welcher verhindert dass
mehrere native Threads Python Bytecode gleichzeitig ausführen können. Die
Parallelisierung beispielsweise von Funktionen kann sogar zu Performanceeinbußen
im Vergleich zur Singlethreaded Ausführung führen.

Diese Einschränkung gilt jedoch nicht für lange laufende oder blockierende
Operationen wie beispielsweise der Zugriff auf die Festplatte (vgl
:cite:`hellmann2011python`).

Da der Zugriff auf Onlinequellen je nach Serverauslastung und Internetanbindung
in der Performance stark variiert, wurde das Herunterladen der Metadaten
parallelisiert. Das parallele Herunterladen zeigt deutliche
Geschwindigkeitsvorteile im Vergleich zur seriellen Verarbeitung (siehe
Abbildung :num:`fig-threaded-download`).




Normalisierung der Metadaten
============================

Die Normalisierung der Metadaten aus unterschiedlichen Quellen ist sehr
schwierig, da es bei den Filmmetadaten keinen einheitlichen Standard gibt. Um
fehlerhafte oder fehlende Metadaten über unterschiedliche Quellen zu ergänzen,
müssen die Metadaten normalisiert werden. Dieses Problem wird nun Anhand vom
Genre Attribut, welches in der internen Metadaten--Datenbank des XBMC abgelegt
wurde, beispielhaft erklärt.

Wird beispielsweise der Spielfilm ,,The Matrix (1999)" über drei verschiedene
Onlinequellen bezogen, so erhält man, falls das Genre ,,Science Fiction" bei den
jeweiligen Quellen gepflegt wurde, oft eine unterschiedliche Schreibweise.

    * TMDb (www.themoviedb.org): Science Fiction
    * IMDb (www.imdb.com): Sci--Fi
    * OFDb (www.ofdb.de): Science--Fiction

Wird nun der Film ,,The Matrix (1999)" über TMDb bezogen und der Film ,,Matrix
Revolutions (2003)" über IMDb, weil er beispielsweise bei TMDb nicht gepflegt
ist, so wird in diesem Fall das Genre mit den zwei unterschiedlichen
Schreibweisen ,,Science Fiction" und ,,Sci--Fi" bezogen.

Durch diesen Umstand haben wir eine Genreinformation redundant in unserem
XBMC--Center gepflegt. Es ist also nicht mehr möglich dieses Filmgenre eindeutig
zu identifizieren. Es ist somit weder eine Gruppierung nach diesem Genre noch
eindeutige eindeutige Filterung möglich.

Dieses Problem betrifft grundsätzlich alle Filmmetadaten Attribute, jedoch
lassen sich andere Attribute wie die Inhaltsbeschreibung problemlos austauschen,
diese von Natur aus individuell und sich somit nicht normalisieren lässt.

Da das Filmgenre, neben der Inhaltsbeschreibung, zu den wichtigsten
Auswahlkriterien bei Filmen zählt, wurde hier bei *libhugin* ein statisches
Konzept der Normalisierung umgesetzt.

Die Normalisierung bei *libhugin* bildet hierzu jedes Genre einer Onlinequelle
auf einem Globalen Genre ab. Die Normalisierung erfolgt über eine statische
Genre--Tabelle, welche der Autor eines Provider--Plugins (Plugin um eine
bestimmte Onlinequellen anzusprechen) bereitstellen muss. Der Nachteil dieser
Variante ist, dass das Genre--Spektrum der Onlinequelle bekannt sein muss.

Das Provider Genre wird über einen Index auf einem globalen Genre abgebildet.
Folgendes Beispiel zeigt ausschnittsweise den Abbildungsansatz:

::

    Globale Genre Tabelle           Provider Tabelle mit Mapping
    =====================           ============================

    1, Science Fiction              21, Sex
    2, Komödie                      22, 3D-Animation
    3, Actionfilm                   2, Comedy
    [...]                           20, Drama
    20, Drama                       1, Sci-Fi
    21, Erotik
    22, Animation

Die Abbildung erfolgt anhand des Indizes:

::

    3D-Animation    --- wird zu --->    Animation
    Comedy          --- wird zu --->    Komödie
    Drama           --- wird zu --->    Drama
    Sci-Fi          --- wird zu --->    Science Fiction
    Sex             --- wird zu --->    Erotik

Wird keine ,,Genremapping--Tabelle" bereitgestellt, so kann das Genre nicht
normalisiert werden. In diesem Fall kann es zu der oben genannten Problematik
kommen. Das Genremapping muss pro Sprache gepflegt werden, der Prototyp besitzt
im aktuellen Zustand eine globale Genre--Tabelle für die deutsche und die
englische Sprache.

Ein weiterer Ansatz bei der Genrenormalisierung war die automatische Erkennung
des Genres Anhand der Wortähnlichkeit. Dies erwies sich jedoch als nicht
praxistauglich. Eine automatische Genreerkennung benötigt eine Wortschatz aus
Referenz--Genres, mit welchen das ,,unbekannte" Provider--Genre verglichen werden
muss. Bei Genres wie Science Fiction, Drama oder Thriller funktioniert das
System noch relativ gut, komme aber seltene oder unbekannte Genrenamen wie
,,Mondo" oder ,,Suspense" hinzu, kann je nach Referenz--Wortschatz keine
Übereinstimmung mehr erfolgen. Hier wäre noch eine semiautomatischer Ansatz
denkbar, welcher automatisiert Genres erkennt und im Fall eines Unbekannten
Genres dieses in eine Liste aus nicht zugeordneten Genres hinzufügt, welche dann
vom Benutzer ,,korrigiert" werden kann. Dies ist jedoch bei einer
Software--Bibliothek wie sie durch *libhugin* bereitgestellt wird, weniger
praktikabel.

** semi auto difflib example**

Ein weiteres Problem das hier jedoch hinzu kommt ist, dass das ,,Genre" an sich
in keiner Form standardisiert ist. Je nach Onlinequelle gibt es
Genrebezeichnungen wie Animationsfilm oder Kinderfilm, welche jedoch im engeren
Sinne aber nicht zum ,,Filmgenre"--Begriff gezählt werden dürften. Des Weiteren
kommt hinzu, dass über die Jahre immer wieder neue Genre entstanden sind.

.. rubric:: Footnotes

.. [#f1] http://de.wikipedia.org/wiki/Hauskatze
