#########################
Analyse Metadatenquellen
#########################

Die im Prototypen implementieren Metadatenquellen weisen unterschiedliche
Eigenschaften auf. Für die Entwicklung des Prototypen wurden bestimmte Annahmen
getroffen wie beispielsweise, dass sich die Genreverteilung unterscheidet.

Für die Analyse der Metadaten wurden für 2800 Filme Metadaten mit Hilfe von
*libhugin-harvest* bezogen. Die Zusammenstellung besteht aus möglichst zufällig
gewählten Filmen verschiedener Kategorien.

Der *libhugin-harvest* Prototyp der für die Beschaffung der Metadaten verwendet
wird hat die Folgenden Movie--Provider implementiert:

    * TMDb, multilingual, Online--Filmdatenbank (API)
    * OMDb, englischsprachig, Metadatenanbieter (API)
    * OFDB, deutschsprachig, Online--Filmdatenbank (API)
    * Filmstarts.de, deutschsprachig, Filme--Plattform, (keine API)
    * Videobuster.de, deutschsprachig, Filme Verleihdienst (keine API)
