awk 'BEGIN{i=0} {print i, $1, $2, (($1-$2)*100)/$1; i++}' ../data/overall_item_express.txt > ../data/overall_item_with_disc_express.txt
awk 'BEGIN{i=0} {print i, $1, $2, (($1-$2)*100)/$1; i++}' ../data/overall_item_j.crew.txt > ../data/overall_item_with_disc_j.crew.txt
awk 'BEGIN{i=0} {print i, $1, $2, (($1-$2)*100)/$1; i++}' ../data/overall_item_br.txt > ../data/overall_item_with_disc_br.txt
