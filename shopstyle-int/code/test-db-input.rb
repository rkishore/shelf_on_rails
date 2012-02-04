require 'rubygems'  
require 'active_record'  
ActiveRecord::Base.establish_connection(  
:adapter => "sqlite3",  
:database => "/home/kishore/workspace/djproj/mysite2/sqlite.db"  
)  
  
class Clothes_brand < ActiveRecord::Base  
end

class Clothes_item < ActiveRecord::Base  
end

#brand = Clothes_brand.find(:first)
timenow = Time.now

puts timenow.strftime("%Y-%m-%d %H:%M:%S")

#puts Clothes_brand.find_all_by_name("Express")

Clothes_item.create(:brand_id => '2', :name => 'Test3', :gender => 'M', :cat1 => 'Dress-shirts', :cat2 => 'Empty', :cat3 => 'Empty', :cat4 => 'Empty', :cat5 => 'Empty', :price => '69.9', :saleprice => '69.9', :insert_date => timenow.strftime("%Y-%m-%d %H:%M:%S"))

#puts %{#{store_info.name}}
