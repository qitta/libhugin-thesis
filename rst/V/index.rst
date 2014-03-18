#######
Entwurf
#######

*Im folgenden wird der systematische Entwurf der Software dargestellt. Die
verwendetetn Algorithmen, Probleme sowie Möglichgeiten der technischen Umsetzung
werden in der Bachelorarbeit genauer beleuchtet und diskutiert.*

Grundüberlegung
===============

Die Library soll über die Metadatenbeschaffung hinaus Werkzeuge zur
Metadatenanalyse bereitstellen. Um eine saubere Trennung zwischen
Metadatenbeschaffung und Metadatenanalyse zu schaffen, wird die Library in die
zwei Teile *libhugin harvest* und *libhugin analyze* aufgeteilt.

Libhugin Architektur
====================

libhugin harvest
----------------

Dieser Teil (siehe Abbildung :num:`fig-harvest-arch`) soll für die
Metadatenbeschaffung zuständig sein und Schnittstellen für die folgenden
Pluginarten bereitstellen:

    * Provider--Plugins
    * Postprocessing--Plugins
    * Output--Converter--Plugins

.. _fig-harvest-arch

.. figure:: fig/harvest-arch.png
    :alt: Architekturübersich libhugin harvest
    :width: 90%
    :align: center

    Architekturübersicht libhugin harvest.

**Session**

Das ist der *Einstiegspunkt* für libhugin harvest. Über eine Sitzung
konfiguriert der Benutzer das ,,System'' und hat Zugriff auf die verschiedenen
Plugins.

**Queue**

Die Queue wird verwendet um die Suchanfrage zu konfigurieren. Hier werden auch
für nicht gesetzte Parameter ,,Defaultwerte'' gesetzt.

**Cache**

Wird verwendet um erfolgreiche Ergebnisse von Suchanfragen persistent
zwischenzuspeichern. So können die Daten bei wiederholter Anfrage aus dem Cache
geladen werden. Dies funktioniert schneller und entlastet den Metadatenanbieter.

**Downloadqueue**

Die Downloadqueue ist für den eigentlichen Download der Daten zuständig. Die
Provider--Plugins müssen so keine eigene Downloadqueue implementieren. Durch
eine zentrale Downloadqueue bleibt die Kontrolle über den Download der Daten bei
libhugin selbst und nicht bei den Plugins.

**GenreNormalize**

GenreNormalize kann von den Provider--Plugins verwendet werden um das Genre zu
*normalisieren*.

libhugin analyze
----------------

Dieser Teil (Abbildung :num:`fig-analyze-arch`) soll für nachträgliche
Metadatenanalyse zuständig sein und Schnittstellen für folgende Pluginarten
bereitstellen.

    * Modifier--Plugins
    * Analyzer--Plugins
    * Comperator--Plugins


.. _fig-analyze-arch

.. figure:: fig/analyze-arch.png
    :alt: Architekturübersich libhugin analyze
    :width: 90%
    :align: center

    Architekturübersicht libhugin analyze.

