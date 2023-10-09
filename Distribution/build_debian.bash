#!/usr/bin/env bash

repertoiredestination="biblioteq-pan2bq"
fichierdestination="BiblioteQ-pan2bq-2023-10-09_32champs"

if [ ! -x /usr/bin/dpkg-deb ]; then
    echo "Please install dpkg-deb."
    exit
fi

if [ ! -x /usr/bin/fakeroot ]; then
    echo "Please install fakeroot."
    exit 1
fi

if [ ! -r pan2bq_gui.py ]; then
    echo "Merci d'executer $0 depuis le repertoire principal."
    exit 1
fi

# Preparation de ./usr/local/biblioteq-pan2bq :
mkdir -p ./opt/biblioteq-pan2bq
echo "copie des programmes .sh ; _cli et _gui"
cp -p ./lancement-biblioteq-pan2bq.sh ./opt/biblioteq-pan2bq/
cp -p ./pan2bq_cli.py ./opt/biblioteq-pan2bq/pan2bq_cli
cp -p ./pan2bq_gui.py ./opt/biblioteq-pan2bq/pan2bq_gui
echo "copie de icone"
cp -p ./Icons/biblioteq-pan2bq.png ./opt/biblioteq-pan2bq/
echo "copie de l'interface graphiqe UI"
cp -pr ./UI/ ./opt/biblioteq-pan2bq/.
echo "copie des fonctions"
cp -pr ./fonctions/ ./opt/biblioteq-pan2bq/.
echo "copie de la documentations"
cp -pr ./Documentations/ ./opt/biblioteq-pan2bq/.
echo "copie des traductions"
cp -pr ./Translations/ ./opt/biblioteq-pan2bq/.


echo "2eme étape : Preparation du paquet  biblioteq-pan2bq-x.deb :"
mkdir -p $repertoiredestination/opt
mkdir -p $repertoiredestination/usr/share/applications
cp -p ./biblioteq-pan2bq.desktop $repertoiredestination/usr/share/applications/
cp -pr ./DEBIAN $repertoiredestination/
cp -r ./opt/biblioteq-pan2bq $repertoiredestination/opt/
echo "génération du package debian .deb"
fakeroot dpkg-deb --build $repertoiredestination $fichierdestination.deb

rm -fr ./opt
rm -fr ./$repertoiredestination
