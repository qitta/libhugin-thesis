#####################
Softwarespezifikation
#####################

Anforderungen an die Library
============================

**Die Anforderungen werden aus den Schwierigkeiten der Momentan vorhandenen
Lösungen abgeleitet.**

Anforderungen -- Suche von Metadaten
------------------------------------

**Modulares Providersystem**

Die Onlinedienste die verwendet werden, sollen austauschbar sein. Der Benutzer
hat die Möglichkeit durch schreiben eines *Plugins* seine bevorzugte Plattform
als Metadatenanbieter zu implementieren. Diese Grundprinzip wird bereits bei der
freien Musik--Metadatensuchlibrary  glyr (siehe :cite:`glyr`) verwendet.

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

Das Suchverhalten bei mehreren Metadatenanbietern soll folgende zwei
Suchstrategien bieten:

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

Anforderungen -- Analyse von Metadaten
--------------------------------------

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

Diese Art von *Plugins* ist experimentell. Sie ist für *Forschungszwecke*
bezüglich der Vergleichbarkeit von Filmen anhand der Metadaten gedacht. Mit den
hier entwickelten *Plugins* soll erforscht werden ob und wie gut sich Filme
anhand von Metadaten vergleichen lassen, um so vielleicht in Zukunft neben der
bereits erwähnten Funktionalität zusätzlich noch Empfehlungen für andere Filme
aussprechen zu können.

Allgemeine Anforderungen
-------------------------

**Anynchrone Library**

Die Bibliothek soll asynchrone Ausführung implementieren. Das herunterladen von
Metadaten verschiedener Metadatenanbieter soll ebenso parallel geschehen um die
Geschwindigkeit zu erhöhen.

**Lokaler Cache**

Es soll ein lokaler Cache implementiert werden um Suchanfragen zu puffern und so
die Geschwindigkeit zu erhöhen und Netzwerkressourcen zu schonen.


**Implementierung eines Test CLI-Client**

Es soll zum Testen der Library ein CLI-Client entwickelt werden der auch zur
Demonstration und für *Scripting--Tasks* verwenden werden kann.

**Grundlegende Konfiguration des Downloadagenten**

Für das Herunterladen sollen die folgenden Parameter konfigurierbar sein:

    * User--Agent
    * Cache--Pfad
    * Timeout in Sekunden
    * Anzahl paralleler *Downloads--Threads*
    * Anzahl der verwendeten *Job--Threads*

**Konfigurationsmöglichkeiten für eine Suchanfrage**

Hier sollen folgende Parameter sollen bei einer Suchanfrage konfigurierbar sein:

    * Filmtitel, Jahr, IMDB-ID oder Personenname (je nach Metadatenart)
    * Metadatenart
    * Sprache in der Metadaten gesucht werden sollen
    * Cache verwenden (ja/nein)
    * Anzahl der Downloadversuche
    * Anzahl der gewünschten Suchergebnisse
    * Suchstrategie (tief/flach)
    * Zu verwendete Metadatenanbieter
    * Unschärfesuche verwenden (ja/nein)
    * Provider übergreifende IMDb--ID--Suche aktivieren (ja/nein)
    * Suchtyp (textuelle Daten, Bilder)








