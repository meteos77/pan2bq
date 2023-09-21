I'm not a developer, so there's no guarantee that it will work for you.


Je ne suis pas développeur donc aucune garantie que cela fonctionne bien chez vous.

------------------------------------------------------------
----------------- testé sur LinuxMint21.2 ------------------

python3.11
yaz-marcdump (apt-get install yaz)


--- modules python a avoir ---
csv
os
sys
chardet 3.0.4 # pour vérifier l'encodage du fichier (utf8).
isbnlib 3.10.14 (pip install isbnlib)

pathlib 0.4.16 # pour vérifier l'encodage du fichier (utf8).
pymarc 4.2.2 (pip install pymarc==4.2.2)
python-magic 0.4.16 # pour vérifier si fichier est en MARC21.
PyQt5 5.14.1 (pip install PyQt5)
unidecode 1.1.1 
------------------------------------------------------------
pan2bq est un outil pour transformer les fichiers unimarc (.pan) vers un fichier au format csv (.csv).

- le format du fichier csv est adapté pour l'importation via l'import csv de BiblioteQ (modele 1).
- place les données du fichier unimarc dans les champs de BiblioteQ.
- certains champs 995 (spécifiques à l'échange de données entre bibliothèque française) sont traités.

- voir le fichier fonctions/fonctionunimarcfr.py pour les transformations

- demande de renseigner l'origine des livres et le place dans le champs origine(originality - enumeration)
- demande de renseigner le numero d'acces
     - si 0 alors prend l'information dans 995$f
     - prend le numéro spécifié est ajoute +1
------------------------------------------------------------
