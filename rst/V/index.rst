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

.. figure:: fig/arch-overview.png
    :alt: Architekturübersich libhugin
    :width: 90%
    :align: center

    Architekturübersicht libhugin.

libhugin analyze
----------------

Dieser Teil (Abbildung :num:`fig-analyze-arch`) soll für nachträgliche
Metadatenanalyse zuständig sein und Schnittstellen für folgende Pluginarten
bereitstellen.

    * Modifier--Plugins
    * Analyzer--Plugins
    * Comperator--Plugins


