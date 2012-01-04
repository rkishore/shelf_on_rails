#!/bin/bash 

for i in jcrew, express; do 
    for j in mens-shirts mens-jeans womens-skirts womens-jeans; do 
	echo "Executing ruby shopstyle-pull for $i $j"; 
	ruby /home/kishore/workspace/sample_app/shopstyle-int/code/shopstyle-pull-data-into-db.rb $i $j /home/kishore/workspace/sample_app/tutorial/testDB  
    done 
done