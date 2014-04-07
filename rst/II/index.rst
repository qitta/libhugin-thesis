####################
Begriffsdefinitionen
####################

Im Folgenden werden Fachbegriffe und Begriffe, die im Kontext von *libhugin*
anders besetzt sind, definiert:

Fachbegriffe
------------

.. glossary::

    Metadaten

     Metadaten sind beschreibende Daten, die Informationen über andere Objekte
     enthalten.

    Home--Theatre--PC

     Ein auf PC--Komponenten basierendes Gerät zur Wiedergabe multimedialer
     Inhalte. Dieser wird oft mit sogenannter Media--Center--Software wie dem
     XBMC betrieben.

    Smart--TV

     Bezeichnung für einen Fernseher der eine Computerfunktion integriert hat
     und internetfähig ist.

    XML

     Extensible Markup Language, eine Auszeichnungssprache zur baumartig
     strukturierten Darstellung von Daten in Form von Textdateien.

    JSON

     JavaScript--Object--Notation, eine Auszeichnungssprache ähnlich wie *XML*
     mit dem Ziel von Mensch und Maschine einfacher lesbar als *XML* zu sein.

    Hashtabelle

     Eine spezielle Datenstruktur, bei welcher Daten jeweils einem eindeutigen
     Index zugeordnet sind. Der Zugriff auf die Daten erfolgt mit konstantem
     Aufwand.

    Scraper

     Auch Webscraper genannt, werden Anwendungen genannt die in der Lage sind
     Informationen aus Webseiten zu extrahieren. Ein Scraper gibt sich einer
     Webseite gegenüber wie ein normaler Webbrowser aus. So wird eine
     maschinelle Verarbeitung der Informationen auf dieser Webseite möglich.

    RESTful

     Eine Form einer Web--API, bei der mithilfe von Standard HTTP--Verben
     und speziellen, menschenlesbaren URLs bestimmte Aktionen getriggert werden
     können. So kann man sich beispielsweise mit einer GET Operation
     Informationen von einem Service beschaffen.


Kontextspezifische Fachbegriffe
-------------------------------

.. glossary::

    Plugin

     Im Kontext von *libhugin* sind Plugins kleine Module welche zur Laufzeit
     austauschbar sind. Diese können von Dritten geschreiben werden um das
     System an die eigenen Bedürfnisse anzupassen.

    Provider

     Im Kontext von *libhugin* ist ein Provider eine Art ,,Vermittler" zwischen
     der entwickelten Bibliothek und einem Online--Webservice der Metadaten
     anbietet. Der Provider ist Bestandteil der Bibliothek und wird als Plugin
     in dieser implementiert.

    Postprocessor

     Im Kontenxt von *libhugin* ist ein Postprocessor ein Plugin, welches für
     die direkte Nachbearbeitung der heruntergeladenen Metadaten verwendet wird.

    Converter

     Im Kontext von *libhugin* ist ein Converter ein Plugin das für das
     Konvertieren eines Ergebnisses in ein bestimmtes Metadatenformat wie
     beispielsweise das XBMC nfo--Format zuständig ist.

    Modifier

     Im Kontext von *libhugin* ist ein Modifier ein Plugin, welches für die
     nachträgliche Bearbeitung von Filmmmetadaten verwendet wird. Das kann
     beispielsweise das Ändern der Sprache der Inhaltsbeschreibung sein.

    Analyzer

     Im Kontext von *libhugin* ist ein Analyzer ein Plugin, welches für die
     nachträgliche Analyse von Filmmmetadaten verwendet wird. Dies kann
     beispielsweise die Erkennung der Sprache der Inhaltsbeschreibung sein.

    Comperator

     Im Kontext von *libhugin* ist ein Comperator ein Plugin, welches für
     Vergleiche zuständig ist. Mit Hilfe dieser Pluginart soll im späteren
     Verlauf untersucht werden wie gut sich Filme anhand von Metadaten
     vergleichen lassen und ob sich beispielsweise Film--Empfehlungen aufgrund
     der gewonnenen Daten aussprechen lassen. Diese Pluginart ist experimentell
     und nur konzeptuell in *libhugin* integriert.
