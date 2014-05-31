###################
Libhugin Bibliothek
###################

Allgemeines zum System
======================

Die zu evaluierende Bibliothek *libhugin* wurde entworfen, weil es mit den
aktuellen Applikationen zur Metadaten Beschaffung und Pflege immer wieder zu
folgenden Problemen kommt:

    * Filmmetadaten werden nicht gefunden.
    * Filmmetadaten sind unvollständig.
    * Filmmetadaten nur in bestimmter Sprache vorhanden.
    * Einsatz von mehreren Onlinequellen schwer oder nicht möglich.

Je nach Abspielsoftware werden nur bestimmte Onlinequellen für die Beschaffung
der Metadaten verwendend. Dies hat zufolge das beispielsweise ausländische Filme
nicht gefunden, die Inhaltsbeschreibung liegt nur in einer bestimmten Sprache
vor oder es kommt zu Redundanzen bei den Metadaten, wenn auf mehrere
Onlinequellen parallel zugegriffen wird.

Redundanzen in der Datenbank der Abspielsoftware entstehen beispielsweise wenn
mehrere Filme von unterschiedlichen Onlinequellen bezogen werden.

    * Film A, Metadatenquelle X, Genre: Sci--Fi, Drama
    * Film B, Metadatenquelle Y, Genre: Science Fiction, Drama
    * Film C, Metadatenquelle Z, Genre: Science--Fiction, Familienfilm

Im Beispiel ist das Genre ,,Science Fiction" bei den drei unterschiedlichen
Onlinequellen in einer unterschiedlichen Schreibweise vorhanden. Müssen
Metadaten von unterschiedlichen Quellen bezogen werden weil die Daten, für einen
bestimmten, Film unvollständig oder nicht vorhanden sind, so wird im Beispiel
das Genre ,,Science Fiction" mit drei verschiedenen Schreibweisen in der
Datenbank der Abspielsoftware hinterlegt. Dies hat zufolge, dass eine
Gruppierung oder Filterung der Filme nach diesem Attribut nicht mehr möglich
ist.

Ein weiteres Problem ist, dass beispielsweise die Genreinformationen
unterschiedlich feingranular gepflegt sind:

    * Film A, Metadatenanbieter X, Genre: Sci--Fi, Drama, Komödie, Erotik
    * Film A, Metadatenanbieter Y, Genre: Drama
    * Film A, Metadatenanbieter Z, Genre: Science--Fiction


Zu den bekannten Applikationen (Abspielsoftware), sogenannte Media--Center,
gehören beispielsweise das XBMC--Media--Center oder das Windows--Media--Center.
Daneben gibt es die sogenannten Filmmetadaten--Manager, diese sind speziell für
die Pflege der Filmmetadaten gedacht. Unter *unixoden* Betriebssystemen ist die
Auswahl an gut funktionierenden Filmmetadaten--Manager

Bei der entwickelten Bibliothek wird eine andere Herangehensweise im Vergleich
zu den bereits existierenden Applikationen gezeigt. Es wurde ein modulares
System entworfen, welches sich nach dem Baukastenprinzip an die jeweiligen
Anforderungen gut anpassen lässt. Das Konzept der Metadatenbeschaffung wurde
gleichzeitig um die Funktionalität der Metadatenaufbereitung erweitert.

Die Bibliothek wurde in die zwei Teile *libhugin--harvest*
(Metadatenbeschaffung) und *libhugin--analyze* (Metadatenaufbereitung)
aufgeteilt. Der *libhugin-harvest* Teil der Bibliothek ist um die folgenden drei
Pluginarten erweiterbar:

    * Provider, Zugriff auf Onlinequellen.
    * Postprocessor, Manipulation der Metadaten direkt nach dem Herunterladen.
    * Converter, Unterstützung verschiedener Metadaten--Exportformate.

Der *libhugin-analyze* Teil der Bibliothek dient zur nachträglichen
Manipulation und Analyse der Metadaten, hier gibt es die Möglichkeit folgende
Pluginarten zu implementieren:

    * Analyzer, Analyse der Metadaten.
    * Modifier, Direkte Modifikation der Metadaten.
    * Comparator, Vergleich der Metadaten verschiedener Filme untereinander.

Die Bibliothek wurde in der Programmiersprache Python (Version 3.3) entworfen.
