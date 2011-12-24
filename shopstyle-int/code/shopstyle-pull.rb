# -*- coding: utf-8 -*-
require 'nokogiri'
require 'open-uri'
require 'net/http'

# Pseudo-code
# 1. Accept cmd-line arguments: item-txt, item-category, color, size, male/female, brand
# 2. Call shopstyle URL with info, and process received arguments
# 3. Filter and present results

# Valid categories for men's shirts are: mens-shirts, mens-dress-shirts, mens-longsleeve-shirts, mens-shortsleeve-shirts, mens-polo-shirts, mens-tees-and-tshirts

# TODO: 
# 1. Figure out how to use Nokogiri to parse color, and size fields, which may contain
#    more than one entry, and need to be dealt with accordingly.
# 2. Figure out filter arguments to the url to refine search further

item_txt = ARGV[0]
item_cat = ARGV[1]

#puts item_txt, item_cat

def call_shopstyle_api(item, category, min_idx, rec_cnt)
  url_str = "http://api.shopstyle.com/action/apiSearch?pid=uid289-3680017-16&fts="+item.to_s+"&cat="+category.to_s+"&min="+min_idx.to_s+"&count="+rec_cnt.to_s
  #puts url_str
  @doc = Nokogiri::XML(open(url_str))
end

def print_record_info(item, category, min_idx, rec_cnt)

  @doc = call_shopstyle_api(item, category, min_idx, rec_cnt)

  pr_id = @doc.xpath('//Product/Id')
  pr_name = @doc.xpath('//Product/Name')
  pr_br_name = @doc.xpath('//Product/BrandName')
  pr_currency = @doc.xpath('//Product/Currency')
  pr_price = @doc.xpath('//Product/Price')
  pr_instock = @doc.xpath('//Product/InStock')
  pr_retailer = @doc.xpath('//Product/Retailer')
  pr_saleprice = @doc.xpath('//Product/SalePrice')

  rec_cnt.times { |idx|    
    if pr_id[idx].nil?
      print "nil | "      
    else
      print pr_id[idx].text+" | " 
    end
    
    if pr_br_name[idx].nil?
      print "nil | "      
    else
      print pr_br_name[idx].text+" | " 
    end

    if pr_name[idx].nil?
      print "nil | "      
    else
      print pr_name[idx].text+" | " 
    end

    if pr_price[idx].nil?
      print "nil, "      
    else 
      print pr_price[idx].text+", "
    end

    if pr_saleprice[idx].nil?
      if pr_price[idx].nil?
        print "nil "
      else
        print pr_price[idx].text+" "
      end
    else
      print pr_saleprice[idx].text+" " 
    end
      
    if pr_currency[idx].nil?
      print "nil | "      
    else
      print pr_currency[idx].text+" | " 
    end

    if pr_instock[idx].nil?    
      print "nil | "      
    else 
      print pr_instock[idx].text+" |\n" 
    end

    #if (!pr_id[idx].nil? and !pr_br_name[idx].nil? and !pr_price[idx].nil? and !pr_saleprice[idx].nil? and !pr_currency[idx].nil? and !pr_instock[idx].nil?) 
  }

end

# Get total number of items
@xmldoc = call_shopstyle_api(item_txt, item_cat, 0, 1)
product_cnt_tag = @xmldoc.xpath('//TotalCount')
product_cnt = product_cnt_tag.text.to_i

#puts "Total number of longsleeve dress shirts: "+product_cnt.to_s
#exit

# Debug. Do not use @url.
# puts url_str
# @the_url = URI.parse(url_str)
# @response = Net::HTTP.get_response(@the_url)
# puts @response.to_s

# Cycle through all available items
max_allowed_records = 250 # dictated by shopstyle.com API
num_iter = product_cnt / max_allowed_records
num_last_cnt = product_cnt % max_allowed_records
#print "Num iterations: "+num_iter.to_s+" "+num_last_cnt.to_s+"\n"
i = 0
min_cnt = 0
while(i < num_iter)
  #print i.to_s+" "+min_cnt.to_s+" "+max_allowed_records.to_s+"\n"
  print_record_info(item_txt, item_cat, min_cnt, max_allowed_records)
  min_cnt += 250
  i += 1  
end
#print i.to_s+" "+min_cnt.to_s+" "+num_last_cnt.to_s+"\n"
print_record_info(item_txt, item_cat, min_cnt, num_last_cnt)


