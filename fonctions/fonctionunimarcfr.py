# -*- coding: utf-8 -*-

__authors__ = "meteos77"
__contact__ = ""
__copyright__ = "2023-11-09"
__version_ = "2.0.2"
"""
Transforme le fichier de la BDP ISO-2709 encoding utf-8
           en fichier .csv pour importation dans BiblioteQ.

encoding entrée : utf8
encoding sortie : utf8 normalize('NFC'
 La forme normale C (NFC) applique d'abord la décomposition canonique, puis compose à nouveau les caractères pré-combinés.


version 2.0.2 : target_audience
version 2.0.1 : dewey
version 2.0 :
fonction analyseurMarcFr pour analyser fichier unimarc ISO2709 de la BDP

# permet de récuperer les informations des notices unimarc et les placer dans
# les variables définies pour le logiciel BiblioteQ (importation csv - modèle 1)
#
Version 1.6
995 $m : date d'achat -> '
995 $n : date de réforme ->
Decomposition de origine (originality pop up : LIB-2022) en origine (Librairie)
ajout de
my_date_of_reform,
my_origin,
my_purchase_date,
alternative_id_1 = n'accepte que des ark:/
pour les champs sans information = "" et plus de commentaire.



"""


import re
import fonctionlocationgenre_995k
from isbnlib import to_isbn10, to_isbn13, canonical
from unicodedata import normalize

def analyseurunimarcfr(notice,originaly,numeroacces):
## les variables
    originaly = originaly.upper()

# target_audience # voir unimarc 333$a ou 995$j (moins précis)
# 0-3 ans
# A partir de 1 ans
# A partir de 2 ans
# A partir de 3 ans
# A partir de 4 ans
# A partir de 5 ans
# A partir de 6 ans
# A partir de 7 ans
# 3-6 ans
# 6-9 ans
# 9-12 ans
# 12 ans et +
# Ados
# Tout public
# Professionnels
# Tous niveaux
# Adultes & ados

#    global my_target_audience
    my_target_audience=""
    my_target_audience_temp=""
    if len(my_target_audience)==0:
        for field in notice.get_fields('333'):
            if field['a'] is not None:
                my_target_audience_temp = field['a']
                my_target_audience = normalize('NFC', str(my_target_audience_temp))


# si my_target_audience est vide alors passer par le champs 995 $j
    if len(my_target_audience)==0:
        for field in notice.get_fields('995'):
            if field['j'] is not None:
                my_target_audience_abrev = field['j']
                if (my_target_audience_abrev == "a"):
                    my_target_audience_temp = "Adultes"
                elif (my_target_audience_abrev == "b"):
                    my_target_audience_temp = "Jeunesse"
                elif (my_target_audience_abrev == "c"):
                    my_target_audience_temp = "Jeunesse"
                elif (my_target_audience_abrev == "u"):
                    my_target_audience_temp = ""
                elif field['j'] is None:
                    my_target_audience_temp = ""
                else:
                    my_target_audience_temp = ""
                pass
    my_target_audience = my_target_audience_temp
    if len(my_target_audience)==0:
        my_target_audience_temp = ""
    my_target_audience = normalize('NFC', str(my_target_audience_temp))



    # accession_number
    # Regarde le champ 995$f ; si rien alors prend le paramètre spécifié.
    my_accessionnumber = ""
    my_accessionnumber_temp = ""
    for field in notice.get_fields('995'):
        if field['f'] is not None:
            my_accessionnumber_temp = field['f']
            my_accessionnumber = normalize('NFC', my_accessionnumber_temp)

    if len(my_accessionnumber)==0:
        my_accessionnumber_temp = ""
        my_accessionnumber_temp = str(numeroacces)
        my_accessionnumber = normalize('NFC', my_accessionnumber_temp)



