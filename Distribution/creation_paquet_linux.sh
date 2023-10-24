#!/bin/bash
chemin=`pwd`
echo "le chemin est $chemin"
pyinstaller \
--onefile \
--clean \
--path=$chemin/../fonctions \
--add-data ../UI/BQimport_unimarc.ui:UI \
--add-data ../UI/BQimport_unimarc_aide.ui:UI \
--add-binary ../Tools/yaz-marcdump:Tools \
--add-data ../fonctions/fonctionsgenerales.py:fonctions \
--add-data ../fonctions/fonctionunimarcfr.py:fonctions \
--add-data ../fonctions/convertyazmarcdump.py:fonctions \
--add-data ../fonctions/fonctionunimarcfr.py:fonctions \
--add-data ../fonctions/fonctionsui.py:fonctions \
--add-data ../fonctions/fonctionlocationgenre_995k.py:fonctions \
../pan2bq_gui.py
