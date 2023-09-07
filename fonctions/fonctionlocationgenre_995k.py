#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Transforme la cote abrégée en description. """

import sys

# Genre [Location] champs 995$k
# Permet de définir le genre et dans BiblioteQ la location
# Définition d'un dictionnaire

location_genre = {}
location_genre["0"] = "000-Documentaires Informatique, information, ouvrages généraux"
location_genre["1"] = "100-Documentaires Philosophie, Parapsychologie et Occultisme, Psychologie"
location_genre["2"] = "200-Documentaires Religions"
location_genre["3"] = "300-Documentaires Sciences sociales"
location_genre["4"] = "400-Documentaires Langues[modifier"
location_genre["5"] = "500-Documentaires Sciences de la nature et Mathématiques"
location_genre["6"] = "600-Documentaires Technologie (Sciences appliquées)"
location_genre["7"] = "700-Documentaires Arts, Loisirs et Sports"
location_genre["8"] = "800-Documentaires Littérature (Belles-Lettres) et techniques d’écriture"
location_genre["9"] = "900-Documentaires Géographie, Histoire et disciplines auxiliaires"


### PERSO
location_genre["Inconnu"] = "Location Genre Inconnu"
location_genre["A"] = "A-Albums"
location_genre["B"] = "B-Bibliographies"
location_genre["BD"] = "BDA-Bande Déssinée Adultes"
location_genre["C"] = "C-Contes"
location_genre["H"] = "H-Humour"
location_genre["M"] = "M-Mémoires"
location_genre["N"] = "N-Nouvelles"
location_genre["NA"] = "NA-Nouvelles d'anticipation"
location_genre["NP"] = "NP-Nouvelles policières"
location_genre["O"] = "O-Oeuvres complètes"
location_genre["P"] = "P-Poésies"
location_genre["PL"] = "PL-Première Lecture"
location_genre["R"] = "R-Romans"
location_genre["RA"] = "RA-Romans Anticipation"
location_genre["RP"] = "RP-Romans Policier"
location_genre["T"] = "T-Théatres"
location_genre["E"] = "Jeunesse"
location_genre["EA"] = "EA-Albums Jeunesse"
location_genre["EC"] = "EC-Conte Jeunesse"
location_genre["EB"] = "EBD-Bande Déssinée Jeunesse"
location_genre["ET"] = "ETI-Textes illutrés Jeunesse"
location_genre["ER"] = "ER-Roman Jeunesse"
location_genre["ERA"] = "ERA-Roman Anticipation Jeunesse"
location_genre["E0"] = "E000-Documentaires Jeunesse : Informatique, information, ouvrages généraux"
location_genre["E1"] = "E100-Documentaires Jeunesse : Philosophie, Parapsychologie et Occultisme, Psychologie"
location_genre["E2"] = "E200-Documentaires Jeunesse : Religions"
location_genre["E3"] = "E300-Documentaires Jeunesse : Sciences sociales"
location_genre["E4"] = "E400-Documentaires Jeunesse : Langues"
location_genre["E5"] = "E500-Documentaires Jeunesse : Sciences de la nature et Mathématiques"
location_genre["E6"] = "E600-Documentaires Jeunesse : Technologie (Sciences appliquées)"
location_genre["E7"] = "E700-Documentaires Jeunesse : Arts, Loisirs et Sports"
location_genre["E8"] = "E800-Documentaires Jeunesse : Littérature (Belles-Lettres) et techniques d’écriture"
location_genre["E9"] = "E900-Documentaires Jeunesse : Géographie, Histoire et disciplines auxiliaires"

def generatetraduction(location_genre_source):
    """ Transforme la cote abrégée en description. """
    my_location = ""
    my_location = location_genre.get(location_genre_source, "Pas de valeur")
    return my_location


if __name__ == "__main__":
    my_location = ""
    print("Rappel : mettre l'argument")
    location_genre_source = ""
    location_genre_source = sys.argv[1]
    print(location_genre_source)
    generatetraduction(location_genre_source)
    print(my_location)
