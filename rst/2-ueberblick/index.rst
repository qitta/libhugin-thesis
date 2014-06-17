.. _motivation:

#####################################
Probleme bei der Metadatenbeschaffung
#####################################

Die Metadaten eines Films stehen in der Regel auf der DVD--Hülle oder finden
sich in der TV--Programmübersicht. Nach dem Digitalisieren der eigenen
DVD--Sammlung oder dem Aufzeichnen von Sendungen fehlen diese und müssen vom
Benutzer nachträglich manuell gepflegt werden.

Die ,,digitale Filmsammlung" wird in der Regel von sogenannter
Home--Theater--Software abgespielt und verwaltet. Hierzu gehört beispielsweise
Software wie das XBMC--Media--Center (siehe :cite:`xbmc`) oder
Windows--Media--Center (siehe :cite:`wmc`). Diese Software kann in der Regel
Metadaten für die digitalisierten Filme beschaffen, ist jedoch oft nur auf
bestimmte Onlinequellen, die nur eine bestimmte Sprache unterstützen,
beschränkt.

Da es für das Speichern der Metadaten keinen durchgesetzten Standard gibt,
verwenden die genannten ,,Media--Center" ein unterschiedliches Format zur
Speicherung der Metadaten. Das XBMC--Media--Center verwendet das *nfo*--Format
(siehe :cite:`xbmcnfo`) und das Windows--Media--Center das *dvdxml*--Format
(siehe :cite:`dvdxml`).

Des Weiteren gibt es sogenannte Movie--Metadaten--Manager--Software, welche
primär nur für das Pflegen und Verwalten der digitalen Medien gedacht ist.  Zu
dieser Art von Software gehört beispielsweise MediaElch (siehe
:cite:`mediaelch`). Die Metadaten--Manager unterstützen oft mehrere
Onlinequellen. Die Software erlaubt es häufig, die gepflegten Metadaten zu
exportieren, um diese in Kombination mit einer Home--Theater--Abspielsoftware
nutzen zu können.

Bei der Pflege von Filmsammlungen von mehreren hundert Filmen, kommt es immer
wieder zu Problemen. Es gibt hier nicht das Werkzeug der Wahl. Jede
Software hat ihre Vor-- und Nachteile und die Bedürfnisse der Benutzer sind hier
unterschiedlich.

Zu den generellen Problemen hierbei gehören folgende Punkte:

    * Filmmetadaten werden nicht gefunden.
    * Filmmetadaten sind unvollständig.
    * Filmmetadaten sind nur in bestimmter Sprache vorhanden.
    * Einsatz von mehreren Onlinequellen schwer oder nicht möglich.

Je nach Abspielsoftware werden nur bestimmte Onlinequellen für die Beschaffung
der Metadaten verwendet. Dies hat zufolge, dass beispielsweise ausländische
Filme oder weniger bekannte Filme nicht gefunden werden oder die
Inhaltsbeschreibung nur in einer bestimmten Sprache vorliegt oder die Metadaten
unvollständig sind.

Unterstützt die Abspielsoftware beziehungsweise der Metadaten--Manager mehrere
Onlinequellen, so entstehen häufig aufgrund der nicht normalisierten Metadaten
Probleme beim parallelen Bezug der Metadaten aus mehreren Quellen. Das
Hauptproblem sind Redundanzen der Metadaten in der internen Datenbank der
Abspielsoftware. Diese entstehen hauptsächlich beim Genre, wenn mehrere Filme
von unterschiedlichen Onlinequellen bezogen werden.

In Abbildung :num:`fig-genre-redundanzen` ist das Genre ,,Science Fiction" bei
den drei unterschiedlichen Onlinequellen in einer unterschiedlichen Schreibweise
vorhanden. Müssen Metadaten von unterschiedlichen Quellen bezogen werden, weil
die Daten für einen bestimmten Film unvollständig oder nicht vorhanden sind,
so wird im Beispiel das Genre ,,Science Fiction" mit drei verschiedenen
Schreibweisen in der Datenbank der Abspielsoftware hinterlegt. Dies hat zufolge,
dass eine Gruppierung oder Filterung der Filme nach diesem Attribut nicht mehr
möglich ist.

.. _fig-genre-redundanzen:

.. figure:: fig/genre-redundanzen.pdf
    :alt: Redundante Metadaten beim Bezug von Filmen aus mehreren Onlinequellen.
    :width: 90%
    :align: center

    Redundante Metadaten beim Bezug von Filmen aus mehreren Onlinequellen.


Ein weiteres Problem zeigt Abbildung :num:`fig-genre-detail`. Hier ist das
Genre--Attribut unterschiedlich detailiert gepflegt.

.. _fig-genre-detail:

.. figure:: fig/genre-detail.pdf
    :alt: Unterschiedlicher Detailgrad im Genre bei verschiedenen Onlinequellen.
    :width: 80%
    :align: center

    Unterschiedlicher Detailgrad im Genre bei verschiedenen Onlinequellen.

Neben den genannten Problemen kommt hinzu, dass unter *unixoiden*
Betriebssystemen die Auswahl an gut funktionierenden Filmmetadaten--Managern,
wie in einem Test in der Projektarbeit festgestellt wurde (siehe
:cite:`cpiechula`, 3.4.2 Probleme bei Movie–Metadaten–Managern), beschränkt ist.

