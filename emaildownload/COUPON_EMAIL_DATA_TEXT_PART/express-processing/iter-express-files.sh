#!/bin/bash

DIR=/home/kishore/rails_projects/sample_app/emaildownload/COUPON_EMAIL_DATA_TEXT_PART/rootofsavvypurse
DIR_LS=`ls $DIR`

for i in $DIR_LS
do
    FILES=`ls $DIR/$i | grep Express`
    for j in $FILES
    do
	#echo "Processing: $PWD/rootofsavvypurse/$i/$j"
	ruby proc-express.rb $DIR/$i/$j
    done
done 

