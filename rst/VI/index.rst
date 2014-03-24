###############
Implementierung
###############

Im folgenden soll die API und die implementierten Plugins vorgestellt werden.

libhugin harvest API
====================

Die API wurde sehr einfach gehalten und ermöglicht dadurch dem Benutzer ein
schnelles Einarbeiten. Folgendes Beispiel, in der interaktiven Python--Shell
,zeigt die typische BenuSuccess!  Wrote 50 pagestzung der API
Success!  Wrote 50 pages
.. code-block:: python

   >>> from hugin.harvest.session import Session

   >>> session = Session()
   >>> query = session.create_query(title='Prometheus')
   >>> results = session.submit(query)
   >>> print(results))
   [<TMDBMovie <picture, movie> : Prometheus (2012)>,
   <OFDBMovie <movie> :  Prometheus - Dunkle Zeichen (2012)>,
   <OMDBMovie <movie> : Prometheus (2012)>]

Für weitere Beispiele siehe Angang X. Eine ausführliche API Dokumentation zum
Projekt ist Online unter http://libhugin.rtfd.org zu finden.

Libhugin harvest Plugins
------------------------

Provider--Plugins
~~~~~~~~~~~~~~~~~

The Movie Database
""""""""""""""""""

Die TMDb ist im Moment der bevorzugte Metadaten--Provider. Für diesen wurde ein
Movie und ein Person Plugin implementiert. Er unterstützt neben der textuellen
Suche auch die Suche nach Bildmaterial. Der Provider wird über die offizielle
API (siehe Angang X) angesprochen.

    * **TMDBMovie**, Metadaten: textuell, grafisch, multilingual
    * **TMDBPerson**, Metadaten: textuell, grafisch, multilingual

Open Movie Database
"""""""""""""""""""

Die Open Movie Database API (siehe OMDB) bietet hauptsächlich textuelle
englischsprache Metadaten. Hier wurde auch ein Film und Personen Provider
implementiert.

    * **OMDBMovie**, Metadaten: textuell, englischsprachig
    * **OMDBPerson**, Metadaten: textutell, englischsprachig

Online Filmdatenbank
""""""""""""""""""""

Die Online Filmdatenbank ist eine deutschsprachige Plattform die ebenso eine API
anbietet. Hier wurde ein Movie Provider implementiert.

    * **OFBDMovie**, Metadaten: textuell, deutschsprachig

Videobuster.de
""""""""""""""

Videobuster ist eine deutschsprachige BluRay und DVD Verleihplattform. Sie
bietet leider keine API. Der hier implementierte Provider muss die Daten manuell
extrahieren. Die Plattform eignet sich gut um seine digitalisierte
BluRay/DVD--Sammlung mit Metadaten zu versorgen. Hier wurde ein Movie Provider
implementiert.

    * **VIDEOBUSTERMovie**, Metadaten: textuell, deutschsprachig

Filmstarts.de
"""""""""""""

Filmstarts ist eine *gute* deutsprachige Filmeplattform mit Review, Kritiken und
allgemeinen Filminformationen.  Die Seite bietet wie Videobuster keine API. Hier
wurde ein Movie Provider implementiert.

    * **FILMSTARTSMovie**, Metadaten: textuell, deutschsprachig


*Die beiden Plattformen Filmstarts und Videobuster bieten auch Personen Metadaten
und grafische Metadaten an, diese müssen jedoch noch implementiert werden.*


Postprocessing Plugins
~~~~~~~~~~~~~~~~~~~~~~

Die Postprocessing Plugins beim libgugin harvest Teil sind für die direkte
,,Nachbearbeitung'' der Daten gedacht. Über diese sollen sich beispielsweise
,,Provider--Kombinationen'' realisieren lassen oder eine bestimmte
Foarmatierung/Encoding bestimmt werden.

Composer
""""""""

Das Composer Plugin ist das momentane Kernstück der Postprocessing Metadaten. Es
erlaubt dem Benutzer sich ein nach seinen wünschen zusammengesetztes Ergebnis zu
,,kompoinieren''. Der Benutzer kann über das angeben eine ,,Pofilemaske''
bestimmten wie sich die Metadaten zusammensetzen sollen. Hier kann er
beispielsweise angeben dass er den Filmtitel, Jahr, Cover vom Provider TMDb
möchte, die Inhaltsbeschreibung jedoch immer vom Filmstarts Provider. Hier
besteht auch die Möglichkeit eines ,,Fallbacks'', falls Filmstarts keine
Inhaltsbeschreibung hat, dann kann auch auf andere Provider zurückgegriffen
werden. Die Beispiele im Angang YYY sowie die Beispiele der Demoanwendung Geri
(YYY2) zeigen den Einsatz des Plugins.

