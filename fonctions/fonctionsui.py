#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" fichier qui regroupe les fonctions graphiques. """

import pymarc


def recuperation_notice_complete(sourcefileutf8, notice_num):
    """ fonction qui retourne la notice du numéro founie. """
    notice_resultat = ""
    num = 0
    with open(sourcefileutf8, 'rb') as fichierdonnees:
        lecteur = pymarc.MARCReader(fichierdonnees, force_utf8=True,\
                                    to_unicode=True, file_encoding='utf8',\
                                    utf8_handling='replace')
        for notice in lecteur:
            num += 1
            notice_num = int(notice_num)
            if num  == notice_num:
                notice_resultat = notice
                return notice_resultat


if __name__ == "__main__":
    """ Affiche la notice (numéro) du fichier spécifié. """
    import sys
    sourcefileutf8 = sys.argv[1]
    notice_num = sys.argv[2]
    print("le fichier unimarc utf8 : " + sourcefileutf8)
    print("le numéro de notice demandée : " + notice_num)
    print("#################################################################")
    notice_resultat = recuperation_notice_complete(sourcefileutf8, notice_num)
    print(notice_resultat)
