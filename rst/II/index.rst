######################################################
Überblick Einführung digitale Videodaten und Metadaten
######################################################

Metadatenarten und Quellen
==========================

:dropcaps:`Grundsätzlich` lassen sich Video--Metadaten in zwei Kategorien
einordnen. Metadaten die das Videoformat (Auflösung, Bitrate, ...) beschreiben
und Metadaten die den Inhalt beschreiben.

Metadaten zur Beschreibung des Videoformat können je nach Container-Format
direkt in in die Datei eingebettet werden. Inhaltsbezogene Metadaten sind Daten
die bei der Digitalisierung nachträglich gepflegt werden müssen. Hierzu bedient
man sich verschiedener Onlinequellen die Metadaten anbieten. Die Bekannte
Metadatenquellen --- neben zahlreichen weniger bekannten Quellen --- hierfür
sind z.B.:

 * Internet Movie Database (IMDb), englischsprachig
 * The Movie Database (TMDb), multilingual, Community gepflegt
 * Online Filmdatenbank (OFDb), deutschsprachig, Community gepflegt


Alle drei genannten Metadatenquellen haben je nach Art, Umfang und Qualität der
Metadaten ihre ,,Stärken'' und ,,Schwächen''.

IMDb ist mehr oder weniger der ,,Platzhirsch'' unter den Metadatenquellen. Sie
ist eine Art ,,Quasistandard--Bezugsplattform". Über die bei der IMDb für jeden
Film gepflegte sog. IMDb-ID kann ein Film genau identifiziert werden. Da diese
ID eindeutig ist, wird sie oft auch von anderen Onlinedatenbanken mit erfasst
und gepflegt um auch über diese eine Suche zu ermöglichen. Leider bietet IMDb in
der "freien" Variante keine deutschsprachigen Daten an. Auch die Cover und
Fanart Daten sind hier von niedriger Qualität.

TMDb ist eine hauptsächlich Community gepflegte Datenbank. Die hier gepflegten
Filme enthalten neben den ,,Standard Metadaten'' auch hochauflösende Cover und
Hintergrundbilder (sog. Backdrops, Fanart).

OFDb ist eine im deutschen Raum bekannte Filmdatenbank, welche deutschsprachige
Metadaten pflegt.

Player und Management Software
==============================

Die Darstellung der Filmesammlung erfolgt in den meisten Fällen über sog.
,,Media Center''--Software die für den ,,Home-Theater Betrieb'' im Wohnzimmer
angepasst ist. Beispiele hierfür wären das Windows Media Center oder auch das
freie Xbox Media Center [#f1]_ (Abb. :num:`fig-xbmcscreenshot`), welches in
letzter Zeit noch einmal durch den Raspberry PI [#f3]_ Bekanntschaft erlangt
hat.

Neben den Media Center Lösungen gibt es für die Pflege von Film Metadaten
sog.  *Video--Management--Tools* wie das noch recht junge MediaElch [#f2]_ (Abb.
:num:`fig-mediaelch`).  Diese sind Hauptsächlich für die Pflege und Korrektur
der Metadaten gedacht.  Diese Programme beziehen ihre Metadaten, wie auch die
Media Center Lösungen, über Onlinequellen. Hier variiert die Qualität und
Auswahl der Quellen, sowie die Export-Möglichkeit der Daten von Applikation zu
Applikation stark.

Zudem kommt hinzu, dass bestimmte Onlinequellen wie die Internet Movie Database
ihre Metadaten nur in englischer Sprache anbieten. Möchte man eine deutsche
Inhaltsbeschreibung haben, so muss man auf einen Anbieter zugreifen der diese in
deutscher Sprache pflegt. Je nach Anwendung wird dies aber nicht immer
unterstützt.

Problematik
===========

Unbekannte/ausländische Filme
-----------------------------

In den meisten Fällen werden bei den oben beispielhaft genannten Anwendungen die
richtigen Metadaten für die ,,bekannten'' Hollywood Filme gefunden. Hat man aber
eine Filmesammlung die viele *Independent Filme* [#f4]_ oder nicht amerikanische
Verfilmungen enthält, so kommt es immer wieder zu Problemen. Die grundlegenden
Probleme hier sind, dass ein Film entweder gar nicht gefunden wird, nur ein Teil
der Metadaten gefunden wird oder diese eben nur in einer bestimmten Sprache
bezogen werden können.

Dateninhomogenität
------------------

Dieses Problem tritt in der Regal auf wenn bei einer Filmesammlung die Daten aus
unterschiedlichen Quellen stammen.

Um das Problem zu veranschaulichen, betrachten wir Auszüge von Metadaten der
drei o.g. Onlinedatenbanken. An einem Beispiel lässt sich die Problematik am
besten erklären. Wir gehen von der Annahme aus, dass wir eine deutschsprachige
Inhaltsbeschreibung möchten und die folgenden drei Filme in unserer
Filmesammlung mit Metadaten versorgen wollen:

    1) ,,After.Life (2010)'', US-amerikanischer Spielfilm, Agnieszka Wojtowicz-Vosloo
    2) ,,Nymphomaniac: Vol. I (2013)'', europäisches Drama, Lars von Trier
    3) ,,RoboCop (2014)'', US-amerikanischer Spielfilm, José Padilha

