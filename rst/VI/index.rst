###############
Implementierung
###############

Im Folgenden soll die API und die implementierten Plugins vorgestellt werden.

Libhugin--harvest API
=====================

Die API wurde sehr einfach gehalten und ermöglicht dadurch dem Benutzer ein
schnelles Einarbeiten. Folgendes Beispiel, in der interaktiven Python--Shell,
zeigt die typische Benutzung der API:

.. code-block:: python

   >>> from hugin.harvest.session import Session
   >>> session = Session()
   >>> query = session.create_query(title='Prometheus')
   >>> results = session.submit(query)
   >>> print(results)
   [<TMDBMovie <picture, movie> : Prometheus (2012)>,
   <OFDBMovie <movie> :  Prometheus - Dunkle Zeichen (2012)>,
   <OMDBMovie <movie> : Prometheus (2012)>]

Für weitere Beispiele siehe offizielle *libhugin--harvest* API :cite:`huginapi`.


Libhugin--harvest Plugins
=========================

Provider--Plugins
-----------------

Libhugin--harvest hat aktuell verschiedene Provider implementiert (siehe Abbildung
:num:`table-provideroverview`).

.. figtable::
    :label: table-provideroverview
    :caption: Übersicht implementierter Provider und Funktionalität.
    :spec: r|l|l|l|l|l
    :alt: Übersicht implementierter Provider und Funktionalität

    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    |                           | *TMDb*             | *OFDb*             | *Videobuster*      | *Filmstarts*       | *OMDb*             |
    +===========================+====================+====================+====================+====================+====================+
    | *Priorität*               | 90                 | 80                 | 70                 | 65                 | 65                 |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *Providerart*             | movie/person       | movie/person       | movie              | movie              | movie              |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *Metadaten*               | textuell/grafisch  | textuell           | textuell           | textuell           | textuell           |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *Sprache*                 | multilingual       | deutsch            | deutsch            | deutsch            | englisch           |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *Unschärfesuche Online*   | :math:`\times`     | :math:`\times`     | :math:`\times`     | :math:`\times`     | :math:`\times`     |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *Unschärfesuche libhugin* | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *IMDB--Suche Online*      | :math:`\checkmark` | :math:`\checkmark` | :math:`\times`     | :math:`\times`     | :math:`\checkmark` |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *IMDB--Suche  libhugin*   | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` | :math:`\checkmark` |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
    | *API verfügbar*           | :math:`\checkmark` | :math:`\checkmark` | :math:`\times`     | :math:`\times`     | :math:`\checkmark` |
    +---------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+

Ein paar der Provider, wie ``Filmstarts``, ``Videobuster`` lassen sich noch
weiter ausbauen. Diese unterstützen momentan nur textuelle Metadaten, würden
sich aber um grafische Metadaten erweitern lassen.


Postprocessor--Plugins
----------------------

Die Postprocessor--Plugins beim *libgugin--harvest* Teil sind für die direkte
,,Nachbearbeitung" der Daten gedacht.

**Compose:**
Das ``Compose``--Plugin ist das momentane Kernstück der Postprocessor--Plugins. Das
Plugin gruppiert die Ergebnisse verschiedener Onlinequellen nach Film und bietet
dem Benutzer dadurch folgende Möglichkeiten:

    1) Ergebnis komponieren.
    2) Genre zusammenführen.

**Zu 1.):** Es erlaubt dem Benutzer sich ein nach seinen Wünschen
zusammengesetztes Ergebnis zu komponieren. Der Benutzer kann über das Angeben
einer Profilmaske bestimmen, wie sich die Metadaten zusammensetzen sollen.
Hier kann er beispielsweise angeben, dass er den Filmtitel, Jahr und Cover vom
Provider *TMDb* möchte, die Inhaltsbeschreibung jedoch immer vom *Filmstarts*
Provider. Hier besteht auch die Möglichkeit eines ,,Fallbacks", falls *Filmstarts*
keine Inhaltsbeschreibung hat, dann kann auch auf andere Provider
zurückgegriffen werden.

Beispiel für eine Profilmaske, die TMDb als Standardprovider nimmt und die
Inhaltsbeschreibung vom OFDb Provider nimmt. Falls keine OFDb--Inhaltsbeschreibung
vorhanden ist, dann erfolgt ein ,,Fallback" auf den OMDb--Provider:

.. code-block:: bash

    $ echo "{'default':['tmdbmovie'], 'plot':['ofdbmovie', 'omdbmovie']}" > profilemask

Wird keine Profilmaske angegeben, so werden fehlende Attribute nach
Provider--Priorität aufgefüllt.

**Zu 2.):** Dieses Feature erlaubt dem Benutzer divergente Genres
beim gleichen Film zu verschmelzen. Das macht das Genre feingranularer und
behebt die genannte Problematik (siehe Abbildung :num:`table-feuchtgebiete`)
divergenter Genres bei verschiedenen Onlinequellen. Das Genre wird hier wie
folgt zusammengesetzt:

.. code-block:: bash

   # Drei Genre der Unterschiedlichen Provider      # Zusammengeführtes Genre
   [Comedy, Drama], [Komödie, Drama], [Erotik] ---> [Komödie, Drama, Erotik]


**Trim:**
Dies ist vergleichsweise ein einfaches Plugin, welches dafür zuständig, ist
vorangehende und nachziehende Leerzeichen bei den Metadaten zu entfernen. Das
Plugin führt eine Bereinigung durch, diese muss nicht explizit vom
Provider--Plugin durchgeführt werden.

Converter--Plugins
------------------

Bei den Converter--Plugins wurde zu Demonstrationszwecken ein *HTML*--Converter
und ein *JSON*--Converter implementiert.

Des Weiteren wurde für den Produktiveinsatz ein XBMC *Nfo*--Converter
implementiert, dieser wird vom *libhugin*--Proxy (siehe Libhugin--Proxy,
:ref:`libhuginproxy`) verwendet, um dem XBMC--libhugin Plugin (siehe XBMC Plugin
Integration, :ref:`xbmcplugin`) die Metadaten im richtigen Format zu liefern.

.. _analyzeapiexample:

Libhugin--analyze API
=====================

Die API von *libhugin--analyze* ist vom Grundaufbau ähnlich zu der
*libhugin--harvest* API. Folgendes Beispiel--Snippet zeigt die Anwendung des
``BracketClean``--Plugins auf *Rohdaten*, welche nicht aus der internen Datenbank
stammen.

.. code-block:: python

    >>> from hugin.analyze.session import Session
        # Beispieltext. Erstelle Sitzung mit Dummy DB. Hole BracketClean Plugin.
    >>> example_text = "Aus diesem Text wird die Klammer (welche?) samt Inhalt entfernt!"
    >>> session = session('/tmp/temporary.db')
    >>> BracketClean = session.modifier_plugins('BracketClean')
        # Wende Plugin im raw Modus auf Daten an
    >>> result = session.modify_raw(BracketClean, 'plot', example_text)
    >>> print(result)
    Aus diesem Text wird die Klammer samt Inhalt entfernt!


Für weitere Informationen siehe *libhugin*--API :cite:`huginapi`. Des Weiteren
zeigt die Demoanwendung Freki den Einsatz von *libhugin--analyze* (siehe :ref:`ref-freki`).


Libhugin--analyze Plugins
=========================

Modifier--Plugins
-----------------

**BracketClean:**
Das ``BracketClean``--Plugin ist für nachträgliche Manipulation der
Inhaltsbeschreibung gedacht. Das Plugin entfernt alle Klammern samt Inhalt aus
der Beschreibung. Das vereinheitlicht die Inhaltsbeschreibung in dem Sinne, dass
alle Schauspieler oder Informationen in Klammern aus der Beschreibung entfernt
werden.

**PlotLangChange:**
Das ``PlotLangChange``--Plugin ist für das nachträgliche Ändern der
Inhaltsbeschreibung zuständig. Es hat die Funktion, die Sprache des Plots zu
ändern.

Analyzer--Plugins
-----------------

**KeywordExtract:**
Dieses Plugin extrahiert aus einem Text, bei Filmen meist die
Inhaltsbeschreibung, relevante Schlüsselwörter, die den Text, beziehungsweise
die darin dargestellte Thematik repräsentieren.

**FileTypeAnalyze:**
Das ``FileTypeAnalyze``--Plugin arbeitet mit den Videodaten selbst. Es ist für die
Extraktion der Datei--Metadaten zuständig. Momentan extrahiert es:

    * Auflösung
    * Seitenverhältnis
    * Videocodec
    * Audiocodec, Anzahl der Audiokanäle, Sprache


**LangIdentify:**
Der ``LangIdentify``--Analyzer erkennt die Sprache des verwendeten Plots und schreibt
die Information zu den Analysedaten.

Comparator--Plugins
-------------------

Dieser Plugintyp ist experimentell, er ist für statistische Zwecke und
Analysen bezüglich der Vergleichbarkeit von Filmen anhand der Metadaten gedacht.

Folgende Comparator--Plugins wurden konzeptionell implementiert:

**GenreCmp:**
Ein Plugin, das die Genres verschiedener Filme miteinander vergleicht.

**KeywordCmp:**
Ein Plugin, das die Schlüsselwörter verschiedener Filme miteinander vergleicht.

.. raw:: Latex

   \newpage

Verschiedenes
=============

Testverfahren
-------------

Für das Testen der Software wird das Python Unittest--Framework verwendet.
Bisher wurden Tests für die wichtigsten Grundklassen und das
Provider--Pluginsystem erstellt, um ein valides Verhalten der Provider--Plugins
zu gewährleisten.

Die Unittests wurden direkt in der ,,Main" der jeweiligen Klasse untergebracht.
Diese werden dann beim Ausführen der Python--Datei gestartet.

Folgendes Beispiel zeigt die Funktionsweise:

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

.. code-block:: bash

    Ran 1 test in 0.000s

    OK

Alle geschriebenen Tests werden bei jedem ,,Einspielen" der Änderungen in das
verwendete Quellcode--Versionsverwaltungssystem automatisiert über einen
externen Dienst ausgeführt (siehe Entwicklungsumgebung, :ref:`dev`).


.. raw:: Latex

   \newpage


.. _dev:

Entwicklungumgebung
-------------------

**Programmiersprache:**
Für die Entwicklung der Bibliothek wurde die Programmiersprache Python, in der
Version 3.3, aus folgenden Gründen gewählt:

.. hübsch! Hab was neues gelernt.

:Rapid Prototyping Language:

    Wichtig bei einem Projekt dieser Größe mit begrenztem Zeitraum (vgl. :cite:`lutz2013learning`).

:Plattformunabhängigkeit:

    Plattformunabhängigkeit ist ein sekundäres Ziel des Projekts.

:Einfach erlernbar:

    Wichtig für Pluginentwickler wegen der kurzen Einarbeitungszeit.

:Verbreitungsgrad:

    Gängige Skriptsprache bei vielen Open--Source--Projekten.

:Optimierungsmöglichkeiten:

    Möglichkeit der Erweiterung durch
    :math:`\mathrm{C/C{\scriptstyle\overset{\!++}{\vphantom{\_}}}}`--Code,
    Optimierung von Python mittels Cython (siehe :cite:`cython`, vgl.
    :cite:`lutz2013learning`).

**Entwicklungssytem:**
Die Bibliothek wird unter *Archlinux* entwickelt. Für die Entwicklung wird der
Editor *gVim* mit entsprechenden Python--Plugins zur Validierung der Python
PEP--Stilrichtlinien (siehe :cite:`pep`) verwendet. Des Weiteren wird die
interaktive Python Shell *IPython* eingesetzt.

**Quellcodeverwaltung:**
Für die Quellcodeverwaltung wird das Versionsverwaltungssystem *git*
eingesetzt. Der Quellcode selbst wird auf dem Hosting--Dienst für
Software--Entwicklungsprojekte *GitHub* (siehe :cite:`github`) gelagert. Das
Projekt ist auf folgender GitHub Seite zu finden:

    * https://github.com/qitta/libhugin

**Automatisches Testen:**
Die oben genannten Softwaretests werden von *TravisCI* (siehe :cite:`travisci`),
einem sogenanntem ,,Continuous Integration Service" automatisch ausgeführt. Dies
passiert bei jedem Hochladen von Quellcodeänderungen auf *GitHub*. *GitHub* hat
hier eine Service--Schnittstelle zu *TravisCI,* welche aktiviert wurde.

Ein Symbol (siehe Abbildung :num:`fig-build`) auf der *libhugin*
Github--Projektseite teilt so dem Besuchern der Seite den aktuellen
,,Projektstatus" mit.

.. _fig-build:

.. figure:: fig/build.png
    :alt: Symbol, das den aktuellen ,,Build Status" der GitHub--Projektseite zeigt
    :width: 60%
    :align: center

    Symbol, das den aktuellen ,,Build--Status" der GitHub--Projektseite zeigt.


**Projektdokumentation:**
Das Projekt wird nach dem Prinzip der *literalen Programmierung*, wie von
*Donald E. Knuth* (siehe :cite:`knuth`) empfohlen, entwickelt. Hierbei liegen
Quelltext und Dokumentation des Programms in der gleichen Datei.

Die Dokumentation kann so über spezielle Softwaredokumentationswerkzeuge
generiert werden. Unter Python wird hier das Softwaredokumentationswerkzeug
*Sphinx* (siehe :cite:`sphinxdoc`) verwendet. Die offizielle
Projektdokumentation ist auf der Plattform *ReadTheDocs* (siehe :cite:`rtfd`)
gehostet und unter folgender Adresse zu finden:

    * http://libhugin.rtfd.org

Dieses kann eine Dokumentation in verschiedenen Formaten generieren, auch diese
Projektarbeit wurde in *reStructuredText* (siehe :cite:`rst`) geschrieben und
mit *Sphinx* generiert.

Des Weiteren wird dem Entwickler bei Nutzung der
Bibliothek in der interaktiven Python--Shell eine zusätzliche Hilfestellung
geboten (siehe Abbildung :num:`fig-knuth`).

.. _fig-knuth:

.. figure:: fig/knuth.png
    :alt: API--Dokumentation als Hilfestellung in der interaktiven Python--Shell bpython
    :width: 80%
    :align: center

    API--Dokumentation als Hilfestellung in der interaktiven Python--Shell bpython.

**Projektumfang:**
Der Projektumfang beträgt ca. 3500 *lines of code*,  hierzu kommt noch
die Onlinedokumentation hinzu. Eine Statistik zum Projekt, welche mit dem Tool
*cloc* erstellt wurde, ist im Anhang unter :ref:`ref-cloc` zu finden.


**Externe Bibliotheken:**
Die Tabelle :num:`table-libs` listet alle verwendeten externen Abhängigkeiten
für die *libhugin*--Bibliothek.

.. figtable::
    :label: table-libs
    :spec: r|l|l
    :alt: Übersicht über externe Abhängigkeiten
    :caption: Übersicht über externe Abhängigkeiten.

    +-------------------------+-----------------+---------------------------------+
    | *Abhängigkeit*          | *Verwendung in* | *Einsatzzweck*                  |
    +=========================+=================+=================================+
    | *yapsy*                 | Pluginsystem    | Laden von Plugins               |
    +-------------------------+-----------------+---------------------------------+
    | *charade*               | Downloadqueue   | Encodingerkennung               |
    +-------------------------+-----------------+---------------------------------+
    | *parse*                 | Plugins         | Parsen von Zeitstrings          |
    +-------------------------+-----------------+---------------------------------+
    | *httplib2*              | Downloadqueue   | Content download                |
    +-------------------------+-----------------+---------------------------------+
    | *jinja2*                | Plugins         | HTML Template Engine            |
    +-------------------------+-----------------+---------------------------------+
    | *docopt*                | Cli--Tools      | CLI--Optionparser               |
    +-------------------------+-----------------+---------------------------------+
    | *Flask*                 | Huginproxy      | Webframework, RESTful interface |
    +-------------------------+-----------------+---------------------------------+
    | *guess_language-spirit* | Plugins         | Spracherkennung                 |
    +-------------------------+-----------------+---------------------------------+
    | *PyStemmer*             | Plugins         | Stemming von Wörtern            |
    +-------------------------+-----------------+---------------------------------+
    | *pyxDamerauLevenshtein* | Plugins, Utils  | Vergleich von Strings           |
    +-------------------------+-----------------+---------------------------------+
    | *Pyaml*                 | Plugins         | Verarbeitung von Yaml Dateien   |
    +-------------------------+-----------------+---------------------------------+
    | *beaufifulsoup4*        | Plugins         | Parsen von HTML Seiten          |
    +-------------------------+-----------------+---------------------------------+
    | *xmltodict*             | Plugins         | Verarbeitung von XML Dokumenten |
    +-------------------------+-----------------+---------------------------------+
    | *hachoir-metadata*      | Plugins         | Extraktion von Datei--Metadaten |
    +-------------------------+-----------------+---------------------------------+
