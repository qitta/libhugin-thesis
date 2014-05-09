##########################
Allgemeines zur Bibliothek
##########################

Die zu evaluierende Bibliothek *libhugin*, die vom Autor entworfen wurde, lässt
sich über die Metadatenbeschaffung hinweg auch um Plugins mit der Funktionalität
der Metadatenaufbereitung erweitern. Die Bibliothek wurde in die zwei Teile
*libhugin--harvest* (Metadatenbeschaffung) und *libhugin--analyze*
(Metadatenaufbereitung) aufgeteilt.

**Libhugin--harvest:** Dieser Teil der Bibliothek unterstützt die folgenden
Pluginarten:

**Provider--Plugins**

Plugins, welche den Zugriff auf die Onlinequellen ermöglichen.

**Postprocessor--Plugins**

Plugins, welche für die direkte Bearbeitung der Metadaten nach dem Herunterladen
verwendet werden.

**Converter--Plugins**

Plugins, welche bestimmte Metadaten Export--Formate unterstützen.


**libhugin--analyze:** Dieser Teil der Bibliothek unterstützt die folgenden
Pluginarten:


.. epigraph::

   | |apostart| *Human beings, who are almost unique in having the ability to learn from the*
   | |apopar|  *experience of others, are also remarkable for their apparent disinclination to do so.* |apoend|

   -- *Douglas Adams, ,,Last Chance to See''*

You can reference a section by its label. This chapter is
Chapter |nbsp| :ref:`ch-refs`.

.. _sec-refs-sub1:

Subsection
==========

This subsection is Section |nbsp| :ref:`sec-refs-sub1`.

Citations
=========

COLLADA |nbsp| :cite:`collada` is a cool 3D file format. I wrote a paper about
3D stuff |nbsp| :cite:`icmepaper`. The website we built is running |nbsp|
:cite:`open3dhub`. The bibliography is in bibtex format.

Footnotes
=========

Reference a footnote |nbsp| [#foot-something]_.

External Links
==============

You can link to a `website <http://google.com/>`_.

.. rubric:: Footnotes

.. [#foot-something] This is a footnote at the end of the page or document.