ResultTrimmer
"""""""""""""

Der Resulttrimmer ist vergleichsweise eine einfaches Plugin, welches dafür
zuständig ist vorangehende und nachziehende Leerzeichen bei den Metadaten zu
entfernen. Das Plugin fürht so gesehen nur eine ,,Säuberung'' durch, diese muss
nicht vom Provider Plugin durchgeführt werden.


OutputConverter Plugins
~~~~~~~~~~~~~~~~~~~~~~~

Bei den OutputConverter Plugins wurde zu Demozwecken ein HTML--OutputConverter
und ein Json--OutputConverter implementiert.

Des weiteren wurde für den ,,Produktiveinsatz'' ein XBMC-NFO-Fileconverter
implementiert, dieser wird von der Demoanwendung ,,libhugin proxy'' (siehe SDA)
verwendet um den XBMC--libhugin--Plugin die Metadaten im richtigen Format zu
liefern.


libhugin analyze API
====================

Die API von libhugin analyze ist vom Grundaufbau ähnlich zu der libhugin harvest
API. Folgendes Beispielsnippet zeigt die Anwendung des ,,Plotcleaner''--Plugins
auf 'Rohdaten'.


.. code-block:: python

    >>> from hugin.analyze.session import Session

        # Beispieltext. Erstelle Sitzung mit Dummy DB. Hole PlotClean Plugin.
    >>> example_text = "Aus diesem Text wird die Klammer (welche?) samt Inhalt entfernt!"
    >>> session = session('/tmp/temporary.db')
    >>> plotclean = session.modifier_plugins('plotclean')  # hole das PlotClean Plugin

        # Wende Plugin im raw Modus auf Daten an
    >>> result = session.modify_raw(plotclean, 'plot', example_text)
    >>> print(result)
    Aus diesem Text wird die Klammer samt Inhalt entfernt!


Ein weiteres ausführliches Beispiel findet sich im Anhang S. Desweiteren
demonstriert die Demoanwendung Freki den Einsatz des Analyzeteils der Library.
Die offizielle API Beschreibung ist unter http://libhugin.rtfd.org zu finden.


Libhugin analyze Plugins
------------------------

Modifier Plugins
~~~~~~~~~~~~~~~~

plotclean
"""""""""

Das PlotClean Plugin ist für nachträgliche Manipulation der
Filminhaltsbeschreibung gedacht. In Fall vom PlotClean Plugin werden alle
Klammern samt Inhalt aus der Beschreibung entfernt. Das ,,vereinheitlich'' die
Inhaltbeschreibungen in dem Sinne dass alle Schauspieler oder Informationen in
Klammern aus der Beschreibung entfernt werden.

plotchange
""""""""""

Das PlotChange Plugin ist für das nachträgliche ändern der Inhaltsbeschreibung
zuständig. Im Moment hat es die Option die Sprache des Plots zu ändern.

Analyzer Plugins
~~~~~~~~~~~~~~~~

filetype analyzer
"""""""""""""""""

Der Filetype--Analyzer arbeitet mit den Videodaten selbst. Er ist für die
extraktion der Datei--Metadaten zuständig. Momentan extrahiert er

    * Auflösung
    * Seitenverhältnis
    * Videocodec
    * Audiocodec, Anzahl der Audiokanäle, Sprache

plotlang
""""""""

Der Plotlang--Analyzer erkennt die Sprache des verwendeten Plots und schreibt
die Information in das Analyzerdata Array.


Comperator Plugins
~~~~~~~~~~~~~~~~~~

Dieser Plugintyp ist experimentiell, er ist für statistische Zwecke und
*Forschungsarbeiten* bzgl. der Vergleichbareit von Filmen anhand Metadaten
gedacht. Weiteres hierzu wird in der Bachelorarbeit behandelt.

Die Plugins die man hier findet sind:

genrecmp
""""""""

Ein Plugin, das die Genres verschiedener Filme miteinander vergleicht.

keywordcmp
""""""""""

Ein Plugin, das die Schlüsselwörter verschiedener Filme miteinander vergleicht.


Verschiedenes
=============

Testverfahren
-------------

Für das Testen der Software wird das Python Unittest Framework verwendet. Bisher
wurden Tests für die wichtigsten Grundklassen und das Provider Plugins
subsustem um ein valides Verhalten der Provider Plugins zu gewährleisten.

