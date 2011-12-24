# -*- coding: utf-8 -*-
require 'nokogiri'
require 'open-uri'
require 'net/http'

# Pseudo-code
# 1. Accept cmd-line arguments: brand/store, category
# 2. Call shopstyle URL with info, and process received arguments
# 3. Write output to file

# Valid categories are: mens-shirts (mens-dress-shirts, mens-longsleeve-shirts, mens-shortsleeve-shirts, mens-polo-shirts, mens-tees-and-tshirts), mens-pants, and mens-jeans
#                       womens-jeans, womens-sweaters

def process_pernode_info(pernode, fp)

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
  
  fp.print(pr_br_name.text, " | ")
  
  i = 0
  pr_category.each do |l|
    fp.print(l.text) #.to_s.strip
    i += 1
    fp.print(", ") if !(i == pr_category.length)
  end  
  
  fp.print(" | ", pr_price.text)

  if ((pr_saleprice.nil? == false) and (pr_saleprice.text.empty? == false))
    fp.print(", ", pr_saleprice.text, " |\n") 
  else 
    fp.print(", ", pr_price.text, " |\n")
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


def parse_each_product(filename, brand, category, time)

  # Create file to store XML data
  data_filename = "../data/" + brand.downcase + "-" + category + "-ss-" + time.year.to_s + "-" + time.month.to_s + "-" + time.day.to_s + ".data"
  fp = File.open(data_filename, 'w')

  reader = Nokogiri::XML::Reader.from_io(File.open(filename))

  reader.each do |node|

    if node.name == 'Product' and node.node_type == Nokogiri::XML::Reader::TYPE_ELEMENT

      doc = Nokogiri::XML(node.outer_xml)
      process_pernode_info(doc, fp)

    end
  end

end

def fetch_xml_into_file(url_str, fp)

  # Read line-by-line and write to file
  @doc = Nokogiri::XML(open(url_str))
  fp.puts(@doc)

end

def get_xml_data(brand, category, time)
 
  # Create file to store XML data
  xml_filename = "../xml-data/" + brand.downcase + "-" + category + "-ss-" + time.year.to_s + "-" + time.month.to_s + "-" + time.day.to_s + ".xml"
  fp = File.open(xml_filename, 'w')

  # First, we get the number of items in the category, i.e. product_cnt
  init_url = construct_shopstyle_url(brand, category, 0, 1)
  @doc = Nokogiri::XML(open(init_url))
  product_cnt_tag = @doc.xpath('//TotalCount')
  product_cnt = product_cnt_tag.text.to_i
  
  # Next, we fetch item info 250 items at a time (max. allowed pull number by shopstyle API)
  max_allowed_records = 250 # dictated by shopstyle.com API
  num_iter = product_cnt / max_allowed_records
  num_last_cnt = product_cnt % max_allowed_records
  # print "Num iterations: "+num_iter.to_s+" "+num_last_cnt.to_s+"\n"
  i = 0
  min_cnt = 0
  while(i < num_iter)
    #print i.to_s+" "+min_cnt.to_s+" "+max_allowed_records.to_s+"\n"
    url_str = construct_shopstyle_url(brand, category, min_cnt, max_allowed_records)
    # Dump XML into file
    fetch_xml_into_file(url_str, fp)    
    min_cnt += 250
    i += 1  
  end
  
  # Fetch remaining item info
  url_str = construct_shopstyle_url(brand, category, min_cnt, num_last_cnt)
  # Dump XML into file
  fetch_xml_into_file(url_str, fp)
  
  return fp
  
end

def construct_shopstyle_url(brand, category, min_idx, rec_cnt)
  
  if (brand.casecmp("j.crew") == 0)
    url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts=&cat="+category.to_s+"&fl=b284"+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  elsif (brand.casecmp("express") == 0)
    url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts=&cat="+category.to_s+"&fl=b13342"+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  end
  
end

if __FILE__ == $0

  if ARGV.length < 2
    puts "Usage    : ruby $0 brand category"
    puts "Example 1: ruby $0 express mens-jeans"
    puts "Example 2: ruby $0 j.crew womens-jeans"
    exit
  end

  store_name = ARGV[0]
  spl_cat = ARGV[1].split("-")
  if (spl_cat[0].casecmp("womens") == 0)
    category = spl_cat[1]
  elsif (spl_cat[0].casecmp("mens") == 0)
    category = spl_cat[0] + "-" + spl_cat[1] 
  elsif ((spl_cat[0].casecmp("jeans") == 0) or 
         (spl_cat[0].casecmp("shirts") == 0) or 
         (spl_cat[0].casecmp("sweaters") == 0) or 
         (spl_cat[0].casecmp("skirts") == 0)) 
    category = spl_cat[0]
  else
    puts "Unknown category: " + spl_cat[0].to_s + ". Exiting..."
    exit
  end
  
  puts "Brand: " + store_name + ", Category: " + category

  time = Time.new  
  xml_fname = get_xml_data(store_name, category, time)  
  parse_each_product(xml_fname, store_name, category, time)
  
end