# alternative_id (ark)
#    global my_alternate_id_1
    my_alternate_id_1 = ""
    my_alternate_id_1_temp = ""
    for field in notice.get_fields('003'):
        if field is not None:
            my_alternate_id_1_temp = field
            my_alternate_id_1_temp = str(my_alternate_id_1_temp)
            # permet de ne garder que la partiea ark

            # exemple
            # str = "Welcome to WayToLearnX."
            # Vérifier si la sous-chaine se trouve dans la chaine principale
            # if "WayToLearnX" in str:
            #    print ('Sous-chaîne trouvée')
            #else:
            #    print('Sous-chaîne non trouvée')
            if "ark:/" in my_alternate_id_1_temp:
                (my_adresse,my_alternate_id_1_temp2) = my_alternate_id_1_temp.split('.fr/')
                my_alternate_id_1 = normalize('NFC', my_alternate_id_1_temp2)
            else:
                my_alternate_id_1 = ""
        #elif field is None:
         #   my_alternate_id_1 = ""
        else:
            my_alternate_id_1 = ""
            pass

# author 700$a et 700$b
#    global my_author
    my_author=""
    my_author_temp=""
    authorNom=""
    authorNom_temp=""
    authorPrenom=""
    authorPrenom_temp=""

    for field in notice.get_fields('700'):
# Nom
        if field['a'] is not None:
            authorNom_temp = field['a']
            authorNom_temp = authorNom_temp.upper()
            authorNOM = normalize('NFC', authorNom_temp)
        elif field['a'] is None:
            authorNom = ""
        else:
            authorNom = ""
            pass

    for field in notice.get_fields('700'):
# Prenom
        if field['b'] is not None:
            authorPrenom_temp = field['b']
            authorPrenom = normalize('NFC', authorPrenom_temp)
        elif field['b'] is None:
            authorPrenom = ""
        else:
            authorPrenom = ""
            pass
        my_author = (authorNOM) + " " + (authorPrenom)

    # si le 700$a et 700$b sont vide alors my_author sera vide => aller voir dans 200$f
    if len(my_author) == 0:
        for field in notice.get_fields('200'):
            if field['f'] is not None:
                my_author_temp = field['f']
                my_author = normalize('NFC', my_author_temp)

# binding_type
#    global my_binding_type
    my_binding_type=""
    for field in notice.get_fields('010'):
        if field['b'] is not None:
            my_binding_typeQ = field['b']
            if my_binding_typeQ == "br. sous jaquette":
                my_binding_type = "Broché sous jaquette"
            if my_binding_typeQ == "br.":
                my_binding_type = "Broché"
            if my_binding_typeQ == "rel. à spirale":
                my_binding_type = "Relié à spirale"
            if my_binding_typeQ == "rel. sous etui":
                my_binding_type = "Relié sous étui"
            if my_binding_typeQ == "rel. dans une boîte":
                my_binding_type = "Relié dans une boîte"
            if my_binding_typeQ == "rel.":
                my_binding_type = "Relié"
            if my_binding_typeQ == "rel":
                my_binding_type = "Relié"
            if my_binding_typeQ == "Rel.":
                my_binding_type = "Relié"
            if my_binding_typeQ == "cart.":
                my_binding_type = "Cartonné"
            if my_binding_typeQ == "Cart.":
                my_binding_type = "Cartonné"
            if my_binding_typeQ == "poche":
                my_binding_type = "Poche"
            if my_binding_typeQ == "Poche":
                my_binding_type = "Poche"
            if my_binding_typeQ == "rectifié":
                my_binding_type = "Rectifié"
            if my_binding_typeQ == "spirale":
                my_binding_type = "Spirale"
            if my_binding_typeQ == "Spirale":
                my_binding_type = "Spirale"
            if my_binding_typeQ == "coffret":
                my_binding_type = "Coffret"
            if my_binding_typeQ == "Livre-disque":
                my_binding_type = "Livre disque"

        elif field['b'] is None:
            my_binding_type = ""
        else:
            my_binding_type = ""
            pass
            my_binding_type = ""

# callnumber # cote
    my_callnumber = ""
    my_callnumber_temp = ""
    for field in notice.get_fields('995'):
        if field['k'] is not None:
            my_callnumber_temp = field['k']
            my_callnumber= normalize('NFC', my_callnumber_temp)