Die Unittests können direkt in der ,,Main'' der jeweiligen Klasse untergebracht
werden. Diese werden dann beim Ausführen der Python--Datei ausgeführt.

.. code-block:: python

   def add(a, b): return a + b

   if __name__ == '__main__':

       import unittest
       class SimpleTest(unittest.TestCase):

           def test_add_func(self):
               result = add(21, 21)
               self.assertTrue(result == 42)

       unittest.main()


Das Ausführen des Beispielcodes würde folgende Ausgabe produzieren:

.. code-black:: bash

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

Alle geschrieben Tests werden bei jedem ,,Einspielen'' der Änderungen in das
verwendete Quellcode--Versionsverwaltungssystem automatisiert über einen
externen Dienst ausgeführt (siehe Entwicklungumgebung).

Entwicklungumgebung
-------------------

Programmiersprache
~~~~~~~~~~~~~~~~~~

Für die Entwicklung der Library wurde bewusst die Programmiersprache Python 3.3
aus folgenden Gründen gewählt:

    * **Rapid Prototyping Language**, wichtig bei einem Projekt dieser Größe mit
      begrenztem Zeitraum
    * **Plattformunabhängigkeit**, Plattformunabhängigkeit ist ein Sekundäres
      Ziel des Projekts
    * **Einfach erlernbar (siehe Tauben)**, Programmiersprache ,,leicht''
      menschenlesbar (Plugin--Entwickler)
    * **Scriptsprache**, Gängige Scriptsprache bei vielen free Software
      Projekten
    * **Optimierungsmöglichkeiten**,  Cython, C/C++--Languagebindings

Entwicklung
~~~~~~~~~~~

Die Library wird unter *Archlinux* entwickelt. Für die Entwicklung wird der
Editor *gVim* mit entsprechenden Python--Plugins zur Validierung der Python PEP
Stilrichtlinien verwendet. Des weiteren wird die interaktive Python Shell
*IPython* eingesetzt.

Für die Quellcodeverwaltung wird das Versionsverwaltungssystem *git*
eingesetzt. Der Quellcode selbst wird auf Hosting--Dienst für
Software--Entwicklungsprojekte github.com (LINK!) gelagert.

Die o.g. Softwaretests werden von *TravisCI*, einem sog. ,,continuous integration
service'', bei jedem hochladen der Änderungen auf github, ausgeführt. Dieser
Dienst wurde über github aktiviert. Ein Logo (Abb.: s) auf der Projektseite Teil dem
Entwickler und Besuchern der Seite mit ob das Projekt alle geschreibenen Tests
,,besteht''.

.. _fig-build

.. figure:: fig/build.png
    :alt: TravisCI Build png
    :width: 80%
    :align: center

    Logo die den aktuellen ,,Build Status'' des Projekts grafisch visualisiert.

Dokumentation
~~~~~~~~~~~~~

Das Projekt wird nach den Regeln der ,,literalten Programmierung'', wie nach
Donald E. Knuth empfohlen, entwickelet. Hierbei liegen Quelltext und
Dokumentation des Programmes in der gleichen Datei.

.. _fig-knuth

.. figure:: fig/knuth.png
    :alt: API Dokumentation in interaktiver Shell
    :width: 80%
    :align: center

    API--Dokumentation als Hilfestellung in interaktivier Python--Shell.

Die Dokumentation kann so über spezielle Softwaredokumentations--Tools generiert
werden. Unter Python wird hier das Softwaredokumentationswerkzeug *Sphinx*
verwendet. Dieses kann die Dokumentation in verschiedenen Formaten generieren.
Diese Projektarbeit wurde auch *reStructuredText* und *Sphinx* generiert.


Abhängigkeiten
--------------

libhugin ist abhängig -- meth.

Projektumfang
-------------

Der Projektumfang (siehe Abb.: s) beträgt ~3500 *lines of code*,  hier kommt noch die
Onlinedokumentation hinzu.

.. code-block:: bash

    $ cloc hugin/ tools/
         119 text files.
         117 unique files.
          87 files ignored.

    http://cloc.sourceforge.net v 1.60  T=0.51 s (109.5 files/s, 11970.3 lines/s)
    -------------------------------------------------------------------------------
    Language                     files          blank        comment           code
    -------------------------------------------------------------------------------
    Python                          49           1220           1171           3540
    XML                              5              1              0             57
    HTML                             2              9            113             10
    -------------------------------------------------------------------------------
    SUM:                            56           1230           1284           3607
    -------------------------------------------------------------------------------
