#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__authors__ = "meteos77"
__contact__ = ""
__copyright__ = "2023-06-07"
__version_ = "1.5"


import sys
sys.path.insert(0, './fonctions')
from convertyazmarcdump import convertiso5426toutf8
from fonctionsgenerales import generatecsv
from fonctionsgenerales import testencodageutf8
from fonctionsgenerales import testtypefichier


if __name__ == "__main__":
    try:
        sourcefile = (sys.argv[1])
        destinationfile = (sys.argv[2])
        originaly =  (sys.argv[3])
        numeroacces = (sys.argv[4])
        print("Traitement de : " + sourcefile + " vers " + destinationfile + " avec paramètres : " + originaly + " et " + numeroacces)
        print("##########################################################################")
        # test si MARC21
        typedefichier = testtypefichier(sourcefile)
        # test si utf8
        charencoding = testencodageutf8(sourcefile)

        if charencoding == "utf-8":
            print(charencoding)
            sourcefileutf8 = sourcefile
        else:
            # Appel de la fonction de conversion ISO5426 si pas utf8 detecté par chardet
            print("Encodage est en : " + charencoding)
            print("Appel a la fonction de conversion yaz-marcdump pour conversion en utf-8")
            destinationfiletmp = sourcefile + ".tmp"
            convertiso5426toutf8(sourcefile, destinationfiletmp)
            sourcefileutf8 = destinationfiletmp

#        print("Appel a la fonction de conversion iso5426")
#        convertiso5426toutf8(sourcefile)

        # Génération du fichier final
        print("Le fichier a convertir en csv : " + sourcefileutf8)
        generatecsv(sourcefileutf8, destinationfile, originaly, numeroacces)

    except IndexError: 
        print("Rappel : mettre 4 argument source et destination et origine")
        print("Rappel : mettre en source le fichier unimarc de la BDP en utf8")
        print("Rappel : mettre en destination le fichier csv")
        print("Rappel : mettre une origine")
        print("Rappel : mettre une numero d'acces")
    except OSError:
        print("Mettre un fichier unimarc en 1er paramètre")
    

