###########################################
Libhugin Einsatzmöglichkeiten in der Praxis
###########################################

Im Folgenden werden die beiden CLI--Demoanwendungen Geri und Freki vorgestellt,
sowie weitere Einsatzmöglichkeiten.

Geri
====

Geri ist eine CLI--Anwendung die zu Demozwecken aber auch als Testwerkzeug für
die libhugin harvest Library verwendet werden kann. Ein Überblick über die
Funktionalität und Möglichen Optionen zeigt die Hilfe des Tools:

.. code-block:: bash

   $python tools/geri -h
   Usage:
     geri (-t <title>) [-y <year>] [-a <amount>] [-p <providers>...] [-c <converter>] \
          [-o <path>] [-l <lang>] [-P <pm>]  [-r <processor>] [-f <pfile>] [-L]
     geri (-i <imdbid>) [-p <providers>...] [-c <converter>] [-o <path>] [-l <lang>] \
          [-r <processor>] [-f <pfile>] [-L]
     geri (-n <name>) [--items <num>] [-p <providers>...] [-c <converter>] [-o <path>]
     geri list-provider
     geri list-converter
     geri list-postprocessing
     geri -h | --help
     geri --version


Das Tool eignet sich neben dem Einsatz als Testwerkzeug für Library und Plugins
auch gut für Scripte und somit für automatische Verarbeitung *großer*
Datenmengen.

Im Angang C wird die Anewendung Anhand von Beispielen demonstriert.


Freki
=====

Freki ist für Demonstrationszwecke und das Testen der libhugin analyze Library
entwickelt worden. Folgend zum Überblick der Funktionalität die Hilfe des
Kommandozeilentools Freki:

.. code-block:: bash

   $python tools/freki
   Usage:
     freki create <database> <datapath>
     freki list <database>
     freki list <database> attr <attr>
     freki list <database> analyzerdata
     freki list-modifier | list-analyzer
     freki (analyze | modify) plugin <plugin> <database>
     freki (analyze | modify) plugin <plugin> pluginattrs <pluginattrs> <database>
     freki export <database>
     freki -h | --help
     freki --version

Freki erlaubt dem Benutzer eine ,,Datenbank'' aus externen Metadaten zu
generieren. Auf dieser Datenbank kann man folgend mit den Analyzern und
Modifiern die libhugin hier anbietet arbeiten und beispielsweise seine Metadaten
zu säubern. Ist man mit dem Gesamtergebnis zufrieden so kann die Datenbank
wieder ,,exportiert'' werden. Es werden die ,,neuen'' Metadaten in die
entsprechenden Metadatenfiles geschreiben.

Im Anhang D wird die Anwendung Anhand von Beispielen demonstriert.

Implementierung von libhugin in das Open Source Projekt XBMC
============================================================

Neben der Kommandozeilentools Geri und Freki wurde konzeptuell für das Xbox
Media Center ein Plugin geschreiben das libhugin als Metadaten--Dienst Nutzen
kann.


Da die direkte Integration in das XBMC aufgrund der begrenzten Zeit der
Projektarbeit nicht möglich ist, wurde hier der Ansatz eines ,,Proxy--Dienstes''
angewandt. Für Libhugin wurde mittels dem Webframework Flask ein *minimalier*
Webservice geschreiben, welcher über eine eigenst definierte API Metadaten an
das XBMC liefert.

* xbmc plugin
* vor und nachteile

Weitere Einsatzmöglichkeiten
============================

* libnotify
* scripting