**,,After.Life (2010)''**

+-------+------------------------+----------------------------------+-------------------------+
|       | IMDb                   | TMDb                             | OFDb                    |
+=======+========================+==================================+=========================+
| Plot  | englischsprachig       | deutschsprachig                  | deutschsprachig         |
+-------+------------------------+----------------------------------+-------------------------+
| Genre | Drama, Horror, Mystery | Drama, Horror, Mystery, Thriller | Drama, Horror, Thriller |
+-------+------------------------+----------------------------------+-------------------------+

Möchte man seine Metadaten in deutscher Sprache pflegen, so fällt schon mal
kategorisch der IMDb Anbieter weg, da hier nur englischsprachige Informationen
bezogen werden. Die Daten bei TMDb werden in verschiedenen Sprachen gepflegt und
sind i.d.R. *qualitativ hochwertig*. Unser erster Film wurde bei TMDb gut
eingepflegt, die Inhaltsbeschreibung ist deutschsprachig, das Genre feingranular
gepflegt. Des weiteren bietet uns TMDb auch gleich hochauflösende Cover und
Film-Fanart. Bei OFDb ist das Genre ,,Mystery'' nicht gepflegt und zudem gibt es
nur ein niedrigauflösendes Cover und kein Fanart.

**,,Nymphomaniac: Vol. I (2013)**

+-------+------------------+------------------+--------------------+
|       | IMDb             | TMDb             | OFDb               |
+=========+==================+==================+====================+
| Plot  | englischsprachig | englischsprachig | deutschsprachig    |
+-------+------------------+------------------+--------------------+
| Genre | Drama            | Drama            | Drama, Erotik, Sex |
+-------+------------------+------------------+--------------------+

Bei unserem zweiten Film (europäischer Film) schaut es schon ganz anders aus.
Hier ist bei TMDb die Inhaltsbeschreibung in deutsch nicht vorhanden. Der Film
ist im Vergleich zu ,,Hollywood''-Blockbuster in deutsch relativ schlecht
gepflegt. Bei OFDb ist wie auch beim ersten Film, eine deutschsprachige
Inhaltsangabe vorhanden. Zur großen Überraschung ist hier das Genre im vergleich
zu den beiden anderen Metadatenanbietern feingranularer gefplegt -- was lauft
Wikipedia [#f5]_ auch besser zum Film passen würde.

**,,RoboCop (2014)''**

+-------+-----------------------+--------------------------------+------------------------------------------+
|       | IMDb                  | TMDb                           | OFDb                                     |
+=======+=======================+================================+==========================================+
| Plot  | englischsprachig      | deutschsprachig                | deutschsprachig                          |
+-------+-----------------------+--------------------------------+------------------------------------------+
| Genre | Action, Crime, Sci-Fi | Action, Science Fiction, Krimi | Action, Krimi, Science-Fiction, Thriller |
+-------+-----------------------+--------------------------------+------------------------------------------+

Der dritte Film, eine Hollywood Remake--Produktion ist hier bei allen drei
Anbietern sehr gut gepflegt.


.. _fig-xbmcscreenshot:

.. figure:: fig/xbmc-screenshot.png
    :alt: In XBMC gepflegte Filmesammlung
    :width: 70%
    :align: center

    Screenshot einer im Xbox Media Center gefpegten Filmesammlung.

.. _fig-mediaelch:

.. figure:: fig/mediaelch.png
    :alt: Übersicht MediaElch Video Management Tool.
    :width: 70%
    :align: center

    Screenshot Video Management Tool MediaElch.

.. rubric:: Footnotes

.. [#f1] http://www.xbmc.org
.. [#f2] http://www.mediacentermaster.com/
.. [#f3] http://www.heise.de/hardware-hacks/artikel/Erste-Schritte-mit-dem-Raspberry-Pi-1573973.html?artikelseite=
.. [#f4] Bezeichnung für Filme, die von Produktionsfirmen finanziert werden,
         welche nicht zu den großen US Studios gehören.
.. [#f5] Nymphomaniac (2013), http://de.wikipedia.org/wiki/Nymph()maniac
