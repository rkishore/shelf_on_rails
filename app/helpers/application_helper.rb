module ApplicationHelper
  
  #def logo
  #  img_loc = "ds-logo.png"
  #  alt_txt = "DiscountSense"
  #  if img_loc.nil?
  #    alt_txt
  #  else 
  #    img_loc
  #  end
  #end

  # Return a title on a per-page basis
  def title
    base_title = "DiscountSense alpha demo"
    if @title.nil?
      base_title
    else 
      "#{base_title} | #{@title}"
    end
  end
end
