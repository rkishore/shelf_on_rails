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

require 'spec_helper'

describe User do

  before(:each) do
    @attr = { :name => "Example User", :email => "user@example.com", :sex => "Female", :shirt_size => "Small", :pant_size => "Small" }
  end
  
  it "should create a new instance given valid attributes" do
    User.create!(@attr)
  end
  
  it "should require a name" do
    no_name_user = User.new(@attr.merge(:name => ""))
    no_name_user.should_not be_valid
  end 

  it "should require an email address" do
    no_name_user = User.new(@attr.merge(:email => ""))
    no_name_user.should_not be_valid
  end 

  it "should require a sex" do
    no_name_user = User.new(@attr.merge(:sex => ""))
    no_name_user.should_not be_valid
  end 

  it "should require a shirt_size" do
    no_name_user = User.new(@attr.merge(:shirt_size => ""))
    no_name_user.should_not be_valid
  end 

  it "should require a pant_size" do
    no_name_user = User.new(@attr.merge(:pant_size => ""))
    no_name_user.should_not be_valid
  end 

  it "should reject names longer than fifty chars" do
    long_name = "a" * 51
    long_name_user = User.new(@attr.merge(:name => long_name))
    long_name_user.should_not be_valid
  end

  it "should reject sex longer than six chars" do
    long_sex = "a" * 7
    long_sex_user = User.new(@attr.merge(:sex => long_sex))
    long_sex_user.should_not be_valid
  end

  it "should reject shirt_size longer than six chars" do
    long_ss = "a" * 7
    long_ss_user = User.new(@attr.merge(:shirt_size => long_ss))
    long_ss_user.should_not be_valid
  end

  it "should reject pant_size longer than six chars" do
    long_ps = "a" * 7
    long_ps_user = User.new(@attr.merge(:pant_size => long_ps))
    long_ps_user.should_not be_valid
  end

  it "should accept valid email addresses" do
    addresses = %w[user@foo.com the_user@foo.bar.org first_last@foo.jp]
    addresses.each do |address|
      valid_email_addr = User.new(@attr.merge(:email => address))
      valid_email_addr.should be_valid
    end    
  end

  it "should reject invalid email addresses" do
    addresses = %w[user@foo,com user_at_foo.org example.user@foo.]
    addresses.each do |address|
      invalid_email_addr = User.new(@attr.merge(:email => address))
      invalid_email_addr.should_not be_valid    
    end
  end

  it "should reject duplicate email addresses" do
    User.create!(@attr)
    user_with_duplicate_email = User.new(@attr)
    user_with_duplicate_email.should_not be_valid
  end

  it "should reject email addresses identical up to case" do
    upcased_email = @attr[:email].upcase
    User.create!(@attr.merge(:email => upcased_email))
    user_with_duplicate_email = User.new(@attr)
    user_with_duplicate_email.should_not be_valid
  end

end
