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
    @attr = { :name => "Example User", 
      :email => "user@example.com", 
      :sex => "Female", 
      :shirt_size => "Small", 
      :pant_size => "Small", 
      :password => "foobar", 
      :password_confirmation => "foobar"
    }
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

  describe "password validations" do
    
    it "should require a password" do
      User.new(@attr.merge(:password => "", :password_confirmation => "")).
        should_not be_valid
    end

    it "should require a matching password confirmation" do
      User.new(@attr.merge(:password_confirmation => "invalid")).
        should_not be_valid
    end
    
    it "should reject short passwords" do
      short = "a" * 5
      hash = @attr.merge(:password => short, :password_confirmation => short)
      User.new(hash).should_not be_valid
    end
    
    it "should reject long passwords" do
      long = "a" * 41
      hash = @attr.merge(:password => long, :password_confirmation => long)
      User.new(hash).should_not be_valid
    end
  
  end
  
  describe "password encryption" do
    
    before(:each) do
      @user = User.create!(@attr)
    end
    
    it "should have an encrypted password attribute" do
      @user.should respond_to(:encrypted_password)      
    end

    it "should set the encrypted password" do
      @user.encrypted_password.should_not be_blank
    end

    describe "has_password? method" do
      
      it "should be true if the passwords match" do
        @user.has_password?(@attr[:password]).should be_true
      end    
      
      it "should be false if the passwords don't match" do
        @user.has_password?("invalid").should be_false
      end 
    end    
    
    describe "authenticate method" do
      
      it "should return nil on email/password mismatch" do
        wrong_password_user = User.authenticate(@attr[:email], "wrongpass")
        wrong_password_user.should be_nil
      end
      
      it "should return nil for an email address with no user" do
        nonexistent_user = User.authenticate("bar@foo.com", @attr[:password])
        nonexistent_user.should be_nil
      end

      it "should return the user on email/password match" do
        matching_user = User.authenticate(@attr[:email], @attr[:password])
        matching_user.should == @user
      end
    end
  end
  
end