# category
    my_category = ""
    my_category_temp = ""
    my_category_temp2 = []
    rec_606s = notice.get_fields('606')
    for rec_606 in rec_606s:
        for sub_a in rec_606.get_subfields('a'):
            my_category_temp = sub_a
            my_category_temp = normalize('NFC', my_category_temp)
            my_category_temp2.append(my_category_temp)
            my_category = '<br>'.join(my_category_temp2)
            print(my_category)


# condition
# IDEE : si achat de l'année mettre Neuf
    my_condition = "Inconnue"

# description
    my_description = ""
    my_description_temp = ""
    for field in notice.get_fields('330'):
        if field['a'] is not None:
            my_description_temp = field['a']
            my_description = normalize('NFC', my_description_temp)
        elif field['a'] is None:
            my_description = ""
        else:
            pass

# date_of_reform
#Fichier de la BDP -> 995$n = pas actif pour le moment sauf recup WEB.
# voir purchase_date car calcul + 1 an
# si fichier BDP provenant du WEB (pas de mail)
    my_date_of_reform_temp = ""
    my_date_of_reform = ""
    if "BDP-" in originaly:
        for field in notice.get_fields('995'):
            if field['n'] is not None:
                my_date_of_reform_temp = field['n']
                my_date_of_reform = normalize('NFC', my_date_of_reform_temp)
#                print("Date de retour prevue format FR : " + my_date_of_reform)#
                if "BDP-" in originaly:
                    my_date_of_reform_AAAA = my_date_of_reform [0:4]
                    my_date_of_reform_MM = my_date_of_reform [4:6]
                    my_date_of_reform_JJ = my_date_of_reform [6:8]
                    my_date_of_reform = str(my_date_of_reform_MM + "/" + my_date_of_reform_JJ + "/" + my_date_of_reform_AAAA)
#                    print("dateAAAA" + my_date_of_reform_AAAA)
#                    print("dateMM" + my_date_of_reform_MM)#
#                    print("dateJJ" + my_date_of_reform_JJ)
                    print("Date de retour pour BQ : " + my_date_of_reform)

# deweynumber
    my_deweynumber = ""
    my_deweynumber_tempo = ""
    for field in notice.get_fields('676'):
            if field['a'] is not None:
                my_deweynumber_tempo = field['a']
                my_deweynumber = normalize('NFC', my_deweynumber_tempo)

# edition
    my_edition = 1

# id ou isbn13
    my_isbn10 = ""
    my_isbn13 = ""
    for field in notice.get_fields('010'):
        if field['a'] is not None:
            isbn = field['a']
            # supprime les -
            isbn = canonical(isbn)
            if isbn.startswith("978"):
                my_isbn13 = isbn
                my_isbn10 = to_isbn10(my_isbn13) # conversion
            elif isbn.startswith("979"):
                my_isbn13 = isbn
                my_isbn10 = ""                   # pas de conversion possible
            elif isbn.startswith("2"):
                my_isbn10 = isbn
                my_isbn13 = to_isbn13(my_isbn10) # conversion
            elif field['a'] is None:
                my_isbn10 = ""
                my_isbn13 = ""
            else:
                pass
# keyword
    my_keyword = ""

# language
    my_language = ""
    my_language_temp = ""
    for field in notice.get_fields('101'):
        if field['a'] is not None:
            my_language_temp = field['a']
            if my_language_temp == "fre":
                my_language_temp = "Français"
                my_language = normalize('NFC', my_language_temp)

        elif field['a'] is None:
            my_language = "Français"
        else:
            my_language = "Français"
            pass
            my_language = "Français"

# lccontrolnumber
    my_lccontrolnumber = ""
    my_lccontrolnumber_temp = ""
    for field in notice.get_fields('215'):
        try:
            if field['a'] is not None:
                my_lccontrolnumber_a = field['a']
                if field['c'] is not None:
                    my_lccontrolnumber_c = field['c']
                    if field['d'] is not None:
                        my_lccontrolnumber_d = field['d']
                        my_lccontrolnumber_temp = my_lccontrolnumber_a + " ; " + my_lccontrolnumber_c + " ; " + my_lccontrolnumber_d
                        my_lccontrolnumber = normalize('NFC', my_lccontrolnumber_temp)
            else:
                my_lccontrolnumber = ""
        except:
            pass


