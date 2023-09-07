#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Convertion d'un fichier Unimarc 2709 encodé en ISO5426 en fichier Unimarc 2709 encodé en utf8.
2 arguments : fichier source et fichier destination."""

import os


def convertiso5426toutf8(sourcefile, destinationfile):
    """yaz-marcdump -f ISO5426 -t UTF-8 -o marc $FichierSource > $FichierDestination_1 """

    cmd = "yaz-marcdump -f ISO5426 -t UTF-8 -o marc -l 9=97 %s > %s"%(sourcefile,destinationfile)
    try:
        print("Debut de la convertion par yaz-marcdump")
        os.system(cmd)
        print("la convertion du ficher " + sourcefile + " est faite")
        print("##############################################")
        return
    except FileNotFoundError:
        print("Problème de convertion par yaz-marcdump : pas de fichier")
