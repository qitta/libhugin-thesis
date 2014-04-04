#####################
Softwarespezifikation
#####################


.. _ref-requirements:

Anforderungen an die Library
============================

Die Anforderungen werden aus den Schwierigkeiten der Momentan vorhandenen
Lösungen abgeleitet, gute Ideen werden hier übernommen. Grundsätzlich ist die
Idee aber eine andere Herangehensweise an die Problematik zu erarbeiten.

Anforderungen an die Datenbeschaffung
-------------------------------------

Die Datenbeschaffung soll modular aufgebaut sein. Die Erweiterbarkeit soll durch
schreiben von Plugins erreicht werden. Folgende Pluginarten sollen bei der
Datenbeschaffung umgesetzt werden:

**Provider Plugins**

Die Onlinequellen die verwendet werden, sollen austauschbar sein. Der Benutzer
hat die Möglichkeit durch schreiben eines Plugins seine bevorzugte
Onlinequelle als Metadatenanbieter zu implementieren. Diese Grundprinzip wird
bereits bei der freien Musik--Metadatensuchlibrary  glyr (siehe :cite:`glyr`)
sowie auch im Ansatz beim XBMC (siehe :cite:`xbmcscraper`) verwendet.

Um nicht direkt einen ,,Standardprovider" festlegen zu müssen werden bei den
Providern Prioritäten von 0-100 vergeben. Provider mit höheren Prioritäten
werden werden beim verarbeiten der Suchergebnisse bevorzugt.


**Postprocessor Plugins**

Die Möglichkeiten der *Datenaufbereitung* beim Herunterladen von Metadaten
sollen erweiterbar sein. Der Benutzer hat die Möglichkeit das Postprocessor
System durch schreiben eines von Plugins zu erweitern.

**Output--Converter Plugins**

Das Format für die Speicherung der Metadaten verwendet wird, lässt sich vom
Benutzer durch schreiben eines Plugins erweitern.

**Suche von Metadaten**

Die Suche von Metadaten soll sich für das Projekt auf Film--Metadaten und
Personen--Metadaten beschränken. Für TV-Serien--Metadaten soll jedoch auch eine
Schnittstelle geboten werden.

Die Film--Metadatensuche soll *feingranular* konfigurierbar sein, d.h. die
zu verwendeten Onlinequellen, die Anzahl der Ergebnisse und die Art der
Metadaten soll bei einer Suchanfrage konfigurierbar sein. Die Unterscheidung der
Art soll sich auf textuelle und grafische Metadaten beschränken.

Eine *onlinequellenübergreifende* Suche über die IMDB--ID, welche exakte
Ergebnisse liefert, ist wünschenswert.


Beim Suchverhalten über mehreren Onlinequellen soll es zwei verschiedene
,,Suchstrategien" geben. Bevor die Suchergebnisse an den Benutzer zurückgegeben
werden, werden diese nach Provider Priorität gruppiert. Die Gruppierten
Ergebnisse je Provider werden nach Übereinstimmung mit der Suche sortiert.

Nun sollen die zwei Strategien zum Einsatz kommen, nach welcher die Ergebnisse
zurück gegeben werden. Die ,,flat'' Strategie, hierbei wird aus jeder Gruppe
jeweils zuerst die höchstpriorisierten Ergebnisse ausgewählt, bis das gewünschte
Ergebnislimit erreicht ist. Die ,,deep'' Strategie, hierbei  wird zuerst der
Provider mit der höchsten Priorität ausgeschöpft, im Anschluss der
nächstniedrigere.

Mit folgendem Beispiel sollen die zwei Strategien des Suchverhaltens anschaulich
erläutert werden:

.. figtable::
    :label: table-searchstrategy
    :caption: Abbildung zeigt Metadatenanbieter (A, B, C) und die jeweils
              gelieferten Ergebnisse  pro Anbieter
    :alt: Abbildung zeigt Metadatenanbieter (A, B, C) und die jeweils
              gelieferten Ergebnisse  pro Anbieter

    +-------------------+---------------------+-----------------+-------------------+
    | Metadatenanbieter | A                   | B               | C                 |
    +===================+=====================+=================+===================+
    |                   | Sin (2003)          | Sin (2003)      | Sin (2003)        |
    +-------------------+---------------------+-----------------+-------------------+
    |                   | Sin Nombre (2009)   | Sin City (2005) | Sin City (2005)   |
    +-------------------+---------------------+-----------------+-------------------+
    |                   | Original Sin (2001) |                 | Sin Nombre (2009) |
    +-------------------+---------------------+-----------------+-------------------+

Die Tabelle :num:`table-searchstrategy` zeigt die Suchanfrage nach dem Film
,,Sin'' mit der Begrenzung auf vier Ergebnisse. Jeder Provider (A, B und C) hat
eine *Priorität* gepflegt. Die Anbieter sind nach *Priorität* sortiert. A hat
die höchste Priorität. Die Ergebnisse pro Anbieter sind nach der Übereinstimmung
zum Suchstring sortiert.

Folgende Ergebnisse werden bei jeweiliger Strategie und der Begrenzung auf vier
Ergebnisse an den Aufrufer gegeben:

    * *flat*: Sin (2003) A, Sin (2003) B, Sin (2003) C, Sin Nombre (2009) A
    * *deep*: Sin (2003) A, Sin Nombre (2009) A, Original Sin (2001) A, Sin (2003) B

