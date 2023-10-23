I'm not a developer, so there's no guarantee that it will work for you.
Je ne suis pas développeur donc aucune garantie que cela fonctionne bien chez vous.

------------------------------------------------------------
### Merci à "Textbrowser" pour son superbe logiciel de gestion de bibliothèque : BiblioteQ.
------------------------------------------------------------
## pan2bq est un outil pour transformer les fichiers unimarc (.pan) vers un fichier au format csv (.csv) importable dans BiblioteQ.


###il prend en compte les formats
- Unimarc 2709 encodé en ISO5426.
- Unimarc 2709 encodé en utf8.


------------------------------------------------------------

##Installation testé sur LinuxMint21.2


* ### paquets .deb à installer avec apt-get
  * - python3.11
  * - yaz-marcdump (apt-get install yaz) - permet de convertir le fichier unimarc si non utf8.

* ### modules python à installer
  * - csv.
  * - os.
  * - sys.
  * - chardet 3.0.4 # pour vérifier l'encodage du fichier (utf8).
  * - isbnlib 3.10.14 (pip install isbnlib)
  * - pathlib 0.4.16 # pour vérifier l'encodage du fichier (utf8).
  * - pymarc 4.2.2 (pip install pymarc==4.2.2).
  * - python-magic 0.4.16 # pour vérifier si fichier est en MARC21.
  * - PyQt5 5.14.1 (pip install PyQt5).
  * - unidecode 1.1.1 .
------------------------------------------------------------
## Description

* - Le format du fichier csv est adapté pour l'importation via l'import csv de BiblioteQ (modele 1).
* - Place les données du fichier unimarc dans les champs de BiblioteQ.
* - Certains champs 995 (spécifiques à l'échange de données entre bibliothèque française) sont traités.
* - Voir le fichier fonctions/fonctionunimarcfr.py pour les transformations


* - Demande de renseigner l'origine des livres et le place dans le champs origine(originality - enumeration)
* - Demande de renseigner le numero d'acces
    * - si 0 alors prend l'information dans 995$f
    * - prend le numéro spécifié est ajoute +1
* - Le nom du fichier destination est par défaut le nom du fichier source + .csv
------------------------------------------------------------
## Détail de la transformation unimarc vers csv (champs de la base de données de BiblioteQ)
* - 003   : Identifiant ark (alternate_id_1).
* - 010$a : isbn13 ou isbn10 (isbn13 ou id) - convertion des isbn13 978 en isbn10 pour champ id.
* - 010$b : Type de reliure (binding_type).
* - 010$d : Prix et Unité monétaire (price & monetary_units).
* - 101$a : Langue (language).
* - 200$a : Titre (title).
* - 210$a : Lieu d'édition (place).
* - 210$c : Éditeur (publisher).
* - 210$d : Date d'édition (pdate).
* - 214$a : Lieu d'édition (place).
* - 214$c : Éditeur (publisher).
* - 214$d : Date d'édition (pdate).
* - 215$a : Description physique (lccontrol_number) - pas de champ dédié à la description physique dans BiblioteQ.
* - 225$v : Numéro de volume (volume_number).
* - 330$a : Résumé du document (desccription)
* - 333$a : Public cible (target_audience).
* - 461$v : Numéro de volume (volume_number).
* - 606$a : Catégorie du document (category).
* - 700$a : Nom de l'auteur (author).
* - 770$b : Prénom de l'auteur (author).
* - 995$a : Numéro d'accès (accession_number).
* - 995$f : Numéro Dewey (deweynumber & callnumber). 
* - 995$j : Public cible (target_audience).
* - 995$k : Numéro Dewey (deweynumber & callnumber). 
* - 995$m : Date de prêt BDP (purchase_date).
* - 995$n : Date de retour BDP (date_of_reform).
-----------------------------------------------------------
