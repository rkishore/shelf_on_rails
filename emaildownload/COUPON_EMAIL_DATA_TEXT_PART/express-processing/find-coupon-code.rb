#!/usr/bin/env ruby

require "raspell"
require "iconv"

# Algorithm to find coupon code
# 1. Open file
# 2. Search through each line for keyword "code" (case-insensitive search)
# 3. if ((next_word != dictionary word) || 
# 4.     (next_word == dictionary_word) && (next_word == capitalized)) 
# 5.     print "Code = ", next_word
# 6. end

fileN = ARGV[0]
fileO = File.open(fileN, 'r')

# Format filename for printing
@fileNs = fileN.split("/")
fileNs_len = @fileNs.length
#print @fileNs[fileNs_len-2], "/", @fileNs[fileNs_len-1], "\t| "

# Store name parsing
tmp_string = fileO.first.split("<")[1]
store_name = tmp_string.split("@")[0]
printf("%30s | ", store_name)

# Coupon code parsing
code_regex = /promo code(.*)|Use code(.*)|offer code(.*)|enter code(.*)/i 
@spell_chk = Aspell.new
class ::String
  # Return a new String that has been transliterated into UTF-8
  # Should work in Ruby 1.8 and Ruby 1.9 thanks to http://po-ru.com/diary/fixing-invalid-utf-8-in-ruby-revisited/
  def as_utf8(from_encoding = 'UTF-8')
    ::Iconv.conv('UTF-8//IGNORE', from_encoding, self + ' ')[0..-2]
  end
end

print "Code: "

fileO.each do |line|
  
  line_utf8 = line.to_s.as_utf8

  #puts line
  if ( line_utf8 =~ code_regex )

    #puts line_utf8
    @arr = line_utf8.split 
    i = 0
    @arr.each do |word|
  
      #print word, " "
      if ( word =~ /code(.*)/i )
        if (!@arr[i+1].to_s.empty?) 

          nxt_word = @arr[i+1].split(".")[0]
          valid_word = @spell_chk.check(nxt_word)          
          nxt_word_upcase = nxt_word.upcase

          #print nxt_word, " ", nxt_word_upcase, "\n"

          if ( !valid_word or ((valid_word) and (nxt_word == nxt_word_upcase)) )
            print nxt_word, ", "
          end
        end
      end
      i += 1
    end    
  end
  
end

print "|\n"

