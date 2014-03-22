###############
Implementierung
###############

Im folgenden soll beispielhaft die API und die implementierten Plugins
vorgestellt werden.

libhugin harvest API
====================

Libhugin harvest Plugins
------------------------

Provider--Plugins
~~~~~~~~~~~~~~~~~

    * tmdb movie
    * tmdb person
    * omdb movie
    * omdb person
    * ofdb movie
    * videobuster movie
    * filmstars movie


Postprocessing Plugins
~~~~~~~~~~~~~~~~~~~~~~

    * Composer
    * ResultTrimmer

OutputConverter Plugins
~~~~~~~~~~~~~~~~~~~~~~~

    * html
    * json
    * nfo

libhugin analyze API
====================

Libhugin analyze Plugins
------------------------

Modifier Plugins
~~~~~~~~~~~~~~~~

    * plotchange
    * plotclean

Analyzer Plugins
~~~~~~~~~~~~~~~~

    * filetype analyzer
    * plotlang

Comperator Plugins
~~~~~~~~~~~~~~~~~~

    * genrecmp
    * keywordcmp





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

    christoph@hitomi [06:45:20] [~/code/libhugin] [master *]
    -> % cloc hugin tools
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

