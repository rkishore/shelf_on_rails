#!/bin/bash

PWD=`pwd`
DIR=`ls $PWD/rootofsavvypurse`
for i in $DIR
do
    FILES=`ls $PWD/rootofsavvypurse/$i`
    for j in $FILES
    do
	#echo "Processing: $PWD/rootofsavvypurse/$i/$j"
	ruby code-find.rb $PWD/rootofsavvypurse/$i/$j
    done
done 

