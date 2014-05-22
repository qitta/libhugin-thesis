################
Metadatenanalyse
################

Zugriffszeiten Metadatenquellen
===============================

Performance der Metadatenquellen variiert je nach Lokation, Uhrzeit,
Internetanbindung, Serverauslastung sowie weiteren zum Teil unbekannten
Faktoren. Um eine groben Überblick zu bekommen in welcher Zeitspanne sich die
Antwortzeiten der von *libhugin harvest* verwendeten Quellen bewegt wurde eine
Messung mit 20 Durchläufen und 10 Filmen durchgeführt. Zum Herunterladen der
Daten wurde von *libhugin* verwendete Bibliothek *http2lib* verwendet. Für die
Anfragen wurde jeweils die Suche nach den genannten Filmen gestartet und das
Suchanfrage--Response heruntergeladen. Für die Messung wurde eine VDSL Anbindung
mit 50Mbit (downstream) / 10Mbit (upstream) verwendet. Abbildung
:num:`fig-site-response-time` zeigt die Antwortzeiten der verschiedenen
Onlinequellen. Für die Messung wurde das Script aus Anhang X verwendet.

.. _fig-site-response-time:

.. figure:: fig/source_response_time.pdf
    :alt: Antwortzeit der aktuell im Prototyp verwendeten Onlinequellen.
    :width: 100%
    :align: center

    Antwortzeit der aktuell im Prototyp verwendeten Onlinequellen.

Die Antwortzeiten bewegen sich im je nach Quelle zwischen 100ms und 450ms. Dies
sind die Antwortzeiten für jeweils eine Suchanfrage. Die Suche nach einem Film
über den Titel benötigt in der Regel mindestens zwei Anfragen --- Eine
Suchanfrage und eine Anfrage um die Metadaten für den gefundenen Film herunter
zu laden.
