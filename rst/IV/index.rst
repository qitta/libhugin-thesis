#####################
Softwarespezifikation
#####################


.. _ref-requirements:

Anforderungen an die Bibliothek
===============================

Die Anforderungen werden aus den Schwierigkeiten der momentan vorhandenen
Lösungen abgeleitet. Gute Ideen werden hier übernommen. Der konzeptionelle Entwurf
der Software ist Bestandteil der Projektarbeit, die Internas und Algorithmik
werden in der Bachelorarbeit behandelt.


Anforderungen an die Datenbeschaffung
-------------------------------------

Die Erweiterbarkeit soll durch Schreiben von Plugins erreicht werden. Folgende
Pluginarten sollen bei der Datenbeschaffung umgesetzt werden:

**Provider--Plugins**

Die Onlinequellen, die verwendet werden, sollen austauschbar sein. Der Benutzer
hat die Möglichkeit, durch Schreiben eines Plugins seine bevorzugte Onlinequelle
als sogenanntes Provider--Plugin zu implementieren. Dieses Grundprinzip wird
bereits bei der freien Musik--Metadatensuchmaschine *libglyr* (siehe
:cite:`glyr`) sowie auch im Ansatz beim XBMC (siehe :cite:`xbmcscraper`)
verwendet.

Um nicht direkt einen ,,Standardprovider" festlegen zu müssen, werden bei den
Providern Prioritäten von 0--100 vergeben. Provider mit höheren Prioritäten
werden beim Verarbeiten der Suchergebnisse bevorzugt.

**Postprocessor--Plugins**

Die Möglichkeit der *Datenaufbereitung* beim Herunterladen von Metadaten
soll erweiterbar sein. Der Benutzer hat die Möglichkeit das
Postprocessor--System durch Schreiben eines Plugins zu erweitern.

**Converter--Plugins**

Die Exportformate, die für die Speicherung der Metadaten verwendet werden,
lassen sich vom Benutzer durch Schreiben eines Plugins erweitern.

**Suche von Metadaten**

Die Suche von Metadaten soll sich für das Projekt auf Film--Metadaten und
Personen--Metadaten beschränken. Für TV--Serien--Metadaten soll jedoch auch eine
Schnittstelle geboten werden.

Die Film--Metadatensuche soll feingranular konfigurierbar sein, das heißt die
zu verwendenden Onlinequellen, die Anzahl der Ergebnisse und die *Art* der
Metadaten soll bei einer Suchanfrage einstellbar sein. Die Unterscheidung der
*Art* soll sich auf textuelle und grafische Metadaten beschränken.

Eine *onlinequellenübergreifende* Suche über die IMDb ID, welche exakte
Ergebnisse liefert, ist wünschenswert.

Beim Suchverhalten über mehrere Onlinequellen soll es zwei verschiedene
,,Suchstrategien" geben. Durch diese Suchstrategien soll dem Benutzer die
Kontrolle darüber gegeben werden, ob er möglichst genaue Ergebnisse von
unterschiedlichen Providern erhalten möchte, oder ob er verschiedene Ergebnisse
eines bevorzugten Providers wünscht.

Bevor die Suchergebnisse an den Benutzer zurückgegeben
werden, werden diese nach Provider--Priorität gruppiert. Die gruppierten
Ergebnisse je Provider werden nach Übereinstimmung mit der Suche sortiert.

Nun sollen die zwei Strategien zum Einsatz kommen, nach welcher die Ergebnisse
zurückgegeben werden. Bei der *flat*--Strategie werden aus jeder Gruppe
jeweils zuerst die höchstpriorisierten Ergebnisse ausgewählt bis das gewünschte
Ergebnislimit erreicht ist. Bei der *deep*--Strategie wird zuerst der
Provider mit der höchsten Priorität ausgeschöpft, im Anschluss der
nächstniedrigere Provider.

Mit folgendem Beispiel sollen die zwei Strategien des Suchverhaltens anschaulich
erläutert werden.

.. figtable::
    :label: table-searchstrategy
    :spec: c|l|l|l
    :caption: Abbildung zeigt Metadatenanbieter (A, B, C) und die jeweils
              gelieferten Ergebnisse  pro Anbieter
    :alt: Abbildung zeigt Metadatenanbieter (A, B, C) und die jeweils
              gelieferten Ergebnisse  pro Anbieter

    +----------------------------+---------------------+-----------------+---------------------+
    | *Onlinequelle*             | *A*                 | *B*             | *C*                 |
    +============================+=====================+=================+=====================+
    | *größte Übereinstimmung*   | Sin (2003)          | Sin (2003)      | Sin (2003)          |
    +----------------------------+---------------------+-----------------+---------------------+
    | :math:`\uparrow`           | Sin Nombre (2009)   | Sin City (2005) | Sin City (2005)     |
    +----------------------------+---------------------+-----------------+---------------------+
    | :math:`\downarrow`         | Original Sin (2001) |                 | Sin Nombre (2009)   |
    +----------------------------+---------------------+-----------------+---------------------+
    | *kleinste Übereinstimmung* |                     |                 | Original Sin (2001) |
    +----------------------------+---------------------+-----------------+---------------------+

Die Tabelle :num:`table-searchstrategy` zeigt die Suchanfrage nach dem Film
,,Sin" mit der Begrenzung auf vier Ergebnisse. Jedem Provider (A, B und C) ist
intern eine *Priorität* zugeordnet. Die Provider sind nach *Priorität* sortiert.
A hat die höchste Priorität. Die Ergebnisse pro Provider sind nach der
Übereinstimmung mit dem Suchstring ,,Sin" sortiert.

