# -*- coding: utf-8 -*-
require 'nokogiri'
require 'open-uri'
require 'net/http'
require 'rubygems'  
require 'active_record'  

#EXPRESS_BRAND_ID = 1
#JCREW_BRAND_ID = 2

# Pseudo-code
# 1. Accept cmd-line arguments: brand/store, category
# 2. Call shopstyle URL with info, and process received arguments
# 3. Write output to db

# Categories are: mens-shirts, mens-jeans, womens-skirts, womens-jeans

def process_pernode_info(pernode, category, time, brandinfo_arr)

  pr_id = pernode.xpath('//Product/Id')
  pr_name = pernode.xpath('//Product/Name')
  pr_br_name = pernode.xpath('//Product/BrandName')
  pr_currency = pernode.xpath('//Product/Currency')
  pr_price = pernode.xpath('//Product/Price')
  pr_instock = pernode.xpath('//Product/InStock')
  pr_retailer = pernode.xpath('//Product/Retailer')
  pr_category = pernode.xpath('//Product/Category')
  pr_saleprice = pernode.xpath('//Product/SalePrice') 
  pr_image = pernode.xpath('//Product/Image/Url') 
  pr_color = pernode.xpath('//Product/Color/Name') 
  pr_size = pernode.xpath('//Product/Size/Name') 
  
  # Determine brand_id
  br_id = ""
  brandinfo_arr.each do |l|
    if (pr_br_name.text.strip.casecmp(l.name.strip) == 0)
      #print "Match: " + l.name.strip + " with " + pr_br_name.text + "\n"
      #print "Match: ID = " + l.id.to_s + "\n"
      br_id = l.id.to_s
      break
    end
  end

  # TODO: if br_id is nill, input new brand name and match with that ID

  # Determine gender
  spl_cat = category.split("-")
  if (spl_cat[0].casecmp("womens") == 0)
    p_gender = 'F'
  elsif (spl_cat[0].casecmp("mens") == 0)
    p_gender = 'M'
  end

  # Determine product categories (up to five supported right now)
  i = 0
  p_cat = ['Empty', 'Empty', 'Empty', 'Empty', 'Empty']
  pr_category.each do |l|
    p_cat[i] = l.text
    i += 1
    break if (i > 4)
  end  

  # Determine saleprice
  if ((pr_saleprice.nil? == false) and (pr_saleprice.text.empty? == false))
    p_saleprice = pr_saleprice.text
  else 
    p_saleprice = pr_price.text
  end

  # Determine image urls (for small, medium and large sizes)
  i = 0
  p_img = ['Empty', 'Empty', 'Empty']
  pr_image.each do |l|
    p_img[i] = l.text
    i += 1
    break if (i > 2)
  end  

  tmp_array = [br_id, pr_name.text, p_gender, p_cat[0], p_cat[1], p_cat[2], p_cat[3], p_cat[4], pr_price.text, p_saleprice, p_img[0], p_img[1], p_img[2]]
  
  return tmp_array

  #Clothes_item.create(:brand_id => br_id, :name => pr_name.text, :gender => p_gender, :cat1 => p_cat[0], :cat2 => p_cat[1], :cat3 => p_cat[2], :cat4 => p_cat[3], :cat5 => p_cat[4], :price => pr_price.text, :saleprice => p_saleprice, :insert_date => time.strftime("%Y-%m-%d %H:%M:%S"))
  
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


def parse_product_info(filename, brand, category, time, dbpath)

  brand_arr = []
  item_cl_name_str = ""
  brand_cl_name_str = ""

  # Establish connection to database
  ActiveRecord::Base.establish_connection(  
                                          :adapter => "sqlite3",  
                                          :database => dbpath,
                                          )  

  # Determine table name and create corresponding Class  
  # In table names, find one that includes "items" substring and capitalize!
  table_a = ActiveRecord::Base.connection.tables
  table_a.each do |l|
    if (l.index('items') != nil) 
      item_cl_name_str = l.capitalize!
    end
    if (l.index('brands') != nil) 
      brand_cl_name_str = l.capitalize!
    end
  end

  item_cl_name = Object.const_set(item_cl_name_str, Class.new(ActiveRecord::Base))
  brand_cl_name = Object.const_set(brand_cl_name_str, Class.new(ActiveRecord::Base))

  brand_arr[0] = brand_cl_name.find_by_name("Express")
  brand_arr[1] = brand_cl_name.find_by_name("J.Crew")

  reader = Nokogiri::XML::Reader.from_io(File.open(filename))

  reader.each do |node|

    if node.name == 'Product' and node.node_type == Nokogiri::XML::Reader::TYPE_ELEMENT

      doc = Nokogiri::XML(node.outer_xml)
      tmp_arr = process_pernode_info(doc, category, time, brand_arr)
      item_cl_name.create(:brand_id => tmp_arr[0], 
                          :name => tmp_arr[1], 
                          :gender => tmp_arr[2], 
                          :cat1 => tmp_arr[3], 
                          :cat2 => tmp_arr[4], 
                          :cat3 => tmp_arr[5], 
                          :cat4 => tmp_arr[6], 
                          :cat5 => tmp_arr[7], 
                          :price => tmp_arr[8], 
                          :saleprice => tmp_arr[9], 
                          :insert_date => time.strftime("%Y-%m-%d %H:%M:%S"), 
                          :img_url_sm => tmp_arr[10], 
                          :img_url_md => tmp_arr[11], 
                          :img_url_lg => tmp_arr[12], 
                          )
      
    end
  end

