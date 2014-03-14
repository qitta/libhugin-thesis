############################################
Einführung digitale Videodaten und Metadaten
############################################

Überblick
=========

:dropcaps:`Grundsätzlich` lassen sich Video--Metadaten in zwei Kategorien
einordnen. Metadaten die das Videoformat (Auflösung, Filmlänge, ...) beschreiben
und Metadaten die den Inhalt beschreiben. Metadaten zur Beschreibung des
Videoformat können je nach Container-Format direkt in in die Datei eingebettet
werden. Letzteres sind Metadaten die bei der Digitalisierung nachträglich
gepflegt werden müssen. Hierfür werden Onlinequellen die Metadaten anbieten
verwendet. Bekannte Metadatenquellen --- neben zahlreichen weniger bekannten
Quellen --- hierfür sind z.B.:

 * Internet Movie Database (IMDb), vorwiegend englischsprachige Metadaten
 * The Movie Database (TMDb), internationale Metadaten

Die Darstellung der Filmesammlung erfolgt in den meisten Fällen über spezielle
,,Media Center''--Software die für den ,,Home-Theater Betrieb'' im Wohnzimmer
angepasst ist. Beispiele hierfür wären das Windows Media Center oder auch das
freie Xbox Media Center [#f1]_, welches in letzter Zeit noch einmal durch den
Raspberry PI [#f3]_ bekannt geworden ist. Neben den Media Center Lösungen gibt
es für die Pflege von Film Metadaten sog. Video Management Tools wie der Media
Center Master [#f2]_. Diese sind Hauptsächlich für die Pflege und Korrektur der
Metadaten gedacht. Diese Programme beziehen ihre Metadaten, wie auch die Media
Center Lösungen, über Onlinequellen. Hier variiert die Qualität und Auswahl der
Quellen, sowie die Export-Möglichkeit der Daten von Applikation zu Applikation
stark.

Zudem kommt hinzu, dass bestimmte Onlinequellen wie die Internet Movie Database
ihre Metadaten nur in englischer Sprache anbieten. Möchte man eine deutsche
Filmbeschreibung haben, so muss man auf einen Anbieter zugreifen der
Filmbeschreibungen in der dieser Sprache anbietet, je nach Anwendung wird dies
aber nicht immer unterstützt.

In den meisten Fällen werden bei den oben beispielhaft genannten Anwendungen
die richtigen Metadaten für die ,,bekannten'' Hollywood Filme bezogen. Hat man
aber eine Filmesammlung die viele *Independent Filme* oder nicht amerikanische
Verfilmungen enthält, so kommt es immer wieder zu Problemen. Die grundlegenden
Probleme hier sind, dass ein Film entweder gar nicht gefunden wird, nur ein Teil
der Metadaten gefunden wird oder diese eben nur in einer bestimmten Sprache
bezogen werden können.

.. [#f1] http://www.xbmc.org
.. [#f2] http://www.mediacentermaster.com/
.. [#f3] http://www.heise.de/hardware-hacks/artikel/Erste-Schritte-mit-dem-Raspberry-Pi-1573973.html?artikelseite=4
