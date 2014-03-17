#####################
Softwarespezifikation
#####################

Anforderungen an die Library
============================

**Die Anforderungen werden aus den Schwierigkeiten der Momentan vorhandenen
Lösungen abgeleitet.**

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
Matrix (1999)'' liefern.