# location
    my_location=""
    my_location_temp=""
    if "BDP-" in originaly:
        print("995$k pour la location")
        for field in notice.get_fields('995'):
            if field['k'] is not None:
                my_deweynumber_temp = field['k']
                my_location_temp = my_deweynumber_temp[0:2]
                if( my_location_temp.isdigit()):
                    my_location_temp = my_deweynumber_temp[0:1]
                    my_location_temp = my_location_temp.replace(" ", "")
                    if( my_target_audience == "Jeunesse"):
                        my_location_temp="E" + my_location_temp

                    my_location_temp2 = fonctionlocationgenre_995k.generatetraduction(my_location_temp)
                    my_location = normalize('NFC', my_location_temp2)
                else:
                    my_location_temp = my_deweynumber_temp[0:2]
                    my_location_temp = my_location_temp.replace(" ", "")
                    my_location_temp2 = fonctionlocationgenre_995k.generatetraduction(my_location_temp)
                    my_location = normalize('NFC', my_location_temp2)
            elif field['k'] is None:
                my_location = ""





# marc_tags
    my_marc_tags = ""
#    my_marc_tags_temp = ""
#    for field in notice.get_fields():
#        if field is not None:
#            my_marc_tags_temp = str(field)
#            my_marc_tags = normalize('NFC', my_marc_tags_temp)

# monetary_units and price
# caractère ? en trop N° 62
    my_monetary_units = ""
    my_price = ""
    price_temp = ""
    priceandmonetary_temp = ""
    for field in notice.get_fields('010'):
        if field['d'] is not None:
            priceandmonetary_temp = field['d']
            priceandmonetary_temp = priceandmonetary_temp.upper()
            # NEGARDER QUE LES CARACTERES 0-9 et EUR F
            priceandmonetary = re.sub(r"[^0-9 EURF,.]", "", priceandmonetary_temp)
            # Suppression si double espace
            priceandmonetary = "".join(priceandmonetary.split())
            priceandmonetary = priceandmonetary.replace(",",".")
            try:
                if priceandmonetary.index("EUR"):
                    princeandmonetary =  priceandmonetary.partition("EUR")
                    price_temp = princeandmonetary[0]
                    monetary_units = princeandmonetary[1]
                    try:
                        float(price_temp)
                        my_price = price_temp
                        my_monetary_units = monetary_units
                    except ValueError:
                        print("prix nom numeric : " + my_price)
                        print("monetary_units : " + monetary_units)
            except ValueError:
                try:
                    if priceandmonetary.index("F"):
                        princeandmonetary =  priceandmonetary.partition("F")
#                       print(my_accessionnumber)
#                       print(princeandmonetary)
                        price_temp =  princeandmonetary[0]
                        monetary_units = princeandmonetary[1]
#                        print("Le prix est de : " + price_temp)
#                        print("La monnaie est le : " + monetary_units)
                        try:
                            float(price_temp)
                            my_price = price_temp
                            my_monetary_units = monetary_units
                        except ValueError:
                            print("prix nom numeric : " + my_price)
                            print("monetary_units : " + monetary_units)

                except ValueError:
                    my_price = "0"
                    my_monetary_units = "zero"

# multivolume_set_isbn
    my_multivolume_set_isbn = ""

# origine (Librairie, BDP , Don)
# transformer le champ my_originaly en my_origin
# BDP-2022-12 -> Prêts de la Médiathèque Départementale
# DON-2023 -> Dons des particuliers
# LIB-2022 -> Achats Librairie

    my_origin = ""
    my_origin_temp = ""
    if "BDP-" in originaly:
        my_origin = "Prêts de la Médiathèque Départementale"
    elif "DON-" in originaly:
         my_origin = "Dons des particuliers"
    elif "LIB-" in originaly:
         my_origin = "Achats Librairie"
    else:
        my_origin = "Pas d'origine connue"
#    print(my_origin)


