:orphan:

.. One big hack.

.. only:: html or singlehtml or singletext

    **Abkürzungsverzeichnis**

.. raw:: latex

    \thispagestyle{plain}
    \renewcommand{\thepage}{\roman{page}}
    \setcounter{page}{8} % cough.
    \addcontentsline{toc}{section}{Abk"urzungsverzeichnis}
    {\centering\Huge \textbf{Abk"urzungsverzeichnis}}

.. figtable::
    :spec: >{\raggedleft\arraybackslash}p{0.25\linewidth} p{0.65\linewidth}

    =======================  ==================================
    Abkürzung                Bedeutung
    =======================  ==================================
    **API**                  *Application Programming Interface*
    **CLI**                  *Command Line Interface*
    **HDTV**                 *High Definition Television*
    **LoC**                  *Lines of Code*
    **XML**                  *Extensible Markup Language*
    =======================  ==================================

.. raw:: latex

    \newpage
    \renewcommand{\thepage}{\arabic{page}}
    \pagestyle{fancy}
    \setcounter{page}{1}
