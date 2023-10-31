#!/usr/bin/bash

#script de test des différents fichiers unimarc .pan rencontrés.
# BDP MAIL
# BDP WEB
# MOCCAM utf8


echo "Test avec l'outil pan2bq_cli.py sur quel type de fichier .pan ?"
select i in BDP_WEB BDP_MAIL MOCCAM ; do

if [ $i == "BDP_WEB" ] ; then
    echo "test sur fichier BDP_WEB"
    ./pan2bq_cli.py ../00_Banc_de_test_fichiers_pan/BDP_WEB.pan ../00_Banc_de_test_fichiers_pan/BDP_WEB.pan.csv BDP-9999-01 1
fi

if [ $i == "BDP_MAIL" ] ; then
    echo "test sur fichier BDP_MAIL"
    ./pan2bq_cli.py ../00_Banc_de_test_fichiers_pan/BDP_MAIL.pan ../00_Banc_de_test_fichiers_pan/BDP_WEB.MAIL.csv BDP-9999-01 0
fi

if [ $i == "MOCCAM" ] ; then
    echo "test sur fichier Moccam"
    ./pan2bq_cli.py ../00_Banc_de_test_fichiers_pan/MOCCAM.unimarc.pan ../00_Banc_de_test_fichiers_pan/MOCCAM.unimarc.pan.csv DON-9999 10000
fi
break
done
