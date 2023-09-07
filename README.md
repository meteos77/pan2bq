Version 1.0
Date : 2023-06-08

sudo apt-get install yaz
sudo apt-get install python3-pip

pip install isbnlib
pip install pyqt5
pip install -Iv pymarc==4.2.2
pip install unicodedata



Répertoire UI -> répertoire qui contient les pages graphiques
    BQimport_unimarc.ui
    BQimport_unimarc_aide.ui
    BQimport_unimarc_erreur.ui

Répertoire Icons -> icône pour application
    biblioteq-pan2bq

Répertoire fonctions
    convertyazmarcdump.py   -> pour convertir fichier iso2709 (iso5426) en iso2709 utf8 (pour fonctionnement avec pymarc 4.2.2)
        def convertiso5426toutf8(sourcefile, destinationfile):

    fonctionLocationGenre_995k.py   -> l'indice Dewey + Classement BDP 
        def generateTraduction(location_genre_source):

    fonctionsGerenales  -> Regroupe les fonctions utilisées par pan2bq_cli.py et pan2bq_gui.py
        def compteNbreNotice(sourcefileutf8):
        def generateCsv(sourcefileutf8, destinationfile,originaly,numeroacces):
        def testencodageutf8(sourcefile):
        def testtypefichier(sourcefile):
        def convertiso5426toutf8(sourcefile): (NE FONCTIONNE PAS) - pour ne pas utiliser l'outil yaz-marcdump

    fonctionsUI.py
        def recuperation_notice_complete(sourcefileutf8, notice_num):

    fonctionUniMarcFr.py
        def analyseurUniMarcFr(notice,originaly,numeroacces):
