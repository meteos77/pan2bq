#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan2bq_gui convertit un fichier unimarc en csv pour BiblioteQ

version 1.0 2023-07-30
Outil GUI pour convertir fichier unimarc en csv.
Permet de visualiser les notices unimarc.
version i18n : fr_FR en argument pour interface en français.

dépendance Modules
pymarc
pyqt5

dépendance paquet Debian
yaz (outil yaz-marcdump pour convertion en utf8)
"""

import os
from pathlib import Path
import sys

from PyQt5 import QtWidgets
from PyQt5.Qt import QDir
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.uic import loadUi


sys.path.insert(0, './fonctions')
from convertyazmarcdump import convertiso5426toutf8
from fonctionsgenerales import comptenbrenotice
from fonctionsgenerales import generatecsv
from fonctionsgenerales import testencodageutf8
from fonctionsgenerales import testtypefichier
from fonctionsui import recuperation_notice_complete


DEBUG = 0 # mettre 1 au lieu de 0 pour activer
VERBEUX = 0 # mettre 1 au lieu de 0 pour activer



repertoiretravailpan = ""
repertoiretravailcsv = ""
#repertoiretravailpan = os.environ['REPERTOIRETRAVAILPAN']
#repertoiretravailcsv = os.environ['REPERTOIRETRAVAILCSV']

class EcranAide(QDialog):
    """Affichage ecran Aide"""
    def __init__(self):
        super().__init__()
#        super(EcranAide,self).__init__()
        #loadUi("UI/BQimport_unimarc_aide.ui",self)
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        loadUi(bundle_dir / 'UI/BQimport_unimarc_aide.ui', self)

class MainWindow(QDialog):
    """ Fenêtre principale. """
    def __init__(self):
        super().__init__()
        #super(MainWindow, self).__init__()
############################################
        # loadUi(bundle_dir / 'BQimport_unimarc.ui', self) # ligne orignale
        # pour faire un pyinstaller --onifile
        # This checks whether the sys._MEIPASS attribute exists
        # (i.e. are we running the bundled executable?),
        # if not, we fall back to the location of the script.
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
############################################
        loadUi(bundle_dir / 'UI/BQimport_unimarc.ui', self)

       # Partie aide (fichier UI externe)
        self.bouton_aide.clicked.connect(self.aide)

        # Partie pour les selecteurs de fichier.
        self.bouton_browsecsv.clicked.connect(self.browsefilescsv)
        self.bouton_browseunimarc.clicked.connect(self.browsefilesunimarc)

        # Entrée manuelle avec bouton retour -> mise à jour de l'écran.
        self.lineEdit_num_notice.returnPressed.connect(self.recuperation_notice_numerosurretour)
        # Si le Slider est touché
        self.slider_noticenum.setSingleStep(1)
        self.slider_noticenum.valueChanged.connect(self.recuperation_notice_numero,\
                                                   int(self.slider_noticenum.value()))

        # Pour générer le fichier .csv.
        self.bouton_generate.clicked.connect(self.generate)

        # Pour quitter l'application.
        self.bouton_exit.clicked.connect(self.exitapp)

############ LES FONCTIONS #################
    def affiche_numero_notice(self, num_notice):
        """ Affiche dans l'interface le numéro de notice actuelle. """
        if DEBUG == 1:
            print(num_notice)
        self.lineEdit_num_notice.setText(str(num_notice))

    def aide(self):
        """ affiche un écran d'aide. """
        EcranAide()
        self.ecranaide = EcranAide()
        self.ecranaide.show()
        print("aide : $ yaz-marcdump -f ISO5426 -t UTF-8 -o marc \
                -l 9=97 fichier.pan > fichier.utf8.pan")

    def browsefilescsv(self):
        """ Définir le requesteur fichier csv. """
        QFileDialog.getSaveFileName(self, self.tr('Sauver un fichier en csv\
                                           format BiblioteQ'), repertoiretravailcsv)

    def browsefilesunimarc(self):
        """ Après la séléction d'un fichier le traitement commence. """
        try:
            # Selecteur du fichier Unimarc.
            fname = QFileDialog.getOpenFileName(self, self.tr('Ouvrir un fichier unimarc'), QDir.homePath() + "/Bureau", "*.pan")
            self.lineEdit_unimarc.setText(fname[0])
            sourcefile = fname[0]

            """ Test type du fichier MARC21 ? """
            marc21 = testtypefichier(sourcefile)
            print(marc21)

            """ Test encodage du fichier utf8 ? """
            charencoding = testencodageutf8(sourcefile)
            if charencoding == "utf-8":
                sourcefileutf8 = sourcefile
            else:
                """ Appel de la fonction de conversion ISO5426 si pas utf8 detecté par chardet. """
                print("Encodage est en : " + charencoding)
                destinationfiletmp = sourcefile + ".tmp"
                convertiso5426toutf8(sourcefile, destinationfiletmp)
                sourcefileutf8 = destinationfiletmp
                self.lineEdit_unimarc.setText(sourcefileutf8)

            # Compter nbre notices.
            print("Appel comptenbrnotice : " + sourcefileutf8)
            retouranalyse_int = comptenbrenotice(sourcefileutf8)
            retouranalyse_str = str(retouranalyse_int)
            print(retouranalyse_str)

            # Affichage dans la case du nombre de notices
            self.lineEdit_resultatanalyse.setText(retouranalyse_str)

            # mise à jour du min et max du slider.
            self.slider_noticenum.setMinimum(1)
            self.slider_noticenum.setMaximum(retouranalyse_int)

           # Indique le nom du fichier de sortie.
            dname = str(fname[0]+".csv")
            self.lineEdit_csv.setText(dname)
            # Place la notice numero 1
            self.lineEdit_num_notice.setText("1")
            return