# originaly (la variable est définie dans l'interface de lancement)
    my_originaly = ""
    my_originaly_temp = ""
    my_originaly_temp = originaly
    my_originaly = normalize('NFC', my_originaly_temp)
    my_originaly = my_originaly.upper()

# pdate (unimarc 210 ou 214 a faire)
# a faire supprimer : DL ou impr. avant la date
    my_pdate = ""
    my_pdate210 = ""
    my_pdate214 = ""
    for field in notice.get_fields('210'):
        if field['d'] is not None:
            my_pdate_temp210 = field['d']
            # ne garde que les nombres
            my_pdate210 = "".join([ele for ele in my_pdate_temp210 if ele.isdigit()])
            # ne garde que 4 chiffres
            my_pdate210 = my_pdate210[0:4]
            # ajout de MM/JJ + AAAA
            my_pdate = "01/01/" + my_pdate210

    if len(my_pdate)==0:
        for field in notice.get_fields('214'):
            # print(field)
            if field['d'] is not None:
                my_pdate_temp214 = field['d']
                # ne garde que les nombres
                my_pdate214 = "".join([ele for ele in my_pdate_temp214 if ele.isdigit()])
                 # ne garde que 4 chiffres
                my_pdate210 = my_pdate210[0:4]
                my_pdate214 = "01/01/" + my_pdate214
                my_pdate = my_pdate214
            else:
                my_pdate = "01/01/1900"

# place : 210$a
    global my_place
    my_place_temp=""
    my_place=""
    for field in notice.get_fields('210'):
        if field['a'] is not None:
            my_place_temp = field['a']
            my_place = normalize('NFC', my_place_temp)
        elif field['a'] is None:
            my_place = ""
# place : 214$a
    if len(my_place)==0:
        for field in notice.get_fields('214'):
            if field['a'] is not None:
                my_place_temp = field['a']
                my_place = normalize('NFC', my_place_temp)


# price
# -> déjà traite dans monetary_units


# purchase_date (date achat ou de prêt de la BDP)
# !!!! attention Date AMERICAINE MM/JJ/AAAA 12/31/2023
    my_purchase_date = ""
    my_purchase_date_temp = ""
# Si fichier BDP 995$m -> devrait contenir date de prêt.
# pour le moment pas le cas.
# se base sur le champ originaly (préciser dans l'interface par utilisateur LIB-2022 ou DON-2023 ou BDP-2023-12)
    if "DON-" in originaly:
        my_purchase_date_temp = originaly [4:9]
        my_purchase_date = "01/01/" + my_purchase_date_temp
    elif "LIB-" in originaly:
        my_purchase_date_temp = originaly [4:9]
        my_purchase_date = "01/01/" + my_purchase_date_temp

# si fichier BDP provenant du WEB (pas de mail)
    elif "BDP-" in originaly:
        for field in notice.get_fields('995'):
            if field['m'] is not None:
                my_purchase_date_temp = field['m']
                my_purchase_date = normalize('NFC', my_purchase_date_temp)
#                print("Date de livraison format FR : " + my_purchase_date)#
                if "BDP" in originaly:#
                    my_purchase_date_AAAA = my_purchase_date [0:4]#
                    my_purchase_date_MM = my_purchase_date [4:6]
                    my_purchase_date_JJ = my_purchase_date [6:8]
                    my_purchase_date = str(my_purchase_date_MM + "/" + my_purchase_date_JJ + "/" + my_purchase_date_AAAA)
#                    print("dateAAAA" + my_purchase_date_AAAA)
#                    print("dateMM" + my_purchase_date_MM)#
#                    print("dateJJ" + my_purchase_date_JJ)
                    print("Date de pret pour BQ : " + my_purchase_date)
    else:
        my_purchase_date_AAAA = originaly [4:8]
        my_purchase_date_MM = originaly [9:11]
        my_purchase_date = my_purchase_date_MM + "/01/" + my_purchase_date_AAAA
        # calcul de la date de retour (+ 1an)
        my_purchase_date_AAAA_int = int(my_purchase_date_AAAA)
        my_purchase_date_AAAA_int_ajout = my_purchase_date_AAAA_int + 1
        my_purchase_date_AAAA_int_ajout_str = str(my_purchase_date_AAAA_int_ajout)
        my_date_of_reform = my_purchase_date_MM + "/01/" + my_purchase_date_AAAA_int_ajout_str


