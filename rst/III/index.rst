#####################
Softwarespezifikation
#####################

Anforderungen an die Library
============================

**Die Anforderungen werden aus den Schwierigkeiten der Momentan vorhandenen
Lösungen abgeleitet.**

Suche von Metadaten
-------------------

**Modulares Providersystem**

Die Onlinedienste die verwendet werden, sollen austauschbar sein. Der Benutzer
hat die Möglichkeit durch schreiben eines *Plugins* seine bevorzugte Plattform
als Metadatenanbieter zu implementieren.

**Modulares Postprocessing--System**

Die Möglichkeiten der *Datenaufbereitung* sollen erweiterbar sein. Der Benutzer
hat die Möglichkeit das Postprocessing System durch schreiben eines neuen


**Modulares Output--Converter--System**

Das Format für die Speicherung der Metadaten verwendet wird, lässt sich vom
Benutzer durch schreiben eines *Plugins* erweitern.

**Suche von Metadaten**

Die Suche von Metadaten soll sich für das Projekt auf Filmmetadaten und Personen
Metadaten beschränken. Für TV-Serien soll jedoch eine Schnittstelle geboten
werden.

Die Film--Metadaten--Suche soll *feingranular* konfigurierbar sein, d.h. die
zu verwendeten Onlineanbieter, die Anzahl der Ergebnisse und die Art der
Metadaten soll bei einer Suchanfrage konfigurierbar sein.

Des weiteren soll nach Möglichkeit eine *Anbieterübergreifende* Suche über die
*IMDb-ID* ermöglicht werden, welche exakte Suchergebnisse liefert.

Das Suchverhalten soll folgende zwei Suchstrategien bieten:

    * Tiefensuche
    * Breitensuche


**Unschärfesuche**

Die Suche nach Filmen soll eine gewissen *unschärfe* erlauben. Der Benutzer soll
auch Ergebnisse erhalten wenn im Suchstring Tippfehler enthalten sind. Der
Suchstring ,,The Marix'' soll *metadatenanbieterübergreifend* den Film ,,The
Matrix (1999)'' liefern. Eine Providerübergreifende Suche wäre hier
wünschenswert.

**IMDB-ID Suche**

Die Suche nach Filmen über die IMDB-ID soll möglich sein. Eine
Providerübergreifende Suche wäre hier wünschenswert.

Analyse von Metadaten
---------------------

*Die Analyse von Metadaten soll auf bereits existierende Metadaten anwendbar
sein, mit dem Ziel die Qualität dieser zu verbessern.*

Die Analyse von Metadaten soll mit folgenden **Pluginarten** umgesetzt werden:

**Modifier Plugins**

Über diese Art von Plugins lassen sich die Metadaten direkt modifizieren. Ein
Beispiel hier wäre z.B. das entfernen von unerwünschten Sonderzeichen aus der
Inhaltsbeschreibung.

**Analyzer Plugins**

Diese Art von Plugins erlaubt es dem Benutzer die vorliegenden Metadaten zu
analysieren um neue Erkenntnisse zu gewinnen oder Defizite zu identifizieren.


**Comperator Plugins**

Diese Art von Plugins ist experimentell. Sie ist für *Forschungszwecke*
bezüglich der Vergleichbarkeit von Filmen anhand der Metadaten gedacht.
