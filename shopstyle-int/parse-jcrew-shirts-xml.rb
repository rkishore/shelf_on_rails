# -*- coding: utf-8 -*-
require 'nokogiri'
require 'open-uri'
require 'net/http'

#def call_shopstyle_api(item, category, min_idx, rec_cnt)
#  url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts="+item.to_s+"&cat="+category.to_s+"&fl=b284"+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  #puts url_str                                                                                                 
#  @doc = Nokogiri::XML(open(url_str))
#end

def process_pernode_info(pernode)

  pr_id = pernode.xpath('//Product/Id')
  pr_name = pernode.xpath('//Product/Name')
  pr_br_name = pernode.xpath('//Product/BrandName')
  pr_currency = pernode.xpath('//Product/Currency')
  pr_price = pernode.xpath('//Product/Price')
  pr_instock = pernode.xpath('//Product/InStock')
  pr_retailer = pernode.xpath('//Product/Retailer')
  pr_category = pernode.xpath('//Product/Category')
  pr_saleprice = pernode.xpath('//Product/SalePrice') 
  pr_color = pernode.xpath('//Product/Color/Name') 
  pr_size = pernode.xpath('//Product/Size/Name') 
  
  print pr_br_name.text, " | "
  
  i = 0
  pr_category.each do |l|
    print l.text #.to_s.strip
    i += 1
    print ", " if !(i == pr_category.length)
  end  
  
  print " | ", pr_price.text

  if ((pr_saleprice.nil? == false) and (pr_saleprice.text.empty? == false))
    print ", ", pr_saleprice.text, " |\n" 
  else 
    print ", ", pr_price.text, " |\n"
  end
  #print " ", pr_currency.text, " |\n "

  #print pr_br_name.text, " | ", pr_name.text, " | ", pr_price.text
  #print ",", pr_saleprice.text if ((pr_saleprice.nil? == false) and (pr_saleprice.text.empty? == false))
  #print " ", pr_currency.text, " | ", pr_instock.text, " | "
  
  # Print available colors
  #i = 0
  #pr_color.each do |l|
  #  print l.text.to_s.strip
  #  i += 1
  #  print ", " if !(i == pr_color.length)
  #end
  #print " | "
  
  # Print available sizes
  #i = 0
  #pr_size.each do |l|
  #  print l.text.to_s.strip
  #  i += 1
  #  print ", " if !(i == pr_size.length)
  #end
  #print " | \n"
  
end

def parse_each_product(filename)
  
  #puts "Processing: "+filename
  reader = Nokogiri::XML::Reader.from_io(File.open(filename))
  
  reader.each do |node|
    
    if node.name == 'Product' and node.node_type == Nokogiri::XML::Reader::TYPE_ELEMENT
      
      doc = Nokogiri::XML(node.outer_xml)      
      process_pernode_info(doc)

    end
  end

  
end


# Main
if __FILE__ == $0
  
  parse_each_product(ARGV[0])  
  
end