Um die aktuell vorhandenen Schwierigkeiten bei der Metadatenpflege zu beheben,
beziehungsweise abzumildern wurde das modulare pluginbasierte System *libhugin*
entwickelt. Das System fungiert als Bibliothek zur Metadatenbeschaffung und
zeigt im Vergleich zu den bestehenden Lösungen eine andere Herangehensweise,
die es dem Benutzer erlaubt, das System durch den pluginbasierten Ansatz besser
an die eigenen Bedürfnisse anzupassen.

Zusätzlich wurde das System um das Konzept der Metadatenaufbereitung erweitert.
Hierdurch soll dem Benutzer die Möglichkeit geboten werden, nachträglich
Metadaten automatisiert zu analysieren und Fehler zu bereinigen. Hier wurde
ebenso ein pluginbasierter Ansatz gewählt.

Das Hauptaugenmerk von *libhugin* liegt auf der automatisierten Metadatenpflege
großer Filmsammlungen von mehreren tausend Filmen.


###################################
Übersicht der Software--Architektur
###################################

Die Bibliothek wurde in die zwei Teile *libhugin--harvest*
(Metadatenbeschaffung) und *libhugin--analyze* (Metadatenaufbereitung)
aufgeteilt. Siehe auch Architektur--Übersicht Abbildung :num:`fig-arch-overview`.

.. _fig-arch-overview:

.. figure:: fig/arch-overview.pdf
    :alt: Übersicht der Architektur von libhugin.
    :width: 80%
    :align: center

    Übersicht der Architektur von libhugin.

**Libhugin--harvest**

Der *libhugin--harvest* Teil der Bibliothek ist um die folgenden drei
Pluginarten erweiterbar:

**Provider--Plugins:** Diese Plugins sind das ,,Kernstück" des Projekts und
fungieren als ,,Vermittler" zwischen der Onlinequelle und *libhugin*. Diese Art
von Plugin muss von einer Provider--Oberklasse ableiten und die folgenden zwei
Methoden implementieren:

    * ``build_url()``--Methode (baut die URL für den Download zusammen)
    * ``parse_response()``--Methode (extrahiert die Daten aus der HTTP--Response)

Abbildung :num:`fig-provider-concept` zeigt die grundlegende Funktionsweise.
Dabei müssen alle Provider ein vorgegebenes Ergebnisobjekt mit ihren Metadaten
befüllen. Für weitere Informationen zum Ergebnisobjekt siehe *libhugin*--API
:cite:`rtfdresult`.

.. _fig-provider-concept:

.. figure:: fig/provider-concept.pdf
    :alt: Provider-Konzept für die Beschaffung von Metadaten.
    :width: 80%
    :align: center

    Provider-Konzept für die Beschaffung von Metadaten.


**Postprocessor--Plugins:** Diese Plugins sind für das Nachbearbeiten der
heruntergeladenen Metadaten zuständig. Diese Plugins müssen eine
``process()``--Methode implementieren und von der Postprocessor--Oberklasse
ableiten.


**Converter--Plugins:** Diese Plugins sind für das Exportieren der Metadaten, in
verschiedene Metadaten--Formate, zuständig. Sie müssen von der
Converter--Oberklasse ableiten und eine ``convert()``--Methode implementieren.


**Libhugin--analyze**

Der *libhugin-analyze* Teil der Bibliothek dient zur nachträglichen
Manipulation und Analyse der Metadaten. Es wird dabei nicht direkt auf den
Metadaten gearbeitet, sondern auf einer internen Kopie. Dazu müssen die Metadaten
über eine *libhugin--analyze*--Sitzung in die ,,interne Datenbank" importiert
werden. Nachdem die Metadaten analysiert und modifiziert wurden, können diese
anschließend wieder ins Produktivsystem zurückgespielt werden.

Hier gibt es die Möglichkeit folgende Pluginarten zu implementieren:

**Analyzer--Plugins**: Dienen zum Analysieren der Metadaten. Die Plugins
müssen von der Analyze--Oberklasse ableiten und eine ``analyze()``--Methode
implementieren.

**Modifier--Plugins**: Modifier--Plugins können Metadaten direkt manipulieren.
Diese Plugins müssen von der Modifier--Oberklasse ableiten und die
``modify()``--Methode implementieren.

**Comparator--Plugins**: Dieses Plugin--Interface ist experimentell. Es soll
zum Vergleich von Filmmetadaten untereinander dienen. Comparator--Plugins müssen
von der Comparator--Oberklasse ableiten und eine ``compare()``--Methode
implementieren.

Weitere Informationen zu der unter Kapitel :ref:`motivation` genannten
Problematik oder zum Software--Design selbst werden in der Arbeit zum Projekt
*,,Design und Implementierung eines modularen Filmmetadaten Such-- und
Analysesystems"*, siehe :cite:`cpiechula`, sowie in der offiziellen API
:cite:`rtfd`, behandelt.

Für die *libhugin*--Bibliothek wurden in der Projektarbeit die zwei
Kommandozeilen Tools Geri (für *libhugin--harvest*) und Freki (für
*libhugin-analyze*) entwickelt. Diese Tools demonstrieren die Funktionsweise und
Features der Bibliothek und dienen gleichzeitig als einfache Schnittstelle
für den direkten Einsatz der Bibliothek.  Des Weiteren wurde auch ein
konzeptioneller Ansatz für die Integration von *libhugin* in andere Projekte
gezeigt. Siehe :cite:`cpiechula`, insbesondere Kapitel 7 Demoanwendungen, für
weitere Informationen zu den Funktionen und Features von *libhugin*.