end

def fetch_xml_into_file(url_str, fp)

  # Read line-by-line and write to file
  @doc = Nokogiri::XML(open(url_str))
  fp.puts(@doc)

end

def get_xml_data(brand, category, time)

  spl_cat = category.split("-")
  if (spl_cat[0].casecmp("womens") == 0)
    url_cat = spl_cat[1]
  else
    url_cat = category
  end
  
  # Create file to store XML data
  xml_filename = "/home/kishore/workspace/sample_app/shopstyle-int/xml-data/" + brand.downcase + "-" + category + "-ss-" + time.year.to_s + "-" + time.month.to_s + "-" + time.day.to_s + ".xml"
  fp = File.open(xml_filename, 'w')

  # First, we get the number of items in the category, i.e. product_cnt
  init_url = construct_shopstyle_url(brand, url_cat, 0, 1)
  @doc = Nokogiri::XML(open(init_url))
  product_cnt_tag = @doc.xpath('//TotalCount')
  product_cnt = product_cnt_tag.text.to_i

  print "Total product count: " + product_cnt.to_s + "\n"
  #product_cnt_tmp = 5

  # Next, we fetch item info 250 items at a time (max. allowed pull number by shopstyle API)
  max_allowed_records = 250 # dictated by shopstyle.com API
  num_iter = product_cnt / max_allowed_records
  num_last_cnt = product_cnt % max_allowed_records
  print "Num iterations: "+num_iter.to_s+" "+num_last_cnt.to_s+"\n"
  min_cnt = 0

  # if product_cnt > max_allowed_records
  if (num_iter > 0)
    print "Should not be here 1 \n"
    i = 0
    while(i < num_iter)
      print "Should not be here 2 \n"
      #print i.to_s+" "+min_cnt.to_s+" "+max_allowed_records.to_s+"\n"
      url_str = construct_shopstyle_url(brand, url_cat, min_cnt, max_allowed_records)
      # Dump XML into file
      fetch_xml_into_file(url_str, fp)    
      min_cnt += 250
      i += 1  
    end
  end

  # Fetch remaining item info
  url_str = construct_shopstyle_url(brand, url_cat, min_cnt, num_last_cnt)
  
  # Dump XML into file
  fetch_xml_into_file(url_str, fp)

  return fp
  
end

def construct_shopstyle_url(brand, category, min_idx, rec_cnt)
  
  if (brand.casecmp("jcrew") == 0)
    url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts=&cat="+category.to_s+"&fl=b284"+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  elsif (brand.casecmp("express") == 0)
    url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts=&cat="+category.to_s+"&fl=b13342"+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  end
  
end

if __FILE__ == $0

  if ARGV.length < 3
    puts "Usage    : ruby $0 brand category /path/to/db"
    puts "Example 1: ruby $0 express mens-jeans /home/kishore/workspace/djproj/mysite2/sqlite.db"
    puts "Example 2: ruby $0 jcrew womens-jeans /home/kishore/workspace/djproj/mysite2/sqlite.db"
    exit
  end

  store_name = ARGV[0]
  category = ARGV[1]
  dbpath = ARGV[2]
  #appname = ARGV[3]

  puts "Brand: " + store_name + ", Category: " + category + ", dbpath: " + dbpath #+ ", appname: " + appname

  time = Time.new  
  xml_fname = get_xml_data(store_name, category, time)  
  parse_product_info(xml_fname, store_name, category, time, dbpath)
  
end

