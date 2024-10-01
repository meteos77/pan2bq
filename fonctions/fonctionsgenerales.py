#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Fonction generateCsv : pour generer le fichier final
Fonction testencodageutf8 : pour tester encodage utf8 ?
Fonction testtypefichier : pour le type de fichier (unimarc : MARC21) ?
version 2023-08-29 : ajout des 3 nouveaux champs
my_date_of_reform,
my_origin,
my_purchase_date,
version 2023-12--31 :
ajout "quoting=csv.QUOTE_ALL" dans csv.writer pour avoir le 039000 au lieu de 39000
"""

import sys
import pathlib # pour vérifier l'encodage du fichier (utf8).
import csv
import magic # pour vérifier si fichier est en MARC21.
import chardet # pour vérifier l'encodage du fichier (utf8).

import pymarc # pour analyse (attention version 4.2.2 de pymarc)

from fonctionunimarcfr import analyseurunimarcfr

VERBEUX = 0

def comptenbrenotice(sourcefileutf8):
    """ Fonction pour compter le nombre de notice. """
#    if VERBEUX == 1:
    print("** Fonction compter le nombre de notice dans le fichier : " + sourcefileutf8)
    print("##############################################")
        # fi
    nbrenotice = 0
    retouranalyse_int=""
    with open(sourcefileutf8, 'rb') as fichierdonnees:
        lecteur = pymarc.MARCReader(fichierdonnees, force_utf8=True, to_unicode=True,\
                                    file_encoding='utf8', utf8_handling='replace')

        for notice in lecteur:
            nbrenotice += 1
    # Fin de l'analyse
    retouranalyse_int = nbrenotice
    if VERBEUX == 1:
        print("Résultat fonction compteNbreNotice : le nombre de notices dans\
               le fichier est de " + str(retouranalyse_int))
    fichierdonnees.close()
    return retouranalyse_int

def generatecsv(sourcefileutf8, destinationfile,originaly,numeroacces):
    """ Fonction qui génére le fichier csv """
    if VERBEUX == 1:
        print("** Fonction generation du fichier csv **")
        print("##############################################")
        print("Début du traitement des notices")
        # fi

    # variables
    notice = ""

    entete = ['accessionnumber', 'alternate_id_1', 'author', 'binding_type',
            'callnumber', 'category', 'condition', 'date_of_reform',
            'description', 'deweynumber', 'edition', 'isbn10', 'isbn13',
            'keyword', 'language', 'lccontrolnumber', 'location',
            'marc_tags', 'monetary_units', 'multivolume_set_isbn', 'origin',
            'originaly', 'pdate', 'place', 'price', 'publisher',
            'purchase_date', 'quantity', 'target_audience', 'title', 'url',
            'volume_number']

    with open(sourcefileutf8, 'rb') as fichierdonnees:
        with open(destinationfile, 'w', newline='', encoding='utf-8') as fichiercsv:
            writer = csv.writer(fichiercsv, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(entete)
            i = -0
            # lecture du fichier BDP et appel de la fonction analyseurUniMarcFr
            # notice contient chaque notice
            # element contient le retour du traitement analyseurUniMarcFr

            lecteur = pymarc.MARCReader(fichierdonnees, force_utf8=True,\
                                        to_unicode=True, file_encoding='utf8',\
                                        utf8_handling='strict')
            for notice in lecteur:
                i += 1
                numeroacces = int(numeroacces)
                numeroacces += 1
                print("_______________________________________________________")
                print("Traitement de la notice numéro : " + str(numeroacces))
                print("_______________________________________________________")
#                elements = (fonctionUniMarcFr.analyseurUniMarcFr(notice,originaly,numeroacces))
                elements = analyseurunimarcfr(notice,originaly,numeroacces)
                writer.writerow(elements)
        fichiercsv.close()

        # affiche le nombre de notices traitées.
        print('Résultat : ' + str(i) + ' notices traitées')
    fichierdonnees.close()
    retourgenerate = 'Résultat : ' + str(i) + ' notices traitées'
    return retourgenerate

def testencodageutf8(sourcefile):
    """ Test de l'encodage. """
    if VERBEUX == 1:
        print("** Fonction Test de l'encodage du fichier (utf8 ?)**")
        # fi
    result = chardet.detect(pathlib.Path(sourcefile).read_bytes())
    charencoding = result['encoding']
    charencodingpourcent = result['confidence']*100
    if VERBEUX == 1:
        print ("l'encodage probable est " + charencoding + " à " + str(charencodingpourcent) + " %")
        print("##########################################################################")
        # fi
    return charencoding

def testtypefichier(sourcefile):
    """ Test du type de fichier. """
    if VERBEUX == 1:
        print("** Fonction Test du type de fichier (MARC21 ?)**")
        # fi
    typedefichier = magic.from_file(sourcefile)

    if typedefichier == "MARC21 Bibliographic":
        if VERBEUX == 1:
            print("Le type de fichier est bien en : " + typedefichier)
            print("##########################################################################")
            # fi
    else:
        print("Le type de fichier est en : " + typedefichier)
        print("Veuillez sélectionner un fichier de type Unimarc - MARC21")
        sys.exit()
        # fi
