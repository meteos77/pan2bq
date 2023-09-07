#!/usr/bin/env bash

repertoiredestination="biblioteq-pan2bq"
fichierdestination="BiblioteQ-pan2bq-2023-08-31_32champs"

if [ ! -x /usr/bin/dpkg-deb ]; then
    echo "Please install dpkg-deb."
    exit
fi

if [ ! -x /usr/bin/fakeroot ]; then
    echo "Please install fakeroot."
    exit 1
fi

if [ ! -r pan2bq_gui.py ]; then
    echo "Please execute $0 from the primary directory."
    exit 1
fi

# Preparation de ./usr/local/biblioteq-pan2bq :
mkdir -p ./usr/local/biblioteq-pan2bq
chmod 755 *
cp -p ./lancement-biblioteq-pan2bq.sh ./usr/local/biblioteq-pan2bq/
cp -p ./pan2bq_cli.py ./usr/local/biblioteq-pan2bq/pan2bq_cli
cp -p ./pan2bq_gui.py ./usr/local/biblioteq-pan2bq/pan2bq_gui
cp -p ./Icons/biblioteq-pan2bq.png ./usr/local/biblioteq-pan2bq/
cp -pr ./UI/ ./usr/local/biblioteq-pan2bq/.
cp -pr ./fonctions/ ./usr/local/biblioteq-pan2bq/.
cp -pr ./Documentations/ ./usr/local/biblioteq-pan2bq/.
cp -pr ./Translations/ ./usr/local/biblioteq-pan2bq/.


echo "2eme étape : Preparation du paquet  biblioteq-pan2bq-x.deb :"
mkdir -p $repertoiredestination-debian/usr/local
mkdir -p $repertoiredestination-debian/usr/share/applications
cp -p ./biblioteq-pan2bq.desktop $repertoiredestination-debian/usr/share/applications/
cp -pr ./DEBIAN $repertoiredestination-debian/
cp -r ./usr/local/biblioteq-pan2bq $repertoiredestination-debian/usr/local/
fakeroot dpkg-deb --build $repertoiredestination-debian $fichierdestination.deb

rm -fr ./usr
rm -fr ./$repertoiredestination
