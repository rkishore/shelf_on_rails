#!/bin/bash 

#for i in jcrew express; do 
for i in bananarepublic; do
    for j in mens-shirts mens-jeans womens-skirts womens-jeans; do 
		echo "Executing ruby shopstyle-pull for $i $j"; 
		#ruby /home/kishore/workspace/dSense/shopstyle-int/code/shopstyle-pull-data-into-db.rb $i $j /home/kishore/workspace/dSense/shopstyle-int/xml-data/ /home/kishore/workspace/dSense/tutorial/testDB  
		ruby /home/kishore/workspace/dSense/shopstyle-int/code/shopstyle-pull-data-into-db.rb $i $j /tmp /home/kishore/workspace/djproj/mysite2/sqlite.db
    done 
done