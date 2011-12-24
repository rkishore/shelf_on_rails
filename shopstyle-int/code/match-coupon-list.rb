


# Main
if __FILE__ == $0
  
  # Read in items and coupons file
  f1 = File.open("/tmp/spec-itemlist")
  f2 = File.open("/tmp/coupons")

  items = []
  i = 0
  f1.each do |l|
    @arr = l.split("|")
    items[i] = { :brand => @arr[0].strip, :sex => @arr[1].strip, :what => @arr[2].strip, :price => @arr[3].strip }
    i += 1
  end

  puts items[0]
  puts items[1]
  puts items[2]
  puts items[3]

  coupons = []
  i = 0
  f2.each do |l|
    @arr = l.split("|")
    #puts @arr
    #coupons[i] = { :brand => @arr[0].to_s.strip, :discount => @arr[1].to_s.strip, :what => @arr[2].to_s.strip, :code => @arr[3].to_s.strip }
    coupons[i] = { :brand => @arr[0].strip, :discount => @arr[1].to_s.strip, :what => @arr[2].to_s.strip, :code => @arr[3].to_s.strip }
    i += 1
  end

  puts coupons[0]
  puts coupons[1]

end
