#################
Metadatenquellen
#################

Die im Prototypen implementieren Metadatenquellen weisen unterschiedliche
Eigenschaften auf. Für die Entwicklung des Prototypen wurden bestimmte Annahmen
getroffen wie beispielsweise, dass sich die Genreverteilung unterscheidet.

Für die Analyse der Metadaten eine Metadaten--Stichprobe von 2500 Filmen mit
Hilfe der  *libhugin-harvest*--Bibliothek beschafft. Die Zusammenstellung
besteht aus möglichst zufällig gewählten Filmen verschiedener Kategorien.

Die folgende Auswertung zeigt die Verteilung der Filme anhand vom Erscheinungsjahr:

.. figtable::
    :label: fig-testdata
    :caption: Testdaten nach Erscheinungsjahr
    :alt: Testdaten nach Erscheinungsjahr

   +----------------------+------------+----------------------+------------+----------------------+------------+
   | **Erscheinungsjahr** | **Anzahl** | **Erscheinungsjahr** | **Anzahl** | **Erscheinungsjahr** | **Anzahl** |
   +======================+============+======================+============+======================+============+
   | 2013                 | 53         | 2001                 | 76         | 1989                 | 15         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2012                 | 224        | 2000                 | 57         | 1988                 | 13         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2011                 | 253        | 1999                 | 50         | 1987                 | 10         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2010                 | 244        | 1998                 | 55         | 1986                 | 13         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2009                 | 245        | 1997                 | 48         | 1985                 | 12         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2008                 | 226        | 1996                 | 27         | 1984                 | 15         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2007                 | 194        | 1995                 | 40         | 1983                 | 7          |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2006                 | 135        | 1994                 | 23         | 1982                 | 10         |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2005                 | 118        | 1993                 | 18         | 1981                 | 4          |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2004                 | 109        | 1992                 | 19         | 1980                 | 9          |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2003                 | 77         | 1991                 | 12         | 1979                 | 4          |
   +----------------------+------------+----------------------+------------+----------------------+------------+
   | 2002                 | 74         | 1990                 | 11         |                      |            |
   +----------------------+------------+----------------------+------------+----------------------+------------+

Der *libhugin-harvest* Prototyp der für die Beschaffung der Metadaten verwendet
wird hat die Folgenden Movie--Provider implementiert:

    * TMDb, multilingual, Online--Filmdatenbank (API)
    * OMDb, englischsprachig, Metadatenanbieter (API)
    * OFDB, deutschsprachig, Online--Filmdatenbank (API)

    * Filmstarts.de, deutschsprachig, Filme--Plattform, (keine API)
    * Videobuster.de, deutschsprachig, Filme Verleihdienst (keine API)

Desweiteren wurden noch Person--Provider für TMDb und OFDb implementiert.
