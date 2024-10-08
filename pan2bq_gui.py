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
import time
from PyQt5 import QtWidgets
from PyQt5.Qt import QDir
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.uic import loadUi

#print(sys._MEIPASS)
#time.sleep(9000)


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



def resource_path(relative_path):
    """La doc est ici: https://pyinstaller.org/en/stable/runtime-information.html"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        repertexec = sys._MEIPASS # programme traité par pyinstaller
        return repertexec
    else:
        repertexec = os.path.dirname(os.path.abspath(__file__)) # non traité
        print(repertexec)
        return repertexec




class EcranAide(QDialog):
    """Affichage ecran Aide"""
    def __init__(self):
        super().__init__()
        repertexec = resource_path('/UI/Qimport_unimarc_aide.ui')
        ecran_aide = os.path.join(repertexec, "UI/BQimport_unimarc_aide.ui")
        loadUi(ecran_aide, self)


class MainWindow(QDialog):
    """ Fenêtre principale. """
    def __init__(self):
        super().__init__()
        repertexec = resource_path('/UI/Qimport_unimarc.ui')
        ecranP = os.path.join(repertexec, "UI/BQimport_unimarc.ui")
        loadUi(ecranP, self)

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
        QFileDialog.getSaveFileName(self, self.tr('Sauver un fichier en csv format BiblioteQ'), QDir.homePath() + "/Bureau", "*.csv")


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
            nomfichiersource = str(fname[0])
            if "-2_" in nomfichiersource:
                print("fichier createur")
                nomfichiersourcepartie = nomfichiersource.split("-2_")
                nomfichiersourcepartie1 = nomfichiersourcepartie[0]
                nomfichiersourcepartie2 = nomfichiersourcepartie[1]
                dname = nomfichiersourcepartie1 + "-3_" + nomfichiersourcepartie2 + ".csv"
            else:
                dname = str(fname[0]+".csv")

            print(dname)
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
        originaly = originaly.upper()

        if originaly:
            valide_originaly = "ok"
            originaly = originaly.replace("_","-")
        else:
            print(self.tr("Pas d'origine spécifiée - Merci de compléter."))
            QMessageBox.warning(self,self.tr("Attention"),self.tr("L'origine des livres n'est pas spécifiée"))
        if numeroacces:
            valide_numeroacces = "ok"
        else:
            print(self.tr("Pas de numero d'acces spécifié - Merci de compléter."))
            QMessageBox.warning(self,self.tr("Attention"),self.tr("Le numéro d'accès n'est pas spécifié"))

        print("la variable originaly contient : " + originaly)
        # 2024-06-04 : Ajout vérification "-" au lieu de "_"

        if "BDP" in originaly:
            if numeroacces == "0":
                print("OK BDP avec 0")
                valide_originaly="ok"
                valide_numeroacces="ok"
            else:
                valide_numeroacces = "pb"
                print(self.tr("Erreur Merci de vérifier les données entrées car avec BDP le numero devrait être 0."))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées \n avec BDP le numero devrait être 0."))

        if "BDP" in originaly:
            if len(originaly)==11:
                valide_originaly="ok"
                valide_patron="ok"
            else:
                valide_patron="pb"
                print(self.tr("Erreur Merci de vérifier les données entrées ne correspondent pas au modèle BDP-AAAA-MM"))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées ne correspondent pas au modèle BDP-AAAA-MM"))


        if "LIB" in originaly:
            if numeroacces != "0":
                valide_numeroacces="ok"
                valide_originaly="ok"
            else:
                valide_originaly = "pb"
                print(self.tr("Erreur Merci de vérifier les données entrées car avec LIB le numero devrait être différent de 0."))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées car avec LIB le numero devrait être différent de 0."))

        if "LIB" in originaly:
            if len(originaly)==8:
                valide_originaly="ok"
                valide_patron="ok"
            else:
                valide_patron="pb"
                print(self.tr("Erreur Merci de vérifier les données entrées ne correspondent pas au modèle LIB-AAAA"))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées ne correspondent pas au modèke LIB-AAAA"))


        if "DON" in originaly:
            if numeroacces != "0":
                valide_numeroacces="ok"
                valide_originaly="ok"
            else:
                valide_originaly = "pb"
                print(self.tr("Erreur Merci de vérifier les données entrées car avec DON le numero devrait être différent de 0."))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("MMerci de vérifier les données entrées car avec DON le numero devrait être différent de 0."))

        if "DON" in originaly:
            if len(originaly)==8:
                valide_originaly="ok"
                valide_patron="ok"
            else:
                valide_patron="pb"
                print(self.tr("Erreur Merci de vérifier les données entrées ne correspondent pas au modèle DON-AAAA"))
                QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées ne correspondent pas au modèle DON-AAAA"))


                print(valide_numeroacces)

        if "DON" in originaly or "LIB" in originaly or "BDP" in originaly:
            pass
        else:
            print(self.tr("Erreur l'entrée d'orgine accepte les valeurs DON, LIB ou BDP"))
            QMessageBox.critical(self,self.tr("Attention"),self.tr("Merci de vérifier les données entrées car l'entrée d'orgine accepte les valeurs DON, LIB ou BDP"))
            valide_originaly = "pb"

        # TEST FINAL
        if valide_originaly == "ok" and valide_numeroacces == "ok" and valide_patron == "ok":
            retourgenerate = generatecsv(sourcefile, destinationfile,originaly,numeroacces)
            self.lineEdit_resultatgenerate.setText(retourgenerate)
        else:
            print("probleme a régler")

app = QApplication(sys.argv)
repertexec = resource_path('/Icons/biblioteq-pan2bq.ico')
icone = os.path.join(repertexec, "Icons/biblioteq-pan2bq.ico")
# mettre la même icone pour toutes les fenêtres de l'application
# app.setWindowIcon(QtGui.QIcon(icone))

app.setApplicationDisplayName("PAN2BQ version 2023-10-24")
## Debut TRADUCTIONapp = QApplication
locale = QLocale()
translators = []
for prefixeQm in ("Translations/pan2bq.", "Translations/qt_", "Translations/qtbase_"):
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