#            return sourcefileutf8
        except (RuntimeError,TypeError, ValueError, NameError):
            pass

    def recuperation_notice_numerosurretour(self):
        """ Mise à jour du slider si entrée par clavier touche retour. """
        num_notice = self.lineEdit_num_notice.text()
        print(type(num_notice))
        num_notice = int(num_notice)
        self.slider_noticenum.setValue(num_notice)

    def recuperation_notice_numero(self,notice_num):
        """ affichage de la notice """
        notice_num = int(notice_num)
        sourcefileutf8 = str(self.lineEdit_unimarc.text())
        if VERBEUX == 1:
            print("le fichier unimarc est :" + str(sourcefileutf8))
            print("le numero de notice est :" + str(notice_num))
            #fi
        self.lineEdit_num_notice.setText(str(notice_num))
        # Appel de la fonction pour recuperer la notice dans le fichier
        notice_resultat = recuperation_notice_complete(sourcefileutf8, notice_num)
        # mise a jour de l'interface avec la notice
        self.textEdit_resultatnoticenum.setText(str(notice_resultat))


    def exitapp(self):
        """ fonction pour quitter l'application """
        print("convertir si besoins le fichier csv obtenu avec la commande suivante")
        print("uconv -f utf-8 -t utf-8 -x nfc source_file.csv -o destination_file.csv")
        app.quit()

    def generate(self):
        """ fonction pour générer le fichier csv pour l'import dans BQ. """
        sourcefile = self.lineEdit_unimarc.text()
        destinationfile = self.lineEdit_csv.text()
        originaly = self.lineEdit_origine.text()
        numeroacces = self.lineEdit_numeroacces.text()
        valide_originaly = ""
        valide_numeroacces = ""

        if originaly:
            valide_originaly = "ok"
        else:
            print(self.tr("Pas d'origine spécifiée - Merci de compléter."))
            QMessageBox.warning(self,self.tr("Attention"),self.tr("L'origine des livres n'est pas spécifiée"))
        if numeroacces:
            valide_numeroacces = "ok"
        else:
            print(self.tr("Pas de numero d'acces spécifié - Merci de compléter."))
            QMessageBox.warning(self,self.tr("Attention"),self.tr("Le numéro d'accès n'est pas spécifié"))

        if valide_originaly == "ok" and valide_numeroacces == "ok":
            retourgenerate = generatecsv(sourcefile, destinationfile,originaly,numeroacces)
            self.lineEdit_resultatgenerate.setText(retourgenerate)
        else:
            print(self.tr("Erreur Merci de vérifier les données entrées."))
            QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées."))

app = QApplication(sys.argv)

## Debut TRADUCTIONapp = QApplication
locale = QLocale()
translators = []
for prefixeQm in ("Translations/monapplication_", "Translations/qt_", "Translations/qtbase_"):
    translator = QTranslator()
    translators.append(translator)
    translator.load(locale,prefixeQm)
    app.installTranslator(translator)
# Fin TRADUCTION

mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(870)
widget.setFixedHeight(700)
widget.show()
rc = app.exec_()
sys.exit(rc)
