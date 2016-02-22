#!/bin/bash

# Merci @viencentp010 et son post sur http://forum.ubuntu-fr.org/viewtopic.php?pid=3918706#p3918706

i=1
text=""

while [ $i -lt 1000 ];
do
     text="${text} ${i}.xml http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getMEAs/${i}"

     # si argument on recherche dans fichiers
     if [ -n "$1" ]; then
       result=$(cat ${i}.xml | grep -ci "$1")
       if [ $result -gt 0 ];
       then
        echo ${i}.xml
        echo $result
       fi
     fi
     i=$(($i+1))
done

# si aucun argument on telecharge 10 par 10 fichiers
if [ -z "$1" ]; then
   echo $text | xargs -n 2 -P 10 xmllint --noent --format --output
fi