# publisher
    my_publisher = ""
    for field in notice.get_fields('210'):
        if field['c'] is not None:
            my_publisher_temp = field['c']
            my_publisher = normalize('NFC', my_publisher_temp)
        elif field['c'] is None:
            my_publisher = ""
    # si la zone 210 est vide alors voir 214
    if len(my_publisher)==0:
        for field in notice.get_fields('214'):
            if field['c'] is not None:
                my_publisher = field['c']
            elif field['c'] is None:
                my_publisher = ""
    
# quantity
    my_quantity = 1

# volume_number
# PB si plusieurs ligne 225
    my_volume_number = ""
    my_volume_number_temp = ""
    try:
        for field in notice.get_fields('225'):
            if field['v'] is not None:
                my_volume_number_temp = field['v']
                my_volume_number = normalize('NFC', my_volume_number_temp)

        if len(my_volume_number)==0:
            for field in notice.get_fields('461'):
                if field['v'] is not None:
                    my_volume_number_temp = field['v']
                    my_volume_number = normalize('NFC', my_volume_number_temp)
    except:
        pass


# title
    my_title_serie = ""
    my_title_serie_temp = ""
    my_title = ""
    my_tilte_temp = ""
    my_title_complet = ""
    for field in notice.get_fields('461'):
        if field['t'] is not None:
            my_title_serie_temp = field['t']
            my_title_serie = " ".join(my_title_serie_temp.split())  # supprime les espaces en trop dans le titre
            if my_title_serie_temp == my_title_serie:
                my_title_serie = normalize('NFC', my_title_serie_temp)

    
    for field in notice.get_fields('200'):
        if field['a'] is not None:
            my_title_temp = field['a']
            my_title = " ".join(my_title_temp.split())  # supprime les espaces en trop dans le titre
            if my_title_temp == my_title:
                my_title = normalize('NFC', my_title_temp)
            else:
                print(my_accessionnumber,my_isbn13,my_title_temp,"->",my_title)
                print(my_title)
        elif field['a'] is None:
            print('Pas de titre')
     
        else:
            my_title = ""
            pass
# verification si il y a un titre de la serie
    if my_title_serie:
        my_title_complet = my_title_serie + ", " + my_volume_number + " : " + my_title
    else:
        my_title_complet = my_title
# url
    my_target_audience_url_temp = ""
    my_url = ""
    for field in notice.get_fields('333'):
        if field['a'] is not None:
            my_target_audience_url_temp = field['a']
            my_url = normalize('NFC', my_target_audience_url_temp)

# volume_number
# PB si plusieurs ligne 225
    my_volume_number = ""
    my_volume_number_temp = ""
    try:
        for field in notice.get_fields('225'):
            if field['v'] is not None:
                my_volume_number_temp = field['v']
                my_volume_number = normalize('NFC', my_volume_number_temp)

        if len(my_volume_number)==0:
            for field in notice.get_fields('461'):
                if field['v'] is not None:
                    my_volume_number_temp = field['v']
                    my_volume_number = normalize('NFC', my_volume_number_temp)
    except:
        pass


    return [my_accessionnumber, my_alternate_id_1, my_author, my_binding_type,
            my_callnumber, my_category, my_condition, my_date_of_reform,
            my_description, my_deweynumber, my_edition, my_isbn10, my_isbn13,
            my_keyword, my_language, my_lccontrolnumber, my_location,
            my_marc_tags, my_monetary_units, my_multivolume_set_isbn, my_origin,
            my_originaly, my_pdate, my_place, my_price, my_publisher,
            my_purchase_date, my_quantity, my_target_audience, my_title_complet, my_url,
            my_volume_number]

# fin de l'AnalyseurUnimarc


if __name__ == "__main__":
    print("impossible d'utilise le module en programme !")
