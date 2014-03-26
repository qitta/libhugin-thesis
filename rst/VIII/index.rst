########
Ausblick
########

Aktueller Stand
===============

Allgemein
---------

Die aktuelle Implementierung zeigt einen modularen Prototypen der soweit für die
gezeigten Anwendungsfälle des Autors gut funktioniert.

Die gesetzten Anforderungen konnten direkt über die Library oder durch schreiben
eines Plugins erfüllt werden. Dennoch gibt es bei einigen Ansätzen
Problemstellungen die nur schwer ,,gut'' umsetzbar sind. Im Fall von Libhugin
wäre das die Normalisierung von Metadaten über mehrere Anbieter hinweg. Das
Funktioniert im Moment beim Genre mittels einem statischen Mapping. Hier wären
andere Ansätze, falls möglich, wünschenswert.

Die genannte Problematik und mögliche andere Ansätze werden in der
Bachelorarbeit genauer betrachtet.

Plugins
-------

Provider--Plugins
~~~~~~~~~~~~~~~~~

Momentan ist ein multilingualer, ein englischsprachiger und drei deutschsprachige
Provider implementiert. Betrachtet man die Möglichkeiten und Anzahl der
Plattformen, ist es wünschenswert weitere Provider zu implementieren.

Die aktuelle Attributestruktur die von den Provider befüllt wird ist mehr oder
einer Vereinigungmenge der möglichen Metadaten, die diese Provider liefern
können. Erweiterungen dieser Struktur um neue Provider und Attribute ist
wünschenswert. Eine Liste mit möglichen recht bekannte Plattformen:

Ein Ansatz bzw. Attribut das hier in erster Linie einen Mehrgewinn bringen würde
wäre die ,,Stimmung''. Die Plattform http://www.jinni.com hat ein Attribut
,,mood'' und noch weitere Interessante Attribute wie ,,Style'' die einen
nach Meinung des Autors einen Mehrgewinn für eine Filmsammlung bringen würden.
Das Stimmnugs--Attribut könnte man beispielsweise als ,,tag'' Attribut sogar in
die Xbox Media Center Metadatenstruktur aufnehmen und hier dann zusätzlich die
Filme nicht nur nach Genre und Inhaltsbeschreibung sondern auch nach
,,Stimmung'' ausswählen.

Postprocessing-- und OutputConverter--Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hier wäre es wünschenswert allgemein bekannte Converter Plugins wie
beispielsweise für das Windwos Media Center zu implementieren.

Libhugin Proxy und XBMC Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der momentan implementierte Proxy zeigt nur einen *konzeptuellen* Ansatz und
ist aktuell für den Einsatz des Xbox Media Center Plugins geschreiben. Hier
wäre eine generische Implementierung eines Proxies als CLI-Tool wünschenswert.

Das aktuelle XBMC Plugin kann soweit erweitert werden, dass sich sämtliche
libhugin Optionen direkt über das Plugin selbst im XBMC konfigurieren lassen.

Systemintegration
~~~~~~~~~~~~~~~~~

Neben einem generischen Proxy wäre auch die Implementierung eines
D--Bus--Service eine gute Idee um systemweit über eine
programmiersprachenunabhängige Schnittstelle auf die Library zugreifen zu
können.

Analyze--Part
-------------


Statistische Untersuchungen
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Analyze--Teil der library bietet die nicht weiter behandelte
experimentelle Comperator--Plugin Schnittstelle. Die Idee hierzu ist es Plugins
zu entwickeln, die Filmmetadaten verschiedener Quellen untersuchen und
miteinander vergleichen. Durch den Vergleich soll statistisch die
,,Qualität'' der Metadaten der Provider untersucht werden.

Des Weiteren kann untersucht werden wie gut sich Filme anhand bestimmter
Metadaten mit einander vergleichen lassen und ob man aufgrund von Metadaten
Empfehlungen für ,,ähnliche'' Filme aussprechen kann.

Wissen zurückgeben
~~~~~~~~~~~~~~~~~~

Viele Plattformen, wie auch TMDb, haben Schlüsselwörter gepflegt. Diese werden
bei TMDb durch die Benutzer der Plattform gepflegt. Oft sind diese jedoch gar
nicht vorhanden oder sind zum Teil auch recht ungenau oder unpassend gepflegt
bei manchen Filmen.

Eine Idee wäre hier die Schlüsselwörter über einen Data--Mining Algorithmus aus
der vorliegenden Inhaltsbeschreibung zu extrahieren. Dies könnte man aufgrund
der Architektur von libhugin problemlos automatisiert für die ganze
Filmesammlung machen und das neu gewonnene ,,Wissen'' in die von der Community
gepflegte Plattform zurückfließen lassen.

Ob die ein möglicher und vom Betreiber der Plattform wünschenswerter Ansatz ist
sollte jedoch vorher mit dem Betreiber der Plattform abgeklärt werden.

Weitere Verbesserungen
======================

Yapsy
-----

Die aktuell verwendete Library (yapsy) für das Laden der Plugins wird nur
minimal genutzt. Hier wäre es sinnvoll diese Abhängigkeit komplett aufzulösen
und durch einen einfacheren Ansatz auszutauschen.

Provider Priorität
------------------

Aktuell wird die *Priorität* der Provider per Hand gepflegt. Hier wäre ein
automatischer Ansatz denkbar und wünschenswert. Eine Idee wäre es Fehlversuche
und Timeouts zu protokollieren und Provider aufgrund dieser zu ,,bestrafen''.
Der Implementierte OMDb--Provider würde hier wahrscheinlich recht schnell in der
*Priorität* fallen, da dieser sehr oft unerreichbar ist. Über diesen Ansatz
würde sich zumindest aufgrund der Verfügbarkeit eine Art Qualität der Provider
bestimmen lassen.
