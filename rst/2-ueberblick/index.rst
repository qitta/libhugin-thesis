###################
Libhugin Bibliothek
###################

Allgemeines zum System
======================

Die zu evaluierende Bibliothek *libhugin* wurde entworfen, weil es mit den
aktuellen Applikationen zur Metadaten Beschaffung und Pflege immer wieder zu
Probleme kommt. Oft werden beispielsweise ausländische Filme nicht gefunden, die
Inhaltsbeschreibung liegt nur in einer bestimmten Sprache vor oder es kommt zu
Redundanzen bei den Metadaten, wenn auf mehrere Onlinequellen parallel
zugegriffen wird (vgl. :cite:`cpiechula`). Zu den bekannten Applikationen
(Abspielsoftware), sogenannte Media--Center, gehören beispielsweise das
XBMC--Media--Center oder das Windows--Media--Center.

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
