module ApplicationHelper
  
  #def logo
  #  img_loc = "logo.png"
  #  alt_txt = "Sample App"
  #  if img_loc.nil?
  #    alt_txt
  #  else 
  #    img_loc
  #  end
  #end

  # Return a title on a per-page basis
  def title
    base_title = "Ruby on Rails Tutorial Sample App"
    if @title.nil?
      base_title
    else 
      "#{base_title} | #{@title}"
    end
  end
end