Folgende Ergebnisse werden bei jeweiliger Strategie und der Begrenzung auf vier
Ergebnisse an den Aufrufer gegeben:

    * *flat*: Sin (2003) A, Sin (2003) B, Sin (2003) C, Sin Nombre (2009) A
    * *deep*: Sin (2003) A, Sin Nombre (2009) A, Original Sin (2001) A, Sin (2003) B

**Unschärfesuche**

Der Benutzer soll auch Ergebnisse erhalten, wenn im Suchstring Tippfehler
enthalten sind. Der Suchstring ,,The Marix" soll
*metadatenanbieterübergreifend* den Film *,,The Matrix (1999)"* liefern. Eine
provider--übergreifende Suche wäre hier wünschenswert.

**IMDb ID Suche**

Die Suche nach Filmen über die *IMDb ID* soll möglich sein. Eine
provider--übergreifende Suche wäre hier wünschenswert.

**Genrenormalisierung**

Um Redundanzen zu vermeiden, soll eine Art Genrenormalisierung
implementiert werden. Hierdurch soll es möglich, sein Genre--Informationen von
mehreren Providern zusammenzuführen oder zwischen den Providern austauschbar zu
machen.


Anforderungen an die Datenanalyse
---------------------------------

Die Analyse von Metadaten soll auf bereits existierende Metadaten anwendbar
sein, mit dem Ziel die Qualität dieser zu verbessern. Hier soll es neben der
reinen Analyse die Möglichkeit der Modifikation von Metadaten geben. Ein
weiterer experimenteller Teil soll die Vergleichbarkeit von Metadaten für
statistische Zwecke ermöglichen.

Aufgrund der genannten Anforderungen sollen folgende unterschiedliche
*Pluginarten*  umgesetzt werden:

**Modifier--Plugins**

Über diese Art von Plugins lassen sich die Metadaten direkt modifizieren. Ein
Beispiel hierfür wäre das Entfernen von unerwünschten Sonderzeichen aus der
Inhaltsbeschreibung.

**Analyzer--Plugins**

Diese Art von Plugins erlaubt es dem Benutzer die vorliegenden Metadaten zu
analysieren, um neue Erkenntnisse zu gewinnen oder Defizite zu identifizieren.
Ein Beispiel hierfür wäre die Erkennung der verwendeten Sprache der
Inhaltsbeschreibung.

**Comparator--Plugins**

Diese Art von Plugins ist experimentell. Sie ist für statistische Auswertungen
bezüglich der Vergleichbarkeit von Filmen anhand der Metadaten gedacht. Mit den
entwickelten Plugins soll untersucht werden, ob und wie gut sich Filme
anhand von Metadaten vergleichen lassen, um so in Zukunft neben der bereits
erwähnten Funktionalität zusätzlich noch Empfehlungen für andere Filme
aussprechen zu können.

Allgemeine Anforderungen an die Bibliothek
------------------------------------------

**Asynchrone Bibliothek**

Die Bibliothek soll eine asynchrone Ausführung von Suchanfragen implementieren.
Das Herunterladen von Metadaten verschiedener Metadatenanbieter soll parallel
geschehen, um die Wartezeit der Suchanfrage zu reduzieren.


**Lokaler Zwischenspeicher (Cache)**

Es soll ein lokaler Cache implementiert werden, um valide Ergebnisse der
Suchanfragen zu puffern um so die Geschwindigkeit zu erhöhen und das
Netzwerk beziehungsweise die Onlinequellen zu entlasten. Manche Onlinequellen
forcieren eine Volumenbegrenzung, welche man durch den Zwischenspeicher
abmildern kann.


**Implementierung eines kommandobasierten Frontends**

Dieses soll sowohl zum Testen der Bibliothek entwickelt als auch für
Demonstrationszwecke fungieren und für *Scripting--Tasks* geeignet sein.

**Grundlegende Konfiguration des Download--Managers**

Für das Herunterladen der Metadaten sollen die folgenden Parameter
konfigurierbar sein:

    * User--Agent
    * Cache--Pfad
    * Timeout in Sekunden
    * Anzahl paralleler Download--Threads (paralleles Herunterladen)
    * Anzahl der verwendeten Job--Threads (parallele Suchanfragen)


**Konfigurationsmöglichkeiten für eine Suchanfrage**

Folgende Parameter sollen bei einer Suchanfrage konfigurierbar sein:

    * Providerart (Film, Person)
    * Filmtitel, Jahr, *IMDb ID* oder Personenname (je nach Providerart)
    * Sprache in der Metadaten gesucht werden sollen (abhängig von Onlinequelle)
    * Cache verwenden (ja/nein)
    * Anzahl der maximalen Downloadversuche
    * Anzahl der maximalen gewünschten Suchergebnisse
    * Suchstrategie (*deep/flat*)
    * Zu verwendende Metadatenanbieter
    * Unschärfesuche (ja/nein)
    * Provider übergreifende IMDb ID--Suche (ja/nein)
    * Metadatenart (textuelle Daten, grafische Daten)


Optionale Anforderungen
-----------------------

Die Bibliothek soll in ein bestehendes Open--Source--Projekt integriert werden.
Hier wäre beispielsweise die Integration als Plugin in das XBMC denkbar.


Nicht--Anforderungen
--------------------

**Nicht Film--Metadaten**

Die Suche und Analyse von Musikmetadaten oder anderen Metadatentypen ist nicht
Bestandteil des Projekts.

**Movie--Metadaten--Manager**

Die Implementierung eines *neuen* Movie--Metadaten--Managers ist nicht
Bestandteil des Projekts.
