.. raw:: latex

   \appendix

.. _ref-attachment-a:

Helferfunktion für NFO-Dateien
==============================

Folgender Anhang zeigt die import/export-Helferfunktion die von
*libhugin--analyze* als Schnittstelle zu den XBMC Metadaten
verwendet wird:


.. code-block:: python

    #!/usr/bin/env python
    # encoding: utf-8

    import os
    import glob
    import xmltodict


    def attr_mapping():
    return {
        'title': 'title', 'originaltitle': 'originaltitle', 'year': 'year',
        'plot': 'plot', 'director': 'director', 'genre': 'genre'
    }


    ##############################################################################
    # -------------------------- import functions --------------------------------
    ##############################################################################
    def attr_import_func(nfo_file, mask):
    try:
        with open(nfo_file, 'r') as f:
            xml = xmltodict.parse(f.read())
            attributes = {key: None for key in mask.keys()}
            for key, filekey in mask.items():
                attributes[key] = xml['movie'][filekey]
            return attributes
    except Exception as e:
        print('Exception', e)


    def data_import(path):
    metadata = []
    for moviefolder in os.listdir(path):
        full_movie_path = os.path.join(path, moviefolder)
        nfofile = glob.glob1(full_movie_path, '*.nfo')
        if nfofile == []:
            nfofile = full_movie_path
        else:
            nfofile = os.path.join(full_movie_path, nfofile.pop())
        metadata.append(nfofile)
    return metadata


    ##############################################################################
    # -------------------------- export functions --------------------------------
    ##############################################################################
    def attr_export_func(movie):
    mask = attr_mapping()
    print(movie.nfo)
    with open(movie.nfo, 'r') as f:
        xml = xmltodict.parse(f.read())
        for key, filekey in mask.items():
            xml['movie'][filekey] = movie.attributes[key]
        with open(movie.nfo, 'w') as f:
            f.write(xmltodict.unparse(xml, pretty=True))


    def data_export(metadata_dict):
    for movie in metadata_dict:
        attr_export_func(movie)

.. _ref-xbmc-libhugin:

XBMC  Scraper Plugin
====================

Folgender Quelltext zeigt die Implementierung des XBMC Plugins. Als
externe Schnittstelle wird hier der libhugin proxy (siehe
:ref:`ref-flaskproxy`) verwendet.

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <scraper framework="1.1" date="2010-02-22">
    <NfoUrl dest="3">
        <RegExp input="$$1" output="\1" dest="3">
            <expression></expression>
        </RegExp>
    </NfoUrl>
    <CreateSearchUrl dest="3">
    <RegExp input="$$1" output="&lt;url&gt;http://localhost:5000/search/\1&lt;/url&gt;" dest="3">
            <expression></expression>
        </RegExp>
    </CreateSearchUrl>
    <GetSearchResults dest="8">
     <RegExp input="$$5" output="$$1" dest="8">
            <expression></expression>
        </RegExp>
    </GetSearchResults>
    <GetDetails dest="3">
        <RegExp input="$$1" output="$$1" dest="3">
            <expression></expression>
        </RegExp>
    </GetDetails>
    </scraper>


.. _ref-flaskproxy:

Libhugin XBMC Proxy
===================

Folgender Quelltext zeigt die Implementierung des libhugin Proxy--Servers,
welcher das XBMC Plugin mit Daten versorgt.

.. code-block:: python

    #!/usr/bin/env python
    # encoding: utf-8

    # stdlib
    import re

    # 3rd party libs
    from flask import Flask
    from flask import Response
    from flask import request

    # hugin
    import hugin.harvest.session as HarvestSession
    import hugin.analyze.session as AnalyzerSession


    SESSION = HarvestSession.Session()
    ANALYZER = AnalyzerSession.Session('/tmp/dummydbforanalyzer')

    POSTPROCESSING = False
    CACHE = {}

    app = Flask(__name__)


    ##############################################################################
    # -------------------------- flask functions ---------------------------------
    ##############################################################################

    @app.route('/search/<title>')
    def search(title):
        imdbid = re.findall('tt\d+', title)
        # search by imdbid
        if imdbid:
            query = SESSION.create_query(
                imdbid=imdbid.pop(), providers=['tmdbmovie'], language='de'
            )
        else:
        # search by title
            query = SESSION.create_query(
                title=str(title), fuzzysearch=True,
                providers=['tmdbmovie'], language='de'
            )
        results = SESSION.submit(query)
        template = _read_template('tools/huginproxy/results.xml')
        return Response(
            template.format(results=_build_search_results(results)),
            mimetype='text/xml')


    @app.route('/movie/<num>')
    def get_movie(num):
        """ Get movie with a specific number. """
        if CACHE:
            result = CACHE[int(num)]
            if POSTPROCESSING:
                postprocess(result)
            nfo_converter = SESSION.converter_plugins('nfo')
            nfo_file = nfo_converter.convert(result)
            return Response(nfo_file, mimetype='text/xml')
        return Response('Cache is empty.', mimetype='text')


    @app.route('/stats')
    def stats():
        response = 'Postprocessor enabled: {}\nResults in queue: {}'.format(
            POSTPROCESSING,
            len(CACHE)
        )
        return Response(response, mimetype='text')


    @app.route('/toggle_pp')
    def toggle_pp():
        try:
            global POSTPROCESSING
            POSTPROCESSING = not POSTPROCESSING
        except Exception as e:
            print(e)
        return 'Postprocessor enabled: {}'.format(POSTPROCESSING)


    @app.route('/shutdown')
    def shutdown():
        print('Shutting down hugin...')
        SESSION.cancel()
        SESSION.clean_up()
        ANALYZER.database_shutdown()
        print('Shutting down server...')
        shutdown_server()


    ##############################################################################
    # -------------------------- helper functions --------------------------------
    ##############################################################################

    def _build_search_results(results):
        enities = []
        CACHE.clear()
        for num, result in enumerate(results):
            template = _read_template('tools/huginproxy/result_enity.xml')
            enities.append(
                template.format(
                    title=result._result_dict['title'],
                    year=result._result_dict['year'],
                    imdbid=result._result_dict['imdbid'],
                    provider=result._provider.name,
                    nr=num
                )
            )
            CACHE[num] = result
        return ''.join(enities)


    def postprocess(result):
        """ Postprocess example. """
        plotcleaner = ANALYZER.modifier_plugins('plot')
        result._result_dict['plot'] = ANALYZER.modify_raw(
            plotcleaner, 'plot', result._result_dict['plot']
        )


    def _read_template(template):
        """ Helper for reading templates. """
        with open(template, 'r') as file:
            return file.read()


    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('No werkzeug server running.')
        func()

    if __name__ == "__main__":
        app.run()


.. _ref-cloc:

Projektstatistik (*cloc*)
========================

Folgend eine Projektstatistik erstellt mit dem Tool *cloc*:

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
