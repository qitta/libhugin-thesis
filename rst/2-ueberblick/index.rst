###################
Libhugin Bibliothek
###################

Einleitung
==========

Die Filmmetadaten eines Films stehen in der Regel auf der DVD--Hülle oder finden
sich in der Fernseher--Programmbeschreibung. Nach dem Digitalisieren der eigenen
DVD--Sammlung oder Aufzeichnen von Sendungen fehlen diesen und müssen vom
Benutzer manuell nachträglich gepflegt werden.

Die ,,digitale Filmsammlung" wird in der Regel von sogenannter
Home--Theatre--Software abgespielt und verwaltet. Hierzu gehört beispielsweise
Software wie das XBMC--Media--Center oder Windows--Media--Center. Diese
Software kann in der Regel Metadaten für die Digitalisierten Filme beschaffen,
ist jedoch oft nur auf bestimmte Onlinequellen, die nur eine bestimmte Sprache
unterstützen, beschränkt.  Da es für das Speichern der Metadaten keinen
durchgesetzten Standard gibt verwenden die beiden genannten ,,Media--Center"
ein unterschiedliches Format zur Speicherung. Das XBMC--Media--Center verwendet
das *nfo--Format* (siehe :cite:`xbmcnfo`) und das Windows--Media--Center das
*dvdxml--Format* (siehe :cite:`dvdxml`).

Des Weiteren gibt es sogenannte Movie--Metadata--Manager--Software, welche
primär nur für das Pflegen und verwalten der digitalen Medien zuständig ist.
Zu dieser Art von Software gehört beispielsweise MediaElch. Die
Metadaten--Manager unterstützen oft mehrere Onlinequellen. Die Software erlaubt
es auch oft die gepflegten Metadaten zu exportieren um diese dann in Kombination
mit einer Home--Theatre--Abspielsoftware nutzen zu können.

Bei der Pflege von Filmsammlungen von mehreren hundert Filmen kommt es immer
wieder zu Problemen. Es gibt nicht nicht das Werkzeug der Wahl. Jedes hat seine
Vor-- und Nachteile und die Bedürfnisse der Benutzer sind hier sehr
unterschiedlich. Zu den generellen Problemen gehören folgende Punkte:

    * Filmmetadaten werden nicht gefunden.
    * Filmmetadaten sind unvollständig.
    * Filmmetadaten nur in bestimmter Sprache vorhanden.
    * Einsatz von mehreren Onlinequellen schwer oder nicht möglich.

Je nach Abspielsoftware werden nur bestimmte Onlinequellen für die Beschaffung
der Metadaten verwendend. Dies hat zufolge das beispielsweise ausländische Filme
nicht gefunden, die Inhaltsbeschreibung liegt nur in einer bestimmten Sprache
vor oder es kommt zu Redundanzen bei den Metadaten, wenn auf mehrere
Onlinequellen parallel zugegriffen wird.

Redundanzen in der Datenbank der Abspielsoftware entstehen beispielsweise beim
Genre wenn mehrere Filme von unterschiedlichen Onlinequellen bezogen werden.

    * Film **A,** Metadatenquelle **X,** Genre: Sci--Fi, Drama
    * Film **B,** Metadatenquelle **Y,** Genre: Science Fiction, Drama
    * Film **C,** Metadatenquelle **Z,** Genre: Science--Fiction, Familienfilm

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

    * Film **A**, Metadatenanbieter **X**, Genre: Sci--Fi, Drama, Komödie, Erotik
    * Film **A**, Metadatenanbieter **Y**, Genre: Drama
    * Film **A**, Metadatenanbieter **Z**, Genre: Science--Fiction


Neben den genannten Problemen kommt hinzu, dass unter *unixoden*
Betriebssystemen die Auswahl an gut funktionierenden Filmmetadaten--Manager, wie
in einem Test in der Projektarbeit festgestellt wurde (vgl. ), beschränkt.

Um die aktuell vorhanden Schwierigkeiten bei der Metadaten--Pflege zu behaben
oder abzumildern wurde das modulare pluginbasierte System *libhugin* für die
Filmmetadatenbeschaffung entwickelt. Das System zeigt im Vergleich zu den
bestehenden Lösungen eine andere Herangehensweise indem es dem Benutzer die
Möglichkeit gibt das System durch den pluginbasierten Ansatz besser an die
eigenen Bedürfnisse anzupassen. Zusätzlich wurde das System um das Konzept der
Metadatenbeschaffung erweitert. Hierdurch soll dem Benutzer die Möglichkeit
geboten werden *nachträglich* Metadaten automatisiert zu analysieren und Fehler
zu bereinigen. Hier wurde ebenso ein pluginbasierter Ansatz gewählt, welcher es
möglich macht große Filmsammlungen von mehreren hundert Filmen automatisiert zu
pflegen.

Die Bibliothek wurde in die zwei Teile *libhugin--harvest*
(Metadatenbeschaffung) und *libhugin--analyze* (Metadatenaufbereitung)
aufgeteilt. Der *libhugin-harvest* Teil der Bibliothek ist um die folgenden drei
Pluginarten erweiterbar:

    * Provider--Plugins, Zugriff auf Onlinequellen.
    * Postprocessor--Plugins, Bearbeitung der Metadaten direkt nach dem Herunterladen.
    * Converter--Plugins, Unterstützung verschiedener Metadaten--Exportformate.

Der *libhugin-analyze* Teil der Bibliothek dient zur nachträglichen
Manipulation und Analyse der Metadaten, hier gibt es die Möglichkeit folgende
Pluginarten zu implementieren:

    * Analyzer--Plugins, Analyse der Metadaten.
    * Modifier--Plugins, Direkte Modifikation der Metadaten.
    * Comparator--Plugins, Vergleich der Metadaten verschiedener Filme untereinander.

Die Bibliothek wurde in der Programmiersprache Python (Version 3.3) entworfen.
Weitere Informationen zu der genannten Problematik oder zum Software Design
finden sich in der Arbeit zum Projekt *,,Design und Implementierung eines
modularen Filmmetadaten Such-- und Analysesystems"*.
