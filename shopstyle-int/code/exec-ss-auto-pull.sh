#!/bin/bash 

for i in jcrew express bananarepublic; do
    for j in mens-shirts mens-jeans mens-sweaters womens-skirts womens-jeans womens-sweaters; do
		echo "Executing ruby shopstyle-pull for $i $j"; 
		ruby /Users/atulsingh/Documents/workspace2/dSense/shopstyle-int/code/shopstyle-pull-data-into-db.rb $i $j /Users/atulsingh/Documents/workspace2/dSense/shopstyle-int/xml-data/ /Users/atulsingh/Documents/workspace2/dSense/tutorial/testDB  
		#ruby /home/kishore/workspace/dSense/shopstyle-int/code/shopstyle-pull-data-into-db.rb $i $j /tmp /home/kishore/workspace/djproj/mysite2/sqlite.db
    done 
done
