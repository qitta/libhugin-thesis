###############
Zusammenfassung
###############

Aktueller Stand
===============

Die aktuelle Implementierung zeigt einen modularen Prototypen der soweit für die
gezeigten Anwendungsfälle des Autors gut funktioniert.

Erfüllung der gesetzten Anforderungen
=====================================

Die vom Autor gesetzten Anforderungen (siehe :ref:`ref-requirements`) konnten
direkt über die Bibliothek oder durch Schreiben eines Plugins erfüllt werden.

Dennoch gibt es bei einigen Ansätzen Problemstellungen die nur schwer ,,gut''
umsetzbar sind.  Im Fall von *libhugin* wäre das die Normalisierung von Metadaten
über mehrere Onlinequellen hinweg. Das funktioniert im Moment beim Genre mittels
statisch gepflegter Abbildungen. Hier wären andere Ansätze, falls möglich,
wünschenswert.

Diese Problematik und mögliche andere Ansätze werden in der Bachelorarbeit
genauer betrachtet.

Defizite und Verbesserungen
===========================

Erweiterung des aktuellen Pluginsystems
---------------------------------------

**Provider--Plugins:** Momentan ist ein multilingualer, ein englischsprachiger
und drei deutschsprachige Provider implementiert (siehe Tabelle
:num:`table-provideroverview`). Betrachtet man die Möglichkeiten und Anzahl der
Plattformen, ist es wünschenswert weitere Provider zu implementieren.

Die aktuelle Attributstruktur die von den Provider befüllt wird ist aktuell
eine Vereinigungsmenge der möglichen Metadaten, die diese Provider liefern
können. Erweiterungen dieser Struktur um neue Provider und Attribute ist
wünschenswert.

Ein Attribut das in erster Linie einen Mehrgewinn bringen würde wäre die
*Stimmung*. Die Onlinequelle *jinni.com* (siehe :cite:`jinni`) hat ein Attribut
*Mood* und noch weitere interessante Attribute wie *Style*, die nach
Meinung des Autors, einen Mehrgewinn für eine Filmsammlung bringen würden.

Das *Stimmungs*--Attribut könnte man beispielsweise als *tag*--Attribut sogar
in die XBMC Metadatenstruktur aufnehmen und hier zusätzlich die Filme nicht nur
nach Genre sondern auch nach *Stimmung* gruppieren und auswählen.

**Postprocessor und Converter Plugins:** Hier wäre es wünschenswert
allgemein bekannte Converter Plugins wie beispielsweise für das
Windows--Media--Center zu implementieren.

Verbesserungen am Grundsystem
-----------------------------

**Provider Priorität**: Aktuell wird die *Priorität* der Provider per Hand
gepflegt. Hier wäre ein automatischer Ansatz denkbar und wünschenswert. Eine
Idee wäre es Fehlversuche und Timeouts zu protokollieren und Provider aufgrund
dieser zu bestrafen.  Der implementierte OFDb--Provider würde hier
wahrscheinlich recht schnell in der *Priorität* fallen, da dieser sehr oft
nicht erreichbar ist. Über diesen Ansatz würde sich zumindest aufgrund der
Verfügbarkeit eine Art *Qualität* der Provider bestimmen lassen.

**Yapsy:** Die aktuell verwendete Bibliothek für das Laden der Plugins wird
nur minimal genutzt. Hier wäre es sinnvoll diese Abhängigkeit komplett
aufzulösen und durch einen einfacheren Ansatz auszutauschen.

Weitere mögliche Verbesserungen
-------------------------------

**Geri und Freki:** Die beiden Kommandozeilen Tools lassen sich noch weiter
ausbauen. Das Analysetool Freki beherrscht im aktuellen Zustand noch keine
Comperator Plugins. Weitere denkbare Entwicklungen bei beiden Tools wären
automatisierte Analysen der Metadaten und statistische Auswertungen dieser.
Des Weiteren wäre ein zusätzliches *ncurses*--Interface, wie es beispielsweise
auch beim Mail Client *mutt* genutzt wird, wünschenswert und würde laut Meinung
des Autors die Benutzerfreundlichkeit im Vergleich zum einfachen CLI-Tool
erhöhen.

**Libhugin Proxy:** Der momentan implementierte Proxy zeigt nur
einen *konzeptuellen* Ansatz und ist aktuell für den Einsatz des XBMC--Plugins
geschrieben. Hier wäre eine generische Implementierung als CLI-Tool
wünschenswert.

**XBMC--Plugin:** Das aktuelle XBMC--Plugin kann soweit erweitert werden, dass
sich sämtliche libhugin Optionen direkt über das Plugin selbst im XBMC
konfigurieren lassen.


Denkbare Weiterentwicklungen
============================

Onlinequellen mit ,,neuem Wissen" anreichern
--------------------------------------------

Viele Onlinequellen, wie beispielsweise TMDb, haben Schlüsselwörter gepflegt.
Diese werden bei TMDb durch die Benutzer der Plattform gepflegt. Oft sind diese
jedoch gar nicht vorhanden oder sind zum Teil auch recht ungenau oder unpassend
gepflegt bei manchen Filmen.

Eine Idee wäre hier die Schlüsselwörter über einen Data--Mining--Algorithmus aus
der vorliegenden Inhaltsbeschreibung zu extrahieren. Dies könnte man aufgrund
der Architektur von libhugin problemlos automatisiert für die ganze
Filmsammlung machen und das neu gewonnene ,,Wissen" in die von der Community
gepflegte Plattform zurückfließen lassen.

Ob dies ein möglicher und vom Betreiber der Plattform wünschenswerter Ansatz
ist, sollte jedoch vorher mit dem Betreiber der Plattform abgeklärt werden.

Statistische Untersuchung der Metadaten
---------------------------------------

**Statistische Untersuchungen:** Der Analyze--Teil der Bibliothek bietet die
nicht weiter behandelte experimentelle Comperator--Plugin Schnittstelle. Die
Idee hierzu ist es Plugins zu entwickeln, die Film Metadaten verschiedener
Quellen untersuchen und miteinander vergleichen. Durch den Vergleich soll
statistisch die *Qualität* der Metadatenquellen untersucht werden.

Des Weiteren kann untersucht werden, wie gut sich Filme anhand bestimmter
Metadaten mit einander vergleichen lassen und ob man aufgrund von Metadaten,
Empfehlungen für ähnliche Filme aussprechen kann.


Systemintegration
-----------------

**D--Bus:** Neben einem generischen Proxy wäre auch die Implementierung eines
D--Bus--Service eine gute Idee um systemweit über eine
programmiersprachenunabhängige Schnittstelle auf die Library zugreifen zu
können.

**Programmiersprachen Bindings:** Für oft genutzte Sprache wäre eine Erstellung
von Bindings wünschenswert.

Abschließendes Fazit
====================

Das Projekt zeigt einen modularen Prototyp für die Suche und Analyse von Film
Metadaten, welcher die bisherigen Fähigkeiten der Movie--Manager um Data--Mining
Algorithmen erweitert. Des Weiteren zeigt dieser Ansatz, dass so die Metadaten
Suche und Analyse sich gut an benutzerspezifische Bedürfnisse anpassen lässt.
