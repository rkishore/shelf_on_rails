# == Schema Information
#
# Table name: users
#
#  id         :integer         not null, primary key
#  name       :string(255)
#  email      :string(255)
#  sex        :string(255)
#  shirt_size :string(255)
#  pant_size  :string(255)
#  created_at :datetime
#  updated_at :datetime
#

class User < ActiveRecord::Base
  
  attr_accessible :name, :email, :sex, :shirt_size, :pant_size

  email_regex = /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i

  validates :name, :presence => true, :length => { :maximum => 50 } 

  validates :email, :presence => true, :format => { :with => email_regex }, :uniqueness => { :case_sensitive => false }
  
  validates :sex, :presence => true, :length => { :maximum => 6 } 
  validates :shirt_size, :presence => true, :length => { :maximum => 6 } 
  validates :pant_size, :presence => true, :length => { :maximum => 6 } 
  
end
