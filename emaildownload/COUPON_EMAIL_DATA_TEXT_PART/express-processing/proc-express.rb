#!/usr/bin/env ruby

require "raspell"
require "iconv"
require 'uri'

# Algorithm to process express coupon email
# 1. Open file
# 2. Find relevant part of email body
# 3. Find and print relevant info (Store, Discount Type, Applicability, Validity, Availability, Coupon Code) for coupon
# 4. end

class CouponInfo

  attr_accessor :brand, :subject, :discount, :code
  
  #def initialize(ibrand, idiscount, icode)
  #  @brand = ibrand
  #  @discount = idiscount
  #  @code = icode
  #end
  
end

# Return a new String without non-UTF-8 chars
class ::String
  # Thanks to http://po-ru.com/diary/fixing-invalid-utf-8-in-ruby-revisited/
  def as_utf8(from_encoding = 'UTF-8')
    ::Iconv.conv('UTF-8//IGNORE', from_encoding, self + ' ')[0..-2]
  end
end

# Open file
def open_file

  fileN = ARGV[0]

  # Format filename for printing
  @fileNs = fileN.split("/")
  fileNs_len = @fileNs.length
  #print @fileNs[fileNs_len-2], "/", @fileNs[fileNs_len-1], "\t| "

  fileO = File.open(fileN, 'r')

end

# Process email headers
def proc_email_hdrs(filePtr, coupon_obj)
  
  i = 0
  filePtr.each do |line|
    break if (i > 3)
    if (i == 0) 
      coupon_obj.brand = line.as_utf8.split("@")[1].split(">")[0].strip
      #printf("%20s | ", coupon_obj.brand)
    elsif (i == 1)
      cust_email = line.as_utf8.split("TO:")[1].strip
      #puts cust_email
    elsif (i == 2)
      coupon_obj.subject = line.as_utf8.split("SUBJECT:")[1].strip      
      #printf("%s | \n", email_subject)
    elsif (i == 3)
      date_rcvd = line.as_utf8.split("DATE:")[1].strip
      #puts date_rcvd
    end

    i += 1
  end
  
end

def proc_email_body(filePtr, coupon_obj)

  dashline_regex = /^-+$/
  express_specific_regex = /^>>(\s|\S)+$/

  body_entry = 0
  body_exit = 0

  puts ""
  puts "Subject: " + coupon_obj.subject
  puts "Relevant Email Body: "

  filePtr.each do |line|
    
    line_utf8 = line.as_utf8
    is_link = true

    # Search for line "-----..."
    if (line_utf8 =~ dashline_regex)
      
      # print body_entry.to_s, " ", body_exit.to_s, "\n"
      if ((body_entry == 0) and (body_exit == 0))
        body_entry = 1
        #print "MOD:", body_entry.to_s, " ", body_exit.to_s, "\n"
      elsif ((body_entry == 1) and (body_exit == 0))
        body_exit = 1
        #print "MOD:", body_entry.to_s, " ", body_exit.to_s, "\n"
      end
      
    end
    
    if ((body_entry == 1) and (body_exit == 0))
      
      begin
        uri = URI(line_utf8)
      rescue URI::InvalidURIError 
        #puts $!
        is_link = false
      end

      # 1st condition ensures "---..." line is ignored
      # 2nd condition ensures all hyperlinks are ignored
      # 3rd condition ensures Express-specific statements that start with ">>" are ignored
      # 4th conditiion ensures Express-specific statements related to texting-offer-to-phone are ignored 
      if ( !(line_utf8 =~ dashline_regex) and 
           (is_link == false) and 
           !(line_utf8 =~ express_specific_regex) and 
           (line_utf8.include?("Text MOBILE") == false) and 
           (line_utf8.include?("Data Rates") == false) )
        puts line_utf8
      end
      
    end
    
  end

  puts ""

end

# Main function
if __FILE__ == $0
  
  # Instantiate coupon object
  coupon = CouponInfo.new

  # Open file
  fileP = open_file

  # Process email headers
  proc_email_hdrs(fileP, coupon)

  # Process email body
  proc_email_body(fileP, coupon)



end 



# Coupon code parsing
# code_regex = /promo code(.*)|Use code(.*)|offer code(.*)|enter code(.*)/i 
#print "Code: "

#print "|\n"