**Unschärfesuche**

Der Benutzer soll auch Ergebnisse erhalten wenn im Suchstring Tippfehler
enthalten sind. Der Suchstring ,,The Marix'' soll
*metadatenanbieterübergreifend* den Film ,,The Matrix (1999)'' liefern. Eine
Providerübergreifende Suche wäre hier wünschenswert.

**IMDB-ID Suche**

Die Suche nach Filmen über die IMDB-ID soll möglich sein. Eine
Providerübergreifende Suche wäre hier wünschenswert.

**Genre ,,Normalisierung''**

Um Redundanzen zu vermeiden soll eine Art ,,Genre--Normalisierung''
implementiert werden. Hierdurch soll es möglich sein Genre--Informationen von
mehreren Providern zusammenzuführen oder zwischen den Providern austauschbar zu
machen.


Anforderungen an die Datenanalyse
---------------------------------

Die Analyse von Metadaten soll auf bereits existierende Metadaten anwendbar
ein, mit dem Ziel die Qualität dieser zu verbessern. Hier soll neben der
reinen Analyse die Möglichkeit der Modifikation von Metadaten geben. Ein
weiterer experimentieller Teil soll auch die Vergleichbarkeit von Metadaten für
statistische Zwecke ermöglichen.

Aufgrund der genannten Anforderungen sollen folgende unterschiedliche
*Pluginarten*  umgesetzt werden:

**Modifier Plugins**

Über diese Art von Plugins lassen sich die Metadaten direkt modifizieren. Ein
Beispiel hier wäre das entfernen von unerwünschten Sonderzeichen aus der
Inhaltsbeschreibung.

**Analyzer Plugins**

Diese Art von Plugins erlaubt es dem Benutzer die vorliegenden Metadaten zu
analysieren um neue Erkenntnisse zu gewinnen oder Defizite zu identifizieren.
Ein Beispiel hier wäre die Erkennung der verwendeten Sprache der
Inhaltsbeschreibung.

**Comperator Plugins**

Diese Art von Plugin ist experimentell. Sie ist für statistische Auswertungen
bezüglich der Vergleichbarkeit von Filmen anhand der Metadaten gedacht. Mit den
hier entwickelten Plugins soll erforscht werden ob und wie gut sich Filme
anhand von Metadaten vergleichen lassen, um so in Zukunft neben der bereits
erwähnten Funktionalität zusätzlich noch Empfehlungen für andere Filme
aussprechen zu können.


Allgemeine Anforderungen
-------------------------

**Asynchrone Library**

Die Bibliothek soll eine asynchrone Ausführung von Suchanfragen implementieren.
Das herunterladen von Metadaten verschiedener Metadatenanbieter soll parallel
geschehen. Durch paralleles Herunterladen soll die Wartezeit der Suchanfrage
reduziert werden.

**Lokaler Cache**

Es soll ein lokaler Cache implementiert werden um valide Ergebnisse der
Suchanfragen zu puffern um so die Geschwindigkeit zu erhöhen und das
Netzwerk beziehungsweise die Onlinequellen zu entlasten.


**Implementierung eines Test CLI-Client**

Es soll zum Testen der Bibliothek ein Konsolen-Client entwickelt werden der auch
zur Demonstration und für *Scripting--Tasks* verwenden werden kann.

**Grundlegende Konfiguration des Downloadagenten**

Für das Herunterladen der Metadaten sollen die folgenden Parameter
konfigurierbar sein:

    * User--Agent
    * Cache--Pfad
    * Timeout in Sekunden
    * Anzahl paralleler Downloads--Threads
    * Anzahl der verwendeten Job--Threads

**Konfigurationsmöglichkeiten für eine Suchanfrage**

Folgende Parameter sollen bei einer Suchanfrage konfigurierbar sein:

    * Filmtitel, Jahr, IMDB-ID oder Personenname (je nach Metadatenart)
    * Metadatenart (Film, Person)
    * Sprache in der Metadaten gesucht werden sollen (providerabhängig)
    * Cache verwenden (ja/nein)
    * Anzahl der Downloadversuche
    * Anzahl der gewünschten Suchergebnisse
    * Suchstrategie (deep/flat)
    * Zu verwendete Metadatenanbieter
    * Unschärfesuche verwenden (ja/nein)
    * Provider übergreifende IMDb--ID--Suche aktivieren (ja/nein)
    * Suchtyp (textuelle Daten, grafische Daten)


Optionale Anforderungen
-----------------------

Die Bibliothek soll in ein bestehendes Open Source Projekt intigriert werden.
Hier wäre beispielsweise die Integration als Plugin in das Xbox Media Center
denkbar.

Demonstration weiterer *Einsatzmöglichkeiten*.

Nicht--Anforderungen
--------------------

**Andere Metadaten**

Die Suche und Analyse von Musikmetadaten oder anderen Metadatentypen ist nicht
Bestandteil des Projekts.

**Movie Metadaten Manager**

Die Implementierung eines *neuen* Movie Metadaten Managers ist nicht Bestandteil
des Projekts. Das Projekt will gerade diesen Ansatz vermeiden und eine *andere*
Herangehensweise aufzeigen.
